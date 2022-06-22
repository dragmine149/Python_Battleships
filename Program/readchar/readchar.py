import importlib
key = importlib.import_module('.key', 'readchar')
readchar_main = importlib.import_module('.readchar_main', 'readchar')

readchar = readchar_main.readchar
readkey = readchar_main.readkey

__all__ = [readchar, readkey, key]
