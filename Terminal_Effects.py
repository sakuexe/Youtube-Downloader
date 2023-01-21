import os

class tcolors:
	cyan = '\033[96m'
	green = '\033[92m'
	yellow = '\033[93m'
	red = '\033[91m'
	gray = '\033[90m'
	clear = '\033[0m'
	underline = '\033[4m'
	bold = '\033[1m'

class clear_terminal:
	def clear():
		return os.system('cls' if os.name == 'nt' else 'clear')