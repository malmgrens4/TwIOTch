import signal
from src.blueteeth.toolbox import toolbox
from inputs import get_gamepad


def main():
    cam = toolbox.get_camaro()
    ms = 10

    led_on = 0
    js_threshold = 5000
    movement_ms = 4
    moving_forward = False
    moving_backward = False
    turning_left = False
    turning_right = False
    while 1:
        events = get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)
            if event.ev_type == 'Key':
                if event.code == 'BTN_SOUTH':
                    if led_on:
                        cam.light_on()
                    else:
                        cam.light_off()
            if event.ev_type == 'Absolute':
                if abs(event.state) > js_threshold:
                    if event.code == 'ABS_Y':
                        if event.state < 0:
                            moving_forward = True
                            moving_backward = False
                        else:
                            moving_backward = True
                            moving_forward = False

                    if event.code == 'ABS_RX':
                        if event.state < 0:
                            turning_left = True
                            turning_right = False
                        else:
                            turning_right = True
                            turning_left = False

                else:
                    moving_backward = False
                    moving_forward = False
                    moving_forward = False
                    moving_backward = False

                if moving_forward:
                    cam.forward(movement_ms)
                if moving_backward:
                    cam.backward(movement_ms)
                if turning_left:
                    cam.left(movement_ms)
                if turning_right:
                    cam.right(movement_ms)




if __name__ == '__main__':
    main()
