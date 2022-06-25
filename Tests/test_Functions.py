import sys
import testRead
if testRead.check("test_Functions"):
    # We assume the user is in the main directory.
    # TODO find Program folder and change to that.
    sys.path.insert(0, './Program/Files')
    import Functions

    def test_Test():
        assert Functions.tests()


print("Test: test_ShipInfo disabled!") 
assert True  #  but disabled