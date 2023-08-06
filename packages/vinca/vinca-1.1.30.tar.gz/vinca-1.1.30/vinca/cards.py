#imports
import curses
import cursor

import string
import datetime
import os
import shutil
from pathlib import Path

from . import reviewers, editors, schedulers 
from . import browser

vinca_path = Path(__file__).parent  # /path/to/vinca
cards_path = vinca_path / 'cards'
decks_file = vinca_path / 'decks.txt'
tags_file = vinca_path / 'tags.txt'

class Deck:
	def __init__(self,name,
	tags_include=[], tags_exclude=[], tags_create=[], idx=None):
		self.name = name
		self.tags_include = tags_include
		self.tags_exclude = tags_exclude
		self.tags_create = tags_create
		self.idx = idx
	def __str__(self):
		l = [f'{self.idx}  ']
		l += [f'{self.name:20s}']
		l += ['+' + t for t in self.tags_include]
		l += ['-' + t for t in self.tags_exclude]
		l += ['=' + t for t in self.tags_create]
		return ' '.join(l)

class Card:
	def __init__(self, cid=None, create=False):
		if not create:
			assert cid and type(cid)==int
			self.id = cid
			self.path = cards_path/str(cid)
			assert self.path.exists()
		elif create:
			old_cids = [int(x.name) for x in cards_path.iterdir()]
			self.id = max(old_cids) + 1 if old_cids else 1 
			self.path = cards_path/str(self.id)
			self.path.mkdir()
			self.make_metadata()

	def make_metadata(self):
		for f in ['history','due_date','tags','config']:
			(self.path/f).touch()

	def make_config(self, editor, reviewer, scheduler):
		(self.path/'config').write_text(f'{editor} {reviewer} {scheduler}')

	def set_due_date(self, date):
		assert type(date)==datetime.date or date in ['deleted','suspended']
		(self.path/'due_date').write_text(str(date))

	def add_tag(self, tag):
		tags = self.tags | {tag}
		(self.path/'tags').write_text(' '.join(tags))

	def remove_tag(self, tag):
		tags = self.tags - {tag}
		(self.path/'tags').write_text(' '.join(self.tags))

	def add_history(self, date, time, grade):
		assert type(date) == datetime.date
		assert type(grade) == int and type(time) == int
		with (self.path/'history').open('a') as f:
			f.write(f'{date} {time} {grade}\n')

	def undo_history(self):
		new_history = self.history[:-1]
		(self.path/'history').open('r+').truncate() # clear the history
		for date, time, grade in new_history:
			self.add_history(date, time, grade) 
			

	def auxfile(self, filename, mode='r'):
		# aux file stands for auxilliary file
		# this is the interface for all file manipulation
		assert filename in self.auxfiles
		return (self.path/filename).open(mode)

	def make_auxfile(self, filename):
		(self.path/filename).touch()

	def review(self, mode='review'):
		return reviewers.review(self, mode) 

	def edit(self, mode='e'):
		return editors.edit(self, mode) 

	def schedule(self):
		return schedulers.schedule(self) 

	def delete(self):
		self.set_due_date('deleted')

	@property
	def auxfiles(self):
		return [f.name for f in self.path.iterdir() if f.name not in ['tags','config','due_date','history']]

	# functools.cached_property could speed this up
	# the add and undo history commands would call an update
	@property
	def history(self):
		# read the history file into a list of entries of
		with open(f'{self.path}/history') as f:
			history = []
			for line in f.readlines():
				date, time, grade = line.split()
				date = datetime.date.fromisoformat(date)
				time, grade = int(time), int(grade)
				history.append((date, time, grade))
			return history

	@property
	def tags(self):
		return set((self.path/'tags').read_text().split())

	@property
	def due_date(self):
		dd = (self.path/'due_date').read_text()
		if dd in ['deleted', 'suspended']:
			return dd
		year, month, day = [int(x) for x in dd.split('-')]
		return datetime.date(year, month, day)

	@property
	def create_date(self):
		return self.history[0][0]
	@property
	def last_date(self):
		return self.history[-1][0]
	@property
	def last_grade(self):
		return self.history[-1][2]
	@property
	def last_interval(self):
		return self.history[-1][0] - self.history[-2][0]  

	@property
	def newQ(self):
		return len(self.history) == 1
	@property
	def deletedQ(self):
		return self.due_date == 'deleted'
	@property
	def suspendedQ(self):
		return self.due_date == 'suspended'

	@property
	def editor(self):
		editor, reviewer, scheduler = (self.path/'config').read_text().split()
		return editor
	@property
	def reviewer(self):
		editor, reviewer, scheduler = (self.path/'config').read_text().split()
		return reviewer
	@property
	def scheduler(self):
		editor, reviewer, scheduler = (self.path/'config').read_text().split()
		return scheduler

class Collection(list):
	def __init__(self):
		list.__init__(self)
		for card_path in cards_path.iterdir():
			cid = int(card_path.name)
			self.append(Card(cid))

	def add_card(self, cid):
		card = Card(cid)
		self.append(card)

	def cache_tags(self):
		tags = set()
		for card in self:
			tags |= card.tags
		tags_file.write_text('\n'.join(tags))
		


class Decklist(dict):
	def __init__(self):
		dict.__init__(self)
		lines = decks_file.read_text().splitlines()
		for i,line in enumerate(lines):
			name, *tags = line.split()
			include = [t[1:] for t in tags if t[0]=='+']
			exclude = [t[1:] for t in tags if t[0]=='-']
			create = [t[1:] for t in tags if t[0]=='=']

			deck = Deck(name,include,exclude,create,i)
			self[name] = deck
			self[i] = deck
	def __len__(self):
		return dict.__len__(self) // 2

	def delete(self, deck):
		del_idx = deck.idx
		l = [str(self[i]) for i in range(len(self)) if i != del_idx]
		decks_file.write_text('\n'.join(l))


