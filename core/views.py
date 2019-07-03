from django.http import JsonResponse
import json
import random


def delay(request, station):
	response = {
		'average_delay': random.randint(0, 300),
		'delay_probability': random.randint(0, 90)
	}

	return JsonResponse(response)
