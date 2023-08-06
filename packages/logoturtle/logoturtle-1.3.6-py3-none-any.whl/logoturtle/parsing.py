# -*- coding: utf-8 -*-

def parse_input():
	cmd = str(input("Turtle > "))
	if cmd == "": return lambda t: 0
	tks = tuple(cmd.split())
	if len(tks) < 2:
		print("Syntax error: too few arguments.")
		print("SYNTAX: Instruction parameter")
		print("""
		Instructions:
		QUIT | <any number>   - closes the program
		PU   | <any number>   - raises the turtle pen
		PD   | <any number>   - drops the same pen
		GO   | <pixels>       - moves the turtle forward for that number of pixels
		BK   | <pixels>       - moves the turtle backward for that number of pixels
		TL   | <degrees>      - turns the turtle left of that number of degrees
		TR   | <degrees>      - turns the turtle right of that number of degrees
		WG   | <weight>       - sets the line weight
		KC   | <lenght>       - draws a Koch curve
		""")
		return lambda t: 0
	istr, par = tks
	if istr == "QUIT":
		raise KeyboardInterrupt # will be catched in main.py
		# don't call me without the "main.py" wrapper
	if istr == "PU":
		return lambda t: t.pu()
	if istr == "PD":
		return lambda t: t.pd()
	if istr == "GO":
		return lambda t: t.fd(int(par))
	if istr == "BK":
		return lambda t: t.bk(int(par))
	if istr == "TL":
		return lambda t: t.lt(int(par))
	if istr == "TR":
		return lambda t: t.rt(int(par))
	if istr == "WG":
		return lambda t: t.pensize(int(par))
	print("Syntax error: unknown command")
	print("SYNTAX: Instruction parameter")
	print("""
	Instructions:
	QUIT | <any number>   - closes the program
	PU   | <any number>   - raises the turtle pen
	PD   | <any number>   - drops the same pen
	GO   | <pixels>       - moves the turtle forward for that number of pixels
	BK   | <pixels>       - moves the turtle backward for that number of pixels
	TL   | <degrees>      - turns the turtle left of that number of degrees
	TR   | <degrees>      - turns the turtle right of that number of degrees
	WG   | <weight>       - sets the line weight
	""")
	return lambda t: 0

def parse_line(cmd):
	import string
	whs = True
	for char in cmd:
		if not char in list(string.whitespace):
			whs = False
			break
	if whs:
		return lambda t: 0
	tks = tuple(cmd.split())
	if len(tks) < 2:
		print("\t COMMAND: "+ cmd)
		print("Syntax error: too few arguments.")
		print("SYNTAX: Instruction parameter")
		print("""
		Instructions:
		QUIT | <any number>   - closes the program
		PU   | <any number>   - raises the turtle pen
		PD   | <any number>   - drops the same pen
		GO   | <pixels>       - moves the turtle forward for that number of pixels
		BK   | <pixels>       - moves the turtle backward for that number of pixels
		TL   | <degrees>      - turns the turtle left of that number of degrees
		TR   | <degrees>      - turns the turtle right of that number of degrees
		WG   | <weight>       - sets the line weight
		##   | <any string>   - defines a comment. It's ignored.
		""")
		raise KeyboardInterrupt
	istr, par = tks[0], tks[1]
	if istr == "##":
		return lambda t: 0
	if istr == "QUIT":
		raise KeyboardInterrupt # will be catched in main.py
		# don't call me without the "main.py" wrapper
	if istr == "PU":
		return lambda t: t.pu()
	if istr == "PD":
		return lambda t: t.pd()
	if istr == "GO":
		return lambda t: t.fd(int(par))
	if istr == "BK":
		return lambda t: t.bk(int(par))
	if istr == "TL":
		return lambda t: t.lt(int(par))
	if istr == "TR":
		return lambda t: t.rt(int(par))
	if istr == "WG":
		return lambda t: t.pensize(int(par))
	print("\t COMMAND: "+ cmd)
	print("Syntax error: unknown command")
	print("SYNTAX: Instruction parameter")
	print("""
	Instructions:
	QUIT | <any number>   - closes the program
	PU   | <any number>   - raises the turtle pen
	PD   | <any number>   - drops the same pen
	GO   | <pixels>       - moves the turtle forward for that number of pixels
	BK   | <pixels>       - moves the turtle backward for that number of pixels
	TL   | <degrees>      - turns the turtle left of that number of degrees
	TR   | <degrees>      - turns the turtle right of that number of degrees
	WG   | <weight>       - sets the line weight
	""")
	raise KeyboardInterrupt
