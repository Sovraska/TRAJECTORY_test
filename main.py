from vehicle_api import VehicleManger, Vehicle

if __name__ == '__main__':
    manager = VehicleManger(url="https://test.tspb.su/test-task")

    manager.get_vehicles()

    print("filter_vehicles", manager.filter_vehicles(params={"name": "Mercedes"}))

    print("get_vehicle", manager.get_vehicle(vehicle_id=1))

    print("add_vehicle", manager.add_vehicle(
        vehicle=Vehicle(
            name='Toyota',
            model='Camry',
            year=2021,
            color='red',
            price=21000,
            latitude=55.753215,
            longitude=37.620393
        )
    )
          )

    print("update_vehicle", manager.update_vehicle(
            vehicle=Vehicle(
                id=1,
                name='Toyota',
                model='Camry',
                year=2021,
                color='red',
                price=21000,
                latitude=55.753215,
                longitude=37.620393
            )
        )
    )

    print("delete_vehicle", manager.delete_vehicle(id=1))

    print("get_distance", manager.get_distance(id1=1, id2=2))

    print("get_nearest_vehicle", manager.get_nearest_vehicle(id=1))
