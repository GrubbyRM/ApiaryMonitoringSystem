from django.shortcuts import render
import json
import os
from django.http import JsonResponse
from datetime import datetime

def get_local_data():
    file_path = '/Users/gruby/Desktop/ApiaryMonitoringSystem/ApiaryMonitoringSystem/monitoring/test/data.json'
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        return {"temperature": "missing", "humidity": "missing", "weight": "missing"}
    
def get_measurements():
    data = get_local_data()
    measurements = []

    for timestamp, values in data["history"].items():
        entry = {
            "date": format_timestamp(timestamp),
            "temperature": values.get("temperature"),
            "humidity": values.get("humidity"),
            "weight": values.get("weight"),
        }
        measurements.append(entry)
    ## sort from newest to the oldest
    measurements.sort(key=lambda x: x["date"], reverse=True)
    return measurements
    
def split_date():
    data = get_local_data()
    data_list = []
    for date in data["history"]:
        data_list.append(format_timestamp(date))

    return data_list

def format_timestamp(ts):
    return datetime.fromtimestamp(int(ts)).strftime('%Y-%m-%d %H:%M:%S')
