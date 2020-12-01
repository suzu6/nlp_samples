import numpy as np


class Variable:
    def __init__(self, data):
        self.data = data


class Function:
    def __call__(self, input: Variable) -> Variable:
        x = input.data
        y = self.forward(x)
        output = Variable(y)
        return output
    
    def forward(self, x):
        raise NotImplementedError()


class Square(Function):
    def forward(self, x):
        return x ** 2


class Exp(Function):
    def forward(self, x):
        return np.exp(x)

if __name__ == "__main__":
    data = np.array(0.5)
    A = Square()
    B = Exp()
    C = Square()

    x = Variable(data)
    a = A(x)
    b = B(a)
    y = C(b)
    
    print(type(y))
    print(y.data)