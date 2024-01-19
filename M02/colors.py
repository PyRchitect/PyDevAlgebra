# STYLES:
# 0	Reset or normal
# 1	Bold or increased intensity
# 2	Faint, decreased intensity
# 3	Italic	Not widely supported
# 4	Underline

# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors

def print_3bit_table():
	# prints table of formatted text format options (3 and 4 bit)
	print("\nSTANDARD\n")
	for style in range(5):
		for fg in range(30,38):
			s1 = ''
			for bg in range(40,48):
				format = ';'.join([str(style), str(fg), str(bg)])
				s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
			print(s1)
		print('\n')
		
	print("\nBRIGHT\n")
	for style in range(5):
		for fg in range(90,98):
			s1 = ''
			for bg in range(100,108):
				format = ';'.join([str(style), str(fg), str(bg)])
				s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
			print(s1)
		print('\n')

def print_8bit_table():
	# prints table of formatted text format options (3 and 4 bit)
	print("\nSTANDARD\n")
	for s in range(256):
		print(f'\x1b[38;5;{s}m {s} \x1b[0m')
		print(f'\x1b[48;5;{s}m {s} \x1b[0m')

# def colors_256(color_):
#     num1 = str(color_)
#     num2 = str(color_).ljust(3, ' ')
#     if color_ % 16 == 0:
#         return(f"\033[38;5;{num1}m {num2} \033[0;0m\n")
#     else:
#         return(f"\033[38;5;{num1}m {num2} \033[0;0m")

# print("\nThe 256 colors scheme is:")
# print(' '.join([colors_256(x) for x in range(256)]))

print_3bit_table()
# print_8bit_table()