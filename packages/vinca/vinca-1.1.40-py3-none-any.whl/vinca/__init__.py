#!/usr/bin/env python

import vinca
# imports
from pathlib import Path
from subprocess import run
import argparse
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


# type checking
def deck_type(arg):
	try:
		if arg.isdigit(): arg = int(arg)
		return decklist[arg]
	except KeyError:
		raise argparse.ArgumentTypeError('That deck is not in the list. Use [-D] to list decks and [-e] to edit.')
def card_type(arg):
	try:
		cid = int(arg)
		return cards.Card(cid)
	except:
		raise argparse.ArgumentTypeError('That is not a valid card id. Use [-q] to search for a card id.')

# argument parsing
parser = argparse.ArgumentParser(description='VINCA Spaced Repetition System')
# Card and Deck are 'operands'; they can be used in combination with the other options
operands = parser.add_mutually_exclusive_group()
operands.add_argument('-d', '--deck', type=deck_type, help='specify which deck to operate upon')
operands.add_argument('-c', '--card', type=card_type, help='specify which card to operate upon')
# the remaining actions are mutually exclusive
options = parser.add_mutually_exclusive_group()
options.add_argument('-a', '--add', action='store_true', help='add a new card of type basic')
options.add_argument('-A', '--add-many', action='store_true', help='add multiple cards')
options.add_argument('-1', '--line-add', action='store_true', help='write a simple one line card')
options.add_argument('-ic', '--img-cloze', action='store_true', help='add a new card of type image cloze')
options.add_argument('-s', '--study', action='store_true', help='study')
options.add_argument('-S', '--statistics', action='store_true', help='statistics')
options.add_argument('-q', '--query', type=str, metavar='PATTERN', help='query for regex pattern')
options.add_argument('-vq', '--visual-query', type=str, metavar='PATTERN', help='visual query for regex pattern')
options.add_argument('-D', '--decks', action='store_true', help='list decks')
options.add_argument('-vd', '--visual-decks', action='store_true', help='visual list decks')
options.add_argument('-e', '--edit', action='store_true', help='edit the decks file, or specified card (see [-c])')
options.add_argument('-b', '--backup', type=Path, dest='small_backup', metavar='DEST', help='backup all cards to the destination')
options.add_argument('--import', type=Path, dest='import_path', metavar='PATH', help='replace cards folder with a new one')
options.add_argument('-x', '--delete', action='store_true', help='delete the specified card or deck. \n Deleting a deck does not delete its cards.')
# miscellaneous functionality
parser.add_argument('--purge', action='store_true', help='delete all cards slated for deletion')
# options.add_argument('--date', type=int, help='+1 will give cards due tomorrow, -3 will give cards at least three days overdue.')
# TODO filter, simulated-date, import
args = parser.parse_args()

# visual selection
arg_dict = {'a':'add',
	    'A':'add_many',
	    'e':'edit',
	    'x':'delete',
	    's':'study',
	    'S':'statistics',
	    '1':'line_add'}
if args.visual_decks:
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
			setattr(args, arg_dict[k], True) 
			break
		
if args.visual_query:
	matches = browser.search(col, args.visual_query)
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
			setattr(args, arg_dict[k], True) 
			break

# deck manipulation
if args.decks:
	for i in range(len(decklist)):
		print(decklist[i])
if args.edit and not args.card:
	vim_cmd = ['vim',decks_path] 
	vim_cmd += [f'+{args.deck.idx+1}'] if args.deck else []
	vim_cmd += ['-Nu',decks_vimrc]
	vim_cmd += ['-c',f'set dictionary={tags_path}']
	run(vim_cmd)
if args.edit and args.card:
	args.card.edit()

# card creation
if args.line_add:  # add a single card without opening vim
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
def add_basic(deck = None):
	tags_create = deck.tags_create if deck else []	
	new_card = cards.Card(create=True)
	new_card.make_config('base','base','base')
	for tag in tags_create:
		new_card.add_tag(tag)
	new_card.edit(mode='a')  # add mode
	cont = new_card.review(mode='preview')
	return new_card, cont
if args.add:
	new_card, cont = add_basic(args.deck)
	new_card.schedule()
if args.add_many:
	prev_card = None
	while True:	
		new_card, cont = add_basic(args.deck)
		new_card.schedule()
		if cont == -1:
			prev_card.review(mode='preview')  # TODO does not support multilevel
			prev_card.undo_history()  # we do not actually want to change the old card
		if cont == 0:
			break
		if cont == 1:
			prev_card = new_card
if args.study:
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

# statistics
if args.statistics:
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
# search
if args.query:
	matches = browser.search(col, args.query)
	for card, hit in matches:
		print(f'{card.id:<4} {hit[:50]}')
# deletion
if args.delete:
	if args.deck:
		decklist.delete(args.deck)
	if args.card:
		args.card.delete()

# backup
if args.small_backup:
	copytree(cards_path, args.small_backup)
# import
if args.import_path:
	rmtree(cards_path)
	copytree(args.import_path, cards_path)

# miscellaneous
if args.purge:
	for card in col:
		if card.deletedQ:
			rmtree(card.path)	
