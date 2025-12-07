"""
sample tests
"""
from django.test import SimpleTestCase
from app import calc
#defining the test case class
class CalcTests(SimpleTestCase):
    """Test the calc module"""
    #adding a test method
    def test_add_numbers(self):
        #test adding numbers together
        res=calc.add(5,6)
        self.assertEqual(res,11)
    def test_subtract_numbers(self):
        res= calc.subtract(10,15)
        self.assertEqual(res, 5)