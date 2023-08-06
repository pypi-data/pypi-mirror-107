# The default reviewer for plaintext front/back style cards
import cursor
import datetime
today = datetime.date.today()

def review(card, mode, stdscr):
	# mode can either be review or preview
	max_y, max_x = stdscr.getmaxyx()
	# the basic card has phases	
	# First, clear the screen
	stdscr.clear()
	stdscr.refresh()

	with card.auxfile('front') as f:
		front = f.readlines()
	with card.auxfile('back') as f:
		back = f.readlines()

	def show_front():
		line_no = 3
		for line in front:
			stdscr.addstr(line_no, 7, line)
			line_no += 1
		return line_no
	def show_back():
		line_no = show_front()
		line_no += 1	
		divider = '⎯'*(max_x - 14)
		stdscr.addstr(line_no, 7, divider); line_no += 1
		line_no += 2
		for line in back:
			stdscr.addstr(line_no, 7, line)
			line_no += 1


	if mode == 'review':
		show_front()
		phase = 0
	elif mode == 'preview':
		show_back()
		phase = 1

	while True:
		# Draw the screen
		cursor.hide()
		stdscr.refresh()

		# Wait for a keystroke
		key = stdscr.getch()
		# Process the keystroke
		# TODO implement scheduling buttons
		card.add_history(today,0)

		if (key == ord('q') or key == 27) and mode=='review':  # escape key
			return 0  # this tells vinka that we should exit

		if key == ord('x'):
			# mark the card for deletion
			card.add_history(today, -1)
			return 0  # this tells vinka that we should exit

		if key == ord('\n') or key == ord('\r') or key == ord(' '):
			if phase == 0:
				show_back()
				phase += 1
			elif phase == 1:
				grade = 2 if mode == 'review' else 0
				# 2 means good
				# 0 means seen
				card.add_history(today, grade)
				return 1

		if key in [ord(str(x)) for x in range(1,10)] and mode=='review' and phase == 1:
			card.add_history(today, int(chr(key)))
			return 1

		if key == ord('e'):
			card.edit('e')
			stdscr.clear()
			phase = 1  # move to the back if we have not already
			show_back()

		if key == ord('f'):
			card.edit('f')
			stdscr.clear()
			phase = 1  # move to the back if we have not already
			show_back()


		if key == ord('b'):
			card.edit('b')
			stdscr.clear()
			phase = 1  # move to the back if we have not already
			show_back()


		if key == ord('t'):
			card.edit()
			# TODO pass 't' param to the editor to edit tags

		if key == ord('*'):
			card.edit()
			# TODO pass '*' param to the editor to mark the card

		if key == ord('@'):
			# suspend the card
			card.add_history(today, -2)
			return 1

		if key == ord('-'):
			# bury the card
			card.add_history(today, -3)
			return 1

		if key == ord('k') and mode=='review':
			phase = 0
			stdscr.clear()
			show_front()

		if key == ord('H'):
			pass # do not change the scheduling
			return -1

		if key == ord('u'):
			pass # TODO undo
			return -1
		














