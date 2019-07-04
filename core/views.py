from django.http import JsonResponse
import json
import random


def delay(request, station):
	response = {
		'average_delay': random.randint(0, 30),
		'delay_probability': random.randint(0, 90)
	}

	res = JsonResponse(response)
	res["Access-Control-Allow-Origin"] = "*"
	return res
