import importlib
Test2 = importlib.import_module('.Test2', 'importTest')
# Test2 = importlib.import_module('Test2')
# Test2 = importlib.import_module('.Test2', 'Test1')
# Test2 = importlib.import_module('.Test2', 'E')

print('Hello World')
Test2.hi()
