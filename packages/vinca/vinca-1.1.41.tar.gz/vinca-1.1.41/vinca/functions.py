# functions
from pathlib import Path
from subprocess import run
import datetime
today = datetime.date.today()
study_day = today

import readchar  # 3rd party module for reading a character one at a time

from . import cards
col = cards.Collection()
col.cache_tags()
decklist = cards.Decklist()

from shutil import copytree, rmtree
from sys import exit

from . import editors, reviewers, schedulers
from . import browser

vinca_path = Path(__file__) # /path/to/vinca/__init__.py
vinca_path = vinca_path.parent # /path/to/vinca
cards_path = vinca_path / 'cards'
decks_path = vinca_path / 'decks.txt'
decks_vimrc = vinca_path / 'decks.vimrc'
tags_path = vinca_path / 'tags.txt'


def study(args):
	queue = browser.filter(col, deck=args.deck, due_date_end=study_day)
	# note that args.deck can be None
	done_queue = []
	while queue:
		card = queue.pop()
		cont = card.review()
		if cont == -1:
			card.undo_history()
			queue.append(card)
			if not done_queue:
				break
			prev_card = done_queue.pop()
			prev_card.undo_history()
			queue.append(prev_card)
		if cont == 0:
			card.undo_history()
			break
		if cont == 1:
			card.schedule()

def line_add(args):
	tags_create = args.deck.tags_create if args.deck else []	
	new_card = cards.Card(create=True)
	new_card.make_config('base','base','base')
	for tag in tags_create:
		new_card.add_tag(tag)
	# BAD: this reading should be implemented elsewhere
	(new_card.path/'front').write_text(input('Q:   '))
	(new_card.path/'back').write_text(input('A:   '))
	new_card.add_history(today, 0, 0)
	new_card.schedule()
def add_basic(args):
	tags_create = args.deck.tags_create if args.deck else []	
	new_card = cards.Card(create=True)
	new_card.make_config('base','base','base')
	for tag in tags_create:
		new_card.add_tag(tag)
	new_card.edit(mode='a')  # add mode
	cont = new_card.review(mode='preview')
	return new_card, cont
def add(args):
	new_card, cont = add_basic(args)
	new_card.schedule()
def add_many(args): #TODO
	 prev_card = None
	 while True:	
		 new_card, cont = add_basic(args)
		 new_card.schedule()
		 if cont == -1:
			 prev_card.review(mode='preview')  # TODO does not support multilevel
			 prev_card.undo_history()  # we do not actually want to change the old card
		 if cont == 0:
			 break
		 if cont == 1:
			 prev_card = new_card
def image_cloze(args):
	pass
def statistics(args):
	if args.deck:
		all_cards = browser.filter(col, deck=args.deck)
		due_cards = browser.filter(all_cards, due_date_end=study_day)
		print(f'{len(all_cards)} cards total')
		print(f'{len(due_cards)} cards due today')
	elif args.card:
		print(f'Due: {args.card.due_date}')
		print(f'Tags: {" ".join(args.card.tags)}')
		print(f'\nDate        Time   Grade')
		hist_lines = [f'{date} {time:5d} {grade:7d}' for date, time, grade in args.card.history]
		print('\n'.join(hist_lines))
	else:
		due_cards = browser.filter(col, due_date_end=study_day)
		print(f'{len(col)} cards total')
		print(f'{len(due_cards)} cards due today')
def edit(args):
	if args.card:
		args.card.edit()
		return
	vim_cmd = ['vim',decks_path] 
	vim_cmd += [f'+{args.deck.idx+1}'] if args.deck else []
	vim_cmd += ['-Nu',decks_vimrc]
	vim_cmd += ['-c',f'set dictionary={tags_path}']
	run(vim_cmd)
def delete(args):
	if args.deck:
		decklist.delete(args.deck)
	if args.card:
		args.card.delete()
arg_dict = {'a':add,
	    'A':add_many,
	    'e':edit,
	    'x':delete,
	    's':study,
	    'S':statistics,
	    '1':line_add}
		

# deck manipulation
def list_decks(args):
	for i in range(len(decklist)):
		deck = decklist[i]
		print(deck.idx, deck)
def visual_decks(args):
	n = len(decklist)
	selected = 0
	run(['tput','civis'])
	print('\n'*(n-1)) # move cursor down n lines
	while True:
		for i in range(n):
			run(['tput','cuu1']) # move up n lines
		for i in range(n):
			# print the decks with the selected deck highlighted
			if i == selected:
				run(['tput','smso'])
			print(decklist[i])
			if i == selected:
				run(['tput','sgr0'])
		#get key
		k = readchar.readchar()
		if k == 'j' and selected < n - 1:
			selected += 1
		if k == 'k' and selected > 0:
			selected -= 1
		if k == 'q' or k == readchar.key.ESC:
			run(['tput','cvvis'])
			exit(0)
			break
		if k in arg_dict.keys():
			# erase the menu
			for i in range(n):
				run(['tput','cuu1']) # move up n lines
				run(['tput','el']) # and clear them as we go
			# make cursor visible
			run(['tput','cvvis'])
			# select the selected deck
			args.deck = decklist[selected]
			# the key sets the same variable as that option normally would
			cmd = arg_dict[k]
			cmd(args)
			break
def query(args):
	matches = browser.search(col, args.pattern)
	for card, hit in matches:
		print(f'{card.id:<4} {hit[:50]}')
def visual_query(args):
	matches = browser.search(col, args.pattern)
	if not matches:
		print('No matches.')
		exit(0)
	n = len(matches)
	selected = 0
	run(['tput','civis'])
	print('\n'*(n-1)) # move down n lines
	while True:
		for i in range(n):
			run(['tput','cuu1']) # move up n lines
		for i,(card,hit) in enumerate(matches):
			if i == selected:
				run(['tput','smso']) # standout attribute
			print(f'{hit[:50]}')
			if i == selected:
				run(['tput','sgr0']) # normal attribute
		#get key
		k = readchar.readchar()
		if k == 'j' and selected < n - 1:
			selected += 1
		if k == 'k' and selected > 0:
			selected -= 1
		if k == 'q' or k == readchar.key.ESC:
			run(['tput','cvvis'])
			exit(0)
			break
		if k in arg_dict.keys():
			for i in range(n):
				run(['tput','cuu1']) # move up n lines
				run(['tput','el']) # and clear them as we go
			run(['tput','cvvis'])
			args.card = matches[selected][0]
			cmd = arg_dict[k]
			cmd(args)
			break

def purge(args):
	for card in col:
		if card.deletedQ:
			rmtree(card.path)	
# backup
def backup(args):
	copytree(cards_path, args.small_backup)
def import_collection(args):
	rmtree(cards_path)
	copytree(args.import_path, cards_path)
