import RPi.GPIO as GPIO

from mail import Mail


class Buttons(Mail):
    def __init__(self, green, yellow, red, blue):
        self.green = green
        self.yellow = yellow
        self.red = red
        self.blue = blue

        self.count = {}
        self.message = """
Daily report:
Total: {total}
Green: {green} ({greenp:.1f}%)
Yellow: {yellow} ({yellowp:.1f}%)
Red: {red} ({redp:.1f}%)
Blue: {blue} ({bluep:.1f}%)
        """

    def mail_setup(self, sender, password):
        super().__init__(sender, password)

    def pressed(self, a):
        match a:
            case self.green:
                self.count["green"] = self.count["green"] + 1 if self.count.get("green") else 1
            case self.yellow:
                self.count["yellow"] = self.count["yellow"] + 1 if self.count.get("yellow") else 1
            case self.red:
                self.count["red"] = self.count["red"] + 1 if self.count.get("red") else 1
            case self.blue:
                self.count["blue"] = self.count["blue"] + 1 if self.count.get("blue") else 1
        print(self.count)

    def send_gmail(self,receiver, reset=True):
        total = sum(self.count.values())
        green = self.count["green"] if self.count.get("green") else 0
        yellow = self.count["yellow"] if self.count.get("yellow") else 0
        red = self.count["red"] if self.count.get("red") else 0
        blue = self.count["blue"] if self.count.get("blue") else 0
        if (green + yellow + red + blue) == 0:
            super().send(receiver,"Button isn't pressed since last reset.")
        else:
            print(green / total * 100)
            super().send(
                receiver,
                self.message.format(
                    total=total,
                    green=green,
                    yellow=yellow,
                    red=red,
                    blue=blue,
                    greenp=green / total * 100,
                    yellowp=yellow / total * 100,
                    redp=red / total * 100,
                    bluep=blue / total * 100
                )
            )
        if reset:
            self.reset()

    def reset(self):
        self.count = {}


def setup(pins: list, a, pull_up_down=GPIO.PUD_DOWN):
    for i in pins:
        GPIO.setup(i, a, pull_up_down=pull_up_down)


def add_event_detect(pins: list, a, callback=None, bouncetime=0):
    for pin in pins:
        GPIO.add_event_detect(pin, a, callback=callback, bouncetime=300)
