# -*- encoding: utf-8 -*-
import os
import sys
import csv


class CarBase:
    """Базовый класс для машинок"""
    def __init__(self, brand, photo_file_name, carrying):
        self.brand = brand
        self.photo_file_name = photo_file_name
        self.carrying = float(carrying)

    def get_photo_file_ext(self):
        return os.path.splitext(self.photo_file_name)[1]

    @staticmethod
    def is_correct(row):
        if not len(row):
            return False
        car_type = row[0]
        types = ['car', 'truck', 'spec_machine']
        if car_type not in types:
            return False
        for i in range(1, 6, 2):
            if not row[i]:
                return False
        '''     #Они считают, что это лишняя проверка, но я не согласен!
        if not os.path.splitext(row[3])[1]:
            return False
        '''
        try:
            float(row[5])
        except ValueError:
            return False
        return True


class Car(CarBase):
    """Класс легковушка"""

    car_type = 'car'

    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        self.passenger_seats_count = passenger_seats_count

    @staticmethod
    def is_correct(row):
        try:
            int(row[2])
        except ValueError:
            return False
        return True

    @staticmethod
    def get_parameters(row):
        return row[1], row[3], float(row[5]), int(row[2])


class Truck(CarBase):
    """Класс грузовик"""

    car_type = 'truck'

    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        if not body_whl:
            self.body_length = 0
            self.body_width = 0
            self.body_height = 0
        else:
            size_list = body_whl.split('x')
            self.body_length = float(size_list[0])
            self.body_width = float(size_list[1])
            self.body_height = float(size_list[2])

    def get_body_volume(self):
        return self.body_length * self.body_width * self.body_height

    @staticmethod
    def is_correct(row):
        if not row[4]:
            return True
        size_list = row[4].split('x')
        if len(size_list) != 3:
            return False
        try:
            for size in size_list:
                float(size)
        except ValueError:
            return False
        return True

    @staticmethod
    def get_parameters(row):
        return row[1], row[3], float(row[5]), row[4]


class SpecMachine(CarBase):
    """Класс спецтехника"""

    car_type = 'spec_machine'

    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        self.extra = extra

    @staticmethod
    def is_correct(row):
        return row[6]

    @staticmethod
    def get_parameters(row):
        return row[1], row[3], float(row[5]), row[6]


def get_car_list(csv_filename):
    car_list = []
    obj_dict = {'car': Car, 'truck': Truck, 'spec_machine': SpecMachine}
    with open(csv_filename) as file:
        reader = csv.reader(file, delimiter=';')
        next(reader)
        for row in reader:
            if not CarBase.is_correct(row):
                continue
            try:
                car_type = obj_dict[row[0]]
            except KeyError:
                continue
            if car_type.is_correct(row):
                obj = car_type(*car_type.get_parameters(row))
            else:
                continue
            car_list.append(obj)
    return car_list


if __name__ == '__main__':
    print(get_car_list(sys.argv[1]))
