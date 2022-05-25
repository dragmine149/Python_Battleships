import sys
# We assume the user is in the main directory.
# TODO find Program folder and change to that.
sys.path.insert(0, './Program')
import Functions

def test_Test():
    assert Functions.tests()
    
