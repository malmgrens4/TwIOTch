import os
from src.blueteeth.models.PhueLight import PhueLight
from src.blueteeth.models.RCCar import RCCar

camaro = None
needle = None


def get_phuelight():
    return PhueLight()


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
