
from blessed import Terminal

t = Terminal()

def hw(name):
	print(f"hello {t.red}{name}{t.normal}")

if __name__ == '__main__':
	hw("world")
