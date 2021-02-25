import signal
from xbox360controller import Xbox360Controller
from src.blueteeth.toolbox import toolbox


def main():


    try:
        cam = toolbox.get_camaro()
        ms = 10

        def turn_left():
            cam.left(ms)

        def turn_right():
            cam.right(ms)

        with Xbox360Controller(0, axis_threshold=0.2) as controller:
            controller.button_a.when_pressed = cam.light_on
            controller.axis_l.when_moved = turn_left
            controller.axis_r.when_moved = turn_right

        signal.pause()

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
