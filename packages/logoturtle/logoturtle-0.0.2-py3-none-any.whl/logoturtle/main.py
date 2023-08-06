def main():
	import turtle
	from .parsing import parse_input
	print("Logoturtle, by Elia Toselli S.")
	t = turtle.Turtle()
	print("Press Control-C to stop. Don't worry.")
	try:
		while 1:
			parse_input()(t)
		t.mainloop()
	except KeyboardInterrupt:
		print("\nIf you want to stop really this wonderful program, I'm sorry. Bye!")
		raise SystemExit
