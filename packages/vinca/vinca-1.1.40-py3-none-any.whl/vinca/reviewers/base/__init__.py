# a basic card reviewer making use of cat and readchar
import subprocess
import readchar
import datetime

from . import video
# we could refactor this into the card class and make
# a function add_grade instead of add_history
today = datetime.date.today() 

grade_dict = {'-': -3,
	      '@': -2,
	      'x': -1,
	      'q': -1,
	      'u': -1,
	      'h': 0,
	      'w': 0,
	      '1': 1,
	      '2': 2,
	      '3': 3,
	      '4': 4,
	      ' ': 3,
	      '\r': 3,
	      '\n': 3}

cont_dict = {'-': 1,
	     '@': 1,
	     'x': 1,
	     'q': 0,
	     'u': -1,
	     'h': -1,
	     'w': 0,
	     '1': 1,
	     '2': 1,
	     '3': 1,
	     '4': 1,
	     ' ': 1,
	     '\r': 1,
	     '\n': 1}

assert cont_dict.keys() == grade_dict.keys()

def review(card,mode):
	# clear screen
	# show front
	# wait for keystroke / check if mode is preview
	# show back
	# call editor(?) / add a single card
	# assign grade (incl. schedule for suspend, bury, deletion)
	# call scheduler
	# return continue value

	# save the screen; tput smcup generates an escape code
	# which tells the terminal to save the screen
	# processes like vim, top, and less use this to recover the terminal at the end

	start = datetime.datetime.now()  # begin card timer

	subprocess.run(['tput','smcup'])
	subprocess.run(['tput','civis'])

	image_back = None
	def show_card():
		global image_back
		subprocess.run(['clear'])
		subprocess.run(['tput','civis'])

		# text
		subprocess.run(['cat',card.path / 'front'])  # view frontside

		# audio
		audio_front_path = card.path / 'audio_front'
		audio_front = Recording(audio_front_path) if audio_front_path.exists() else None
		if audio_front: audio_front.play()

		# images
		image_front_path = card.path / 'image_front'
		image_front = video.DisplayImage(image_front_path) if image_front_path.exists() else None
		if image_front: image_front.show()

		# card flip
		if mode == 'review':
			char = readchar.readchar() # later I might allow adding and quitting on the frontside

		# backside text
		subprocess.run(['echo','\n\n']) # dividing space
		subprocess.run(['cat',card.path / 'back'])  # view backside

		# erase frontside audio/images
		if audio_front: audio_front.stop()
		if image_front: image_front.close()
			
		# audio
		audio_back_path = card.path / 'audio_back'
		audio_back = Recording(audio_back_path) if audio_back_path.exists() else None
		if audio_back: audio_back.play()

		# images
		image_back_path = card.path / 'image_back'
		image_back = video.DisplayImage(image_back_path) if image_back_path.exists() else None
		if image_back: image_back.show()

	show_card()

	char = None
	while char not in grade_dict.keys():
		if char in ['e','f','b','*']:
			subprocess.run(['tput','rmcup']) # restore terminal state so that vim does not overwrite smcup
			card.edit(mode=char)
			subprocess.run(['tput','smcup']) 
			show_card()
		char = readchar.readchar()

	grade = grade_dict[char]
	cont = cont_dict[char]

	stop = datetime.datetime.now()  # stop card timer
	elapsed_time = min(120, (stop - start).seconds)
	
	card.add_history(today, elapsed_time, grade)

	# restore terminal
	if image_back: image_back.close()
	subprocess.run(['tput','rmcup'])
	subprocess.run(['tput','cvvis'])
	
	return cont
	# -1 means go back to previous card
	# 0 means exit
	# 1 means continue
