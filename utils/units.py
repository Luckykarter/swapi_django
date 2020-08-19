# This is special class. Is is being used a lot in different projects throughout the empire.
# It is extremely important to NOT change the way other tools interact with this class.
# However we have a hunch it could be improved. Do you have any ideas?

"""
The only thing came in mind that it can be 'improved' by
replacing hardcoded indexes with dynamic names. i.e.:
    def __init__(self):
        for i in range(1, 6):
            setattr(self, '_unit' + str(i), 0)

And properties/setters could be also defined the same way
However, it is not quite an improvement because makes the code
less maintainable since it becomes less clear what is actually
happening.

"""

class Units:
    def __init__(self):
        self._unit1 = 0
        self._unit2 = 0
        self._unit3 = 0
        self._unit4 = 0
        self._unit5 = 0

    @property
    def unit1(self):
        return self._unit1

    @unit1.setter
    def unit1(self, unit):
        self._unit1 = unit if unit % 2 == 0 else 0

    @property
    def unit2(self):
        return self._unit2

    @unit2.setter
    def unit2(self, unit):
        self._unit2 = unit if unit % 2 == 0 else 0

    @property
    def unit3(self):
        return self._unit3

    @unit3.setter
    def unit3(self, unit):
        self._unit3 = unit if unit % 2 == 0 else 0

    @property
    def unit4(self):
        return self._unit4

    @unit4.setter
    def unit4(self, unit):
        self._unit4 = unit if unit % 2 == 0 else 0

    @property
    def unit5(self):
        return self._unit5

    @unit5.setter
    def unit5(self, unit):
        self._unit5 = unit if unit % 2 == 0 else 0