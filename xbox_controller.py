import signal
from src.blueteeth.toolbox import toolbox
from inputs import get_gamepad


def main():
    cam = toolbox.get_camaro()
    ms = 10

    def turn_left():
        cam.left(ms)

    def turn_right():
        cam.right(ms)

    while 1:
        events = get_gamepad()
        for event in events:
            print(event.ev_type, event.code, event.state)


if __name__ == '__main__':
    main()
