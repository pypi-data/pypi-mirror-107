import datetime

__Name__ = "MargotRobbie"
__Version__ = "0.0.1"
__Author__ = "xFueY"
__Description__ = "Margot Robbie for Python"
__URL__ = "https://github.com/xFueY/MargotRobbie/"
__Email__ = "xFueY@protonmail.com"
__License__ = "MIT"

class MargotRobbie():
    def __init__(self):
        self.Name = "Margot Robbie"
        self.Birthday = "July 2, 1990"
        self.Height = "1.68 m"

    @property
    def Age(self):
        x = datetime.datetime.now() - datetime.datetime(1990, 7, 2)
        return str(x.days / 365).split(".")[0]
