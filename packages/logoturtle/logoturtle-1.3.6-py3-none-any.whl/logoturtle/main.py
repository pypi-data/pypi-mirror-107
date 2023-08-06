def main():
	import turtle, sys
	from .parsing import parse_input, parse_line
	print("Logoturtle, by Elia Toselli S.")
	t = turtle.Turtle()
	if len(sys.argv) <= 1:
		try:
			print("Press Control-C to stop. Don't worry.\n\n")
			while 1:
				parse_input()(t)
		except KeyboardInterrupt:
			print("\nClosed")
			sys.exit(0)
	else: # script mode
		try:
			for line in open(sys.argv[1], "r"):
				parse_line(line)(t)
			input("\nPress Enter to end script")
		except KeyboardInterrupt:
			sys.exit(1)
		
