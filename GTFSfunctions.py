import requests
import pandas as pd
from google.transit import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict
from datetime import datetime

# Function to fetch real-time positions
def getRealTimePositions(url: str, headers: dict) -> pd.DataFrame:
    response = requests.get(url, headers=headers)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    feed = MessageToDict(feed)

    entities = feed['entity']
    parsed_data = []

    for entity in entities:
        vehicle = entity['vehicle']
        trip = vehicle['trip']
        position = vehicle['position']
        vehicle_info = vehicle['vehicle']
        
        parsed_data.append({
            'id': entity['id'],
            'isDeleted': entity['isDeleted'],
            'tripId': trip['tripId'],
            'startTime': datetime.strptime(trip['startTime'], '%H:%M:%S').time(),
            'startDate': datetime.strptime(trip['startDate'], '%Y%m%d').date(),
            'scheduleRelationship': trip['scheduleRelationship'],
            'routeId': trip['routeId'],
            'directionId': trip['directionId'],
            'latitude': position['latitude'],
            'longitude': position['longitude'],
            'bearing': position['bearing'],
            'currentStopSequence': vehicle.get('currentStopSequence'),
            'currentStatus': vehicle.get('currentStatus'),
            'timestamp': datetime.fromtimestamp(int(vehicle['timestamp'])),
            'stopId': vehicle.get('stopId'),
            'vehicleId': vehicle_info['id'],
            'label': vehicle_info['label'],
            'licensePlate': vehicle_info['licensePlate'],
            'occupancyStatus': vehicle.get('occupancyStatus')
        })

    df = pd.DataFrame(parsed_data)
    df.set_index('id', inplace=True)
    return df

def getRealTimeTripUpdates(url: str, headers: dict) -> pd.DataFrame:
    response = requests.get(url, headers=headers)
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    feed = MessageToDict(feed)

    entities = feed['entity']
    parsed_data = []

    for entity in entities:
        trip_update = entity['tripUpdate']
        trip = trip_update['trip']
        stop_time_updates = trip_update['stopTimeUpdate']

        for stop_time_update in stop_time_updates:
            parsed_data.append({
                'id': entity['id'],
                'tripId': trip['tripId'],
                'startTime': datetime.strptime(trip['startTime'], '%H:%M:%S').time(),
                'startDate': datetime.strptime(trip['startDate'], '%Y%m%d').date(),
                'scheduleRelationship': trip.get('scheduleRelationship', None),
                'routeId': trip.get('routeId', None),
                'directionId': trip.get('directionId', None),
                'stopSequence': stop_time_update.get('stopSequence', None),
                'arrival': datetime.fromtimestamp(int(stop_time_update['arrival']['time'])) if 'arrival' in stop_time_update else None,
                'departure': datetime.fromtimestamp(int(stop_time_update['departure']['time'])) if 'departure' in stop_time_update else None,
                'stopId': stop_time_update.get('stopId', None),
            })

    df = pd.DataFrame(parsed_data)
    df.set_index('id', inplace=True)
    return df

# Function to read shapes.csv and filter data
def getShapeCSV() -> pd.DataFrame:
    routeShapes = pd.read_csv('static/shapes.csv')
    routeShapes = routeShapes[routeShapes['shape_id'].isin(['RRED_16', 'RGRN_72', 'RYEL_96', 'RBLU_47', 'RSLV_192', 'RORG_134'])]
    shape_id_mapping = {
        'RRED_16': 'RED',
        'RGRN_72': 'GREEN',
        'RYEL_96': 'YELLOW',
        'RBLU_47': 'BLUE',
        'RSLV_192': 'SILVER',
        'RORG_134': 'ORANGE'
    }
    routeShapes['shape_id'] = routeShapes['shape_id'].map(shape_id_mapping)
    return routeShapes