# this is the test/example_test.py file
# import some code from the app dir
# invoke that code with certain inputs
# ... to ensure it produces the expected outputs
# we have to name our test functions with test_
# ... for pytest to collect them
# def test______():
#     pass
# EXPECT THAT THE ENLARGE FUNCTION RETURNS A LARGER NUMBER
from app.example import enlarge, to_usd
#from app.example import to_usd
def test_enlarge():
    #assert True
    #assert False
    #assert 2 == 2
    #assert 2 == 5
    assert enlarge(9) == 900
# EXPECT THAT WE GET A ROUNDED STRING BACK WITH DOLLAR SIGN
def test_to_usd():
    assert to_usd(23.2222) == "$23.22"

    
