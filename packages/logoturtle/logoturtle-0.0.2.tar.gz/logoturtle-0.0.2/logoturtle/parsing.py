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
