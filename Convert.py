#!/usr/bin/env python3

from sys import stderr


class WeightCon:

    __weight_definition = (
        (('st','stone','stones'),                         'st'),
        (('lb', 'lbls', 'pound', 'pounds'),               'lb'),
        (('kg', 'kgs', 'kilog', 'kilogram', 'kilograms'), 'kg')
    )

    __weight_conversions = (
        ('st','kg', 6.35029),  ('lb','kg', 0.453592),  ('st','lb', 14)
    )

    def __init__(self):
        self.def_map = WeightCon.__definitionArray2Map(WeightCon.__weight_definition)
        self.con_map = WeightCon.__conversionArray2Map(WeightCon.__weight_conversions)

    def convert(self, fr,to):

        if fr == "":
            print("No unit given, assuming 'lb'", file=stderr)
            fr = 'lb'

        fr = self.def_map[fr]
        to = self.def_map[to]


        return self.con_map[(fr,to)]


    @staticmethod
    def __definitionArray2Map(array):
        unit_converter = {}
        for unit_types in array:
            for unit in unit_types[0]:
                unit_converter[unit] = unit_types[1]

        return unit_converter

    @staticmethod
    def __conversionArray2Map(array):
        unit_converter = {}
        for u1,u2,val in array:
            unit_converter[(u1,u2)] = val
            unit_converter[(u2,u1)] = 1/val
            unit_converter[(u1,u1)] = 1

        return unit_converter
