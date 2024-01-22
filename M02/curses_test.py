import curses 
from curses import wrapper

# screen = curses.initscr() 
# #curses.noecho() 
# curses.curs_set(0) 
# screen.keypad(1) 
# curses.mousemask(curses.ALL_MOUSE_EVENTS)

# screen.addstr("This is a Sample Curses Script\n\n") 

# key=0
# while key!=27: # Esc to close
#     key = screen.getch() 
#     #screen.erase()
#     if key == curses.KEY_MOUSE:
#         _, mx, my, _, _ = curses.getmouse()
#         y, x = screen.getyx()
#         # screen.addstr('mx, my = %i,%i                \r'%(mx,my))
#         screen.addstr(y, x, screen.instr(my, mx, 5))
#     #screen.refresh()

# curses.endwin()



# def main(stdscr):
#     curses.curs_set(0)
#     curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
#     print("\033[?1003h\n") # allows capturing mouse movement

#     while True:
#         c = stdscr.getch()
#         if c == curses.KEY_MOUSE:
#             try:
#                 event = curses.getmouse()
#                 x = event[2]
#                 y = event[1]
#                 dims = stdscr.getmaxyx()
#                 stdscr.addstr(0,0,"="*dims[1])
#                 stdscr.addstr(0,dims[1]-len(str(dims)),str(dims))
#                 stdscr.addstr(0,0,str(event))
#                 if event[4] == 4:
#                     stdscr.addstr(x,y,"X")
#                 else:
#                     stdscr.addstr(x,y,"*")
#             except:
#                 pass
#         stdscr.refresh()

# curses.wrapper(main)



# https://hyperskill.org/blog/post/introduction-to-the-curses-library-in-python-text-based-interfaces
# def main(stdscr):
#    stdscr.clear()
#    stdscr.addstr('Click on the screen...')
#    curses.mousemask(curses.ALL_MOUSE_EVENTS)

#    while True:
#        key = stdscr.getch()

#        if key == ord('q'):
#            break
#        elif key == curses.KEY_MOUSE:
#            _, mx, my, _, _ = curses.getmouse()
#            stdscr.clear()
#            stdscr.addstr(f'You clicked at {my}, {mx}')

# wrapper(main)



def main(stdscr):
    # Clear screen
    stdscr.clear()

    # This raises ZeroDivisionError when i == 10.
    for i in range(0, 9):
        v = i-10
        stdscr.addstr(i, 0, '10 divided by {} is {}'.format(v, 10/v))

    stdscr.refresh()
    stdscr.getkey()

wrapper(main)