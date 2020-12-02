import unittest
import dezero as dz
import numpy as np

class SquareTest(unittest.TestCase):
    def test_forward(self):
        x = dz.Variable(np.array(2.0))
        y = dz.square(x)
        expected = np.array(4.0)
        self.assertEqual(y.data, expected)



unittest.main()