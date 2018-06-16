from abc import ABC, abstractmethod

__version__ = "1.0"
__author__ = "Reza Payambari (reza.payambari@gmail.com)"


class LogFunc(ABC):
    def __init__(self, numInputs, numOutputs):
        self.__Inputs = [False] * numInputs
        self.__Outputs = [False] * numOutputs
        self.__Name = type(self).__name__
        self.execute()

    # getter and setter
    def __getInputs(self):
        return self.__Inputs

    def __setInputs(self, inputs):
        self.__Inputs = inputs

    def __getOutputs(self):
        return self.__Outputs

    def _setOutputs(self, outputs):
        self.__Outputs = outputs

    def __getName(self):
        return self.__Name

    def __setName(self, name):
        self.__Name = name

    # methods
    def show(self):
        print(self.__str__())

    def __str__(self):
        self.execute()
        outputString = "Output"
        if len(self.Outputs) > 1:
            ausgangsstring = str(len(self.Outputs)) + " outputs"
        return "Inputs " + str(self.Inputs) + ", " \
               + self.Name + " with " + outputString + " folowing values: " + str(self.Outputs)

    @abstractmethod
    def execute(self):
        pass

    # properties
    Name = property(__getName, __setName)
    Inputs = property(__getInputs, __setInputs)
    Outputs = property(__getOutputs, None)


class AndGate(LogFunc):
    def __init__(self, numInputs=2):
        super().__init__(numInputs, 1)

    def execute(self):
        if self.Inputs.count(False) == 0:
            self._setOutputs(True)
        else:
            self._setOutputs(False)


class OrGate(LogFunc):
    def __init__(self, numInputs=2):
        super().__init__(numInputs, 1)

    def execute(self):
        if self.Inputs.count(True) == 0:
            self._setOutputs(False)
        else:
            self._setOutputs(True)


class XorGate(LogFunc):
    def __init__(self, numInputs=2):
        super().__init__(numInputs, 1)

    def execute(self):
        if self.Inputs.count(True) % 2 == 1:
            self._setOutputs(True)
        else:
            self._setOutputs(False)


class NandGate(LogFunc):
    def __init__(self, numInputs=2):
        super().__init__(numInputs, 1)

    def execute(self):
        if self.Inputs.count(False) == 0:
            self._setOutputs(False)
        else:
            self._setOutputs(True)


class NotGate(LogFunc):
    def __init__(self, numInputs=2):
        super().__init__(numInputs, numInputs)

    def execute(self):
        outputs = [None] * len(self.Outputs)
        for i in range(len(self.Inputs)):
            outputs[i] = not self.Inputs[i]
        self._setOutputs(outputs)


class HalfAdder(LogFunc):
    def __init__(self):
        self.__sum = XorGate(2)
        self.__carry = AndGate(2)
        super().__init__(2, 2)

    def execute(self):
        self.__sum.Inputs = self.Inputs
        self.__carry.Inputs = self.Inputs
        self.__sum.execute()
        self.__carry.execute()
        self._setOutputs([self.__carry.Outputs, self.__sum.Outputs])


class FullAdder(LogFunc):
    def __init__(self):
        self.__sum = [HalfAdder(), HalfAdder()]
        self.__carry = OrGate()
        super().__init__(3, 2)

    def execute(self):
        self.__sum[0].Inputs = [self.Inputs[0], self.Inputs[1]]
        self.__sum[0].execute()
        self.__sum[1].Inputs = [self.__sum[0].Outputs[1], self.Inputs[2]]
        self.__sum[1].execute()
        self.__carry.Inputs = [self.__sum[0].Outputs[0], self.__sum[1].Outputs[0]]
        self.__carry.execute()
        self._setOutputs([self.__carry.Outputs, self.__sum[1].Outputs[1]])


class EightBitAdder(LogFunc):
    def __init__(self):
        self.__adder = [FullAdder()] * 8
        super().__init__(16, 9)

    def execute(self):
        carry = 0
        sumOutputs = len(self.Outputs) - 1
        outputs = [None] * (sumOutputs + 1)
        for i in range(sumOutputs):
            self.__adder[i].Inputs = [carry, self.Inputs[i], self.Inputs[i + sumOutputs]]
            self.__adder[i].execute()
            carry = self.__adder[i].Outputs[0]
            outputs[i] = self.__adder[i].Outputs[1]
        outputs[sumOutputs] = carry
        self._setOutputs(outputs)
        
