import json
from django.shortcuts import render

from django.http import HttpResponse
# Create your views here.


from api import tasks


def my_data_view(request):

    info={
            "Students": [
                {
                "Name": "Tina",
                "Age": 17,
                "City": "Narsinghpur",
                "Birthday": "March 24, 2005",
                
                },
                {
                "Name": "Atharv",
                "Age": 7,
                "City": "Bhopal",
                "Birthday": "April 7, 2015",
                
                }
            ]
            }
    x = json.dumps(info,indent=2)
        
    tasks.publish_message({'hello': 'world'})
    return HttpResponse(status=201)

    # tasks.publish_message({'hello': x})
    # return HttpResponse(x, content_type ="text/plain" )