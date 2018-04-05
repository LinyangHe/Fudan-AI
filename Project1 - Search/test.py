import os
class ProrityQueue(object):
    """docstring for ProrityQueue."""
    def __init__(self, number):
        super(ProrityQueue, self).__init__()
        self.number = number
    def PrintNumber(self):
        print(self.number)
test = ProrityQueue(15)
test.PrintNumber()
