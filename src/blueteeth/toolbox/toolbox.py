import os
from src.blueteeth.models.PhueLight import PhueLight
from src.blueteeth.models.RCCar import RCCar

camaro = None
needle = None
phue_light = None


def get_phuelight():
    global phue_light
    if not phue_light:
        phue_light = PhueLight()
    return phue_light


def get_camaro():
    global camaro
    if camaro is None:
        camaro = RCCar(os.environ['CAMARO_MAC'])
    return camaro


def get_needle():
    global needle
    if needle is None:
        needle = RCCar(os.environ['NEEDLE_MAC'])
    return needle
