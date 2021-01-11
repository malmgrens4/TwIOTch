from src.blueteeth.models.Stepper import Stepper
from src.blueteeth.models import PhueLight

dino_stepper_mac = 'Pull from config file'
cat_stepper_mac = 'None'

# TODO reimplement a retry for instantiating the objects
# Would it make more sense to establish the connection here and pass that to the object?


def get_phuelight():
    return PhueLight()


def get_dino_stepper():
    return Stepper(dino_stepper_mac)


def get_cat_stepper():
    return Stepper(cat_stepper_mac)
