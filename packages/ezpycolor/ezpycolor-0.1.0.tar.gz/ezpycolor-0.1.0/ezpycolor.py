class ColorClass:
	PURPLE = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	GOLD = '\033[33m'
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	BGPURPLE = '\033[95;7m'
	BGBLUE = '\033[94;7m'
	BGGREEN = '\033[92;7m'
	BGYELLOW = '\033[93;7m'
	BGGOLD = '\033[33;7m'
	BGRED = '\033[91;7m'
	RESET = '\033[0m'

def printpurple(x):
	print(ColorClass.PURPLE+str(x)+ColorClass.RESET)

def printblue(x):
	print(ColorClass.BLUE+str(x)+ColorClass.RESET)

def printgreen(x):
	print(ColorClass.GREEN+str(x)+ColorClass.RESET)

def printyellow(x):
	print(ColorClass.YELLOW+str(x)+ColorClass.RESET)

def printgold(x):
	print(ColorClass.GOLD+str(x)+ColorClass.RESET)

def printred(x):
	print(ColorClass.RED+str(x)+ColorClass.RESET)

def printbold(x):
	print(ColorClass.BOLD+str(x)+ColorClass.RESET)

def printunderline(x):
	print(ColorClass.UNDERLINE+str(x)+ColorClass.RESET)

def printbgpurple(x):
	print(ColorClass.BGPURPLE+str(x)+ColorClass.RESET)

def printbgblue(x):
	print(ColorClass.BGBLUE+str(x)+ColorClass.RESET)

def printbggreen(x):
	print(ColorClass.BGGREEN+str(x)+ColorClass.RESET)

def printbgyellow(x):
	print(ColorClass.BGYELLOW+str(x)+ColorClass.RESET)

def printbggold(x):
	print(ColorClass.BGGOLD+str(x)+ColorClass.RESET)

def printbgred(x):
	print(ColorClass.BGRED+str(x)+ColorClass.RESET)

def printrainbow(x):
	cl = [ColorClass.RED, ColorClass.YELLOW, ColorClass.GREEN, ColorClass.BLUE, ColorClass.PURPLE]
	r = ColorClass.RESET
	output = ""
	counter = 0
	for letter in str(x):
		if letter.isspace():
			output += " "
		else:
			output += cl[counter]+letter
			counter += 1
		if counter > len(cl)-1:
			counter = 0
	output += r # add reset
	print(output)

def printbgrainbow(x):
	cl = [ColorClass.BGRED, ColorClass.BGYELLOW, ColorClass.BGGREEN, ColorClass.BGBLUE, ColorClass.BGPURPLE]
	r = ColorClass.RESET
	output = ""
	counter = 0
	for letter in str(x):
		if letter.isspace():
			output += " "
		else:
			output += cl[counter]+letter
			counter += 1
		if counter > len(cl)-1:
			counter = 0
	output += r # add reset
	print(output)

#=============

def colorpurple(x):
	return(ColorClass.PURPLE+str(x)+ColorClass.RESET)

def colorblue(x):
	return(ColorClass.BLUE+str(x)+ColorClass.RESET)

def colorgreen(x):
	return(ColorClass.GREEN+str(x)+ColorClass.RESET)

def coloryellow(x):
	return(ColorClass.YELLOW+str(x)+ColorClass.RESET)

def colorgold(x):
	return(ColorClass.GOLD+str(x)+ColorClass.RESET)

def colorred(x):
	return(ColorClass.RED+str(x)+ColorClass.RESET)

def colorbold(x):
	return(ColorClass.BOLD+str(x)+ColorClass.RESET)

def colorunderline(x):
	return(ColorClass.UNDERLINE+str(x)+ColorClass.RESET)

def colorbgpurple(x):
	return(ColorClass.BGPURPLE+str(x)+ColorClass.RESET)

def colorbgblue(x):
	return(ColorClass.BGBLUE+str(x)+ColorClass.RESET)

def colorbggreen(x):
	return(ColorClass.BGGREEN+str(x)+ColorClass.RESET)

def colorbgyellow(x):
	return(ColorClass.BGYELLOW+str(x)+ColorClass.RESET)

def colorbggold(x):
	return(ColorClass.BGGOLD+str(x)+ColorClass.RESET)

def colorbgred(x):
	return(ColorClass.BGRED+str(x)+ColorClass.RESET)

def colorrainbow(x):
	cl = [ColorClass.RED, ColorClass.YELLOW, ColorClass.GREEN, ColorClass.BLUE, ColorClass.PURPLE]
	r = ColorClass.RESET
	output = ""
	counter = 0
	for letter in str(x):
		if letter.isspace():
			output += " "
		else:
			output += cl[counter]+letter
			counter += 1
		if counter > len(cl)-1:
			counter = 0
	output += r # add reset
	return(output)

def colorbgrainbow(x):
	cl = [ColorClass.BGRED, ColorClass.BGYELLOW, ColorClass.BGGREEN, ColorClass.BGBLUE, ColorClass.BGPURPLE]
	r = ColorClass.RESET
	output = ""
	counter = 0
	for letter in str(x):
		if letter.isspace():
			output += " "
		else:
			output += cl[counter]+letter
			counter += 1
		if counter > len(cl)-1:
			counter = 0
	output += r # add reset
	return(output)