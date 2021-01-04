import configparser
import logging.config
from models.ModelEnums import StepperDirection
from bluetooth import BluetoothError
from toolbox import toolbox

config = configparser.ConfigParser()
config.read('config.ini')

logging.config.fileConfig('config.ini')
log = logging.getLogger(__name__)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    try:
        stepper = toolbox.get_dino_stepper()
        stepper.rotate(StepperDirection.CW, 720, 50)
        stepper.rotate(StepperDirection.CCW, 720, 700)

    except BluetoothError as blue_error:
        log.exception("Dino stepper connection failure.")


# we need to test adding async calls to a stack and making sure we wait to execute each one
