#!/usr/bin/env python

import logging
import json
from ml import ML

HAS_DELAY_THRESHOLD = 60

class Convertor:
    def __init__(self, data_path, station_uris_path):
        self._logger = logging.getLogger(__name__)
        self._logger.debug("Init main")
        self.data_path = data_path
        self.station_uris_path = station_uris_path
        self.raw_data = None
        self.station_uris = None
        self.converted_data = []
        self.read_data()
        self.convert_data()

    def read_data(self):
        with open(self.data_path, "r") as f:
            self.data = json.load(f)

        with open(self.station_uris_path, "r") as f:
            self.station_uris = json.load(f)

    def convert_data(self):
        data_iter = iter(self.data)
        for entry in data_iter:
            fields = entry["fields"]

            # Discard measuring points, only real stops are allowed
            if not fields["ptcar_lg_nm_nl"].lower() in self.station_uris:
                self._logger.debug("Skipping measurement point: %s" % fields["ptcar_lg_nm_nl"])
                continue

            converted_entry = {
                "vehicle_type": fields["relation"].split()[0],
                "vehicle_number": fields["train_no"],
                #"agency": fields["train_serv"],
                "stop": self.station_uris.get(fields["ptcar_lg_nm_nl"].lower(), "NA"),
            }

            # Add departure information if available
            if "planned_date_dep" in fields:
                converted_entry["departure_datetime"] = "{} {}".format(fields["planned_date_dep"], fields["planned_time_dep"]) # <DATE>
                converted_entry["departure_delay"] = fields["delay_dep"]
                converted_entry["departure_line"] = fields.get("line_no_dep", "NA")
                converted_entry["has_departure_delay"] = fields["delay_dep"] > HAS_DELAY_THRESHOLD

            # Add arrival information if available
            if "planned_date_arr" in fields:
                converted_entry["arrival_datetime"] = "{} {}".format(fields["planned_date_arr"], fields["planned_time_arr"]) # <DATE>
                converted_entry["arrival_delay"] = fields["delay_arr"]
                converted_entry["arrival_line"] = fields.get("line_no_arr", "NA")
                converted_entry["has_arrival_delay"] = fields["delay_arr"] > HAS_DELAY_THRESHOLD

            # Add direction if available
            if "relation_direction" in fields:
                converted_entry["direction"] = fields["relation_direction"].split(": ")[1]
            # International trains like the TGV, Thalys, ... only have a
            # `relation` field
            else:
                converted_entry["direction"] = fields["relation"]


            # Generate warnings for missing data
            if ("departure" in converted_entry and converted_entry["departure"]["line"] == "NA")\
            or ("arrival" in converted_entry and converted_entry["arrival"]["line"] == "NA"):
                self._logger.warning("%s: Unknown line(s)" % converted_entry)

            if converted_entry["stop"] == "NA":
                self._logger.warning("%s: Unknown stop" % converted_entry)

            self.converted_data.append(converted_entry)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    c = Convertor("data.json", "station_uris.json")
    machine_learning = ML(c.converted_data)
    machine_learning.create_dataframe()
    machine_learning.decission_tree()


