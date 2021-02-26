import signal
from src.blueteeth.toolbox import toolbox
from inputs import get_gamepad


def main():
    try:
        cam = toolbox.get_camaro()
        ms = 10

        led_on = False
        js_threshold = 8000
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
                            cam.light_off()
                        else:
                            cam.light_on()
                        led_on = not led_on
                if event.ev_type == 'Absolute':
                    if abs(event.state):
                        if event.code == 'ABS_Y' and abs(event.state) > js_threshold:
                            if event.state < 0:
                                moving_forward = True
                                moving_backward = False
                            elif event.state > 0 and event.state > js_threshold:
                                moving_backward = True
                                moving_forward = False
                            else:
                                moving_forward = False
                                moving_backward = False

                        if event.code == 'ABS_RX':
                            if event.state < 0 and abs(event.state) > js_threshold:
                                turning_left = True
                                turning_right = False
                            elif event.state > 0 and event.state > js_threshold:
                                turning_right = True
                                turning_left = False
                            else:
                                turning_left = False
                                turning_right = False

            if moving_forward:
                cam.forward(movement_ms)
            if moving_backward:
                cam.backward(movement_ms)
            if turning_left:
                cam.left(movement_ms)
            if turning_right:
                cam.right(movement_ms)


    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
