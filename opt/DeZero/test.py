import unittest
import dezero as dz
import numpy as np

def numerical_diff(f, x, eps=1e-4):
    x0 = dz.Variable(x.data - eps)
    x1 = dz.Variable(x.data + eps)
    y0 = f(x0)
    y1 = f(x1)
    return (y1.data - y0.data) / (2 * eps)


class SquareTest(unittest.TestCase):
    def test_forward(self):
        x = dz.Variable(np.array(2.0))
        y = dz.square(x)
        expected = np.array(4.0)
        self.assertEqual(y.data, expected)
    
    def test_backward(self):
        x = dz.Variable(np.array(3.0))
        y = dz.square(x)
        y.backward()
        expected = np.array(6.0)
        self.assertEqual(x.grad, expected)

    def test_gradient_check(self):
        x = dz.Variable(np.random.rand(1))
        y = dz.square(x)
        y.backward()
        num_grad = numerical_diff(dz.square, x)
        flg = np.allclose(x.grad, num_grad)
        self.assertTrue(flg)

class ExeTest(unittest.TestCase):
    def test_forward(self):
        x = dz.Variable(np.array(2.0))
        y = dz.exp(x)
        expected = np.exp(2.0)
        self.assertEqual(y.data, expected)
    
    def test_backward(self):
        x = dz.Variable(np.array(2.0))
        y = dz.exp(x)
        y.backward()
        expected = np.exp(2.0)
        self.assertEqual(x.grad, expected)
        
    def test_gradient_check(self):
        x = dz.Variable(np.random.rand(1))
        y = dz.square(x)
        y.backward()
        num_grad = numerical_diff(dz.square, x)
        flg = np.allclose(x.grad, num_grad)
        self.assertTrue(flg)

unittest.main()
