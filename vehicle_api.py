import json
from dataclasses import dataclass
from math import asin, cos, radians, sin, sqrt
from typing import Optional

import requests

from example_env import DELETE_URL, GET_ID_URL, GET_URL, POST_URL, PUT_URL


@dataclass
class Vehicle:
    name: str
    model: str
    year: int
    color: str
    price: int
    latitude: float
    longitude: float
    id: Optional[int] = None

    def __repr__(self):
        return (f'{self.name} {self.model} '
                f'{self.year} {self.color} {self.price}')


class VehicleManger:
    def __init__(self, url):
        self.url = url

    @staticmethod
    def wrap_vehicle(vehicle):
        return Vehicle(
            id=vehicle['id'],
            name=vehicle['name'],
            model=vehicle['model'],
            year=vehicle['year'],
            color=vehicle['color'],
            price=vehicle['price'],
            latitude=vehicle['latitude'],
            longitude=vehicle['longitude']
        )

    def get_vehicles(self):
        response = requests.get(f'{self.url}{GET_URL}')
        response = json.loads(response.text)
        vehicles = []
        for vehicle in response:
            vehicles.append(
                self.wrap_vehicle(vehicle)
            )
        return vehicles

    def filter_vehicles(self, params):
        response = requests.get(f'{self.url}{GET_URL}', params)
        response = json.loads(response.text)
        if len(response) > 1:  # if query params fails
            for vehicle in response:
                if list(params)[0] in vehicle:
                    if vehicle[f'{list(params)[0]}'] == list(
                            params.values()
                    )[0]:
                        return self.wrap_vehicle(vehicle)

    def get_vehicle(self, vehicle_id):
        response = requests.get(
            f'{self.url}{GET_ID_URL.format(id=vehicle_id)}'
        )
        vehicle = json.loads(response.text)
        return self.wrap_vehicle(vehicle)

    def add_vehicle(self, vehicle):
        vehicle = vehicle.__dict__
        vehicle.pop('id')
        vehicle = json.dumps(vehicle)
        response = requests.post(
            f'{self.url}{POST_URL}',
            data=vehicle,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
        )
        return Vehicle(*json.loads(response.text).values())

    def update_vehicle(self, vehicle):
        vehicle = vehicle.__dict__
        vehicle_id = vehicle.pop('id')
        vehicle = json.dumps(vehicle)
        response = requests.put(
            f'{self.url}{PUT_URL.format(id=vehicle_id)}',
            data=vehicle,
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
        )
        return Vehicle(*json.loads(response.text).values())

    def delete_vehicle(self, id):
        response = requests.delete(f'{self.url}{DELETE_URL.format(id=id)}')
        return response

    def get_distance(self, id1, id2):
        vehicle_1 = self.get_vehicle(id1)
        vehicle_2 = self.get_vehicle(id2)

        radius = 6373.0
        lat1 = radians(vehicle_1.latitude)
        lon1 = radians(vehicle_1.longitude)
        lat2 = radians(vehicle_2.latitude)
        lon2 = radians(vehicle_2.longitude)
        dlong = lon2 - lon1
        dlat = lat2 - lat1
        ans = (
                pow(
                    sin(dlat / 2), 2
                )
                + cos(lat1)
                * cos(lat2) *
                pow(
                    sin(dlong / 2), 2
                )
        )
        ans = 2 * asin(sqrt(ans))
        return ans * radius * 1000

    def get_nearest_vehicle(self, id):
        vehicles = self.get_vehicles()
        vehicles = [vehicle for vehicle in vehicles if vehicle.id != id]
        result = min(vehicles, key=lambda p: self.get_distance(id, p.id))
        return result
