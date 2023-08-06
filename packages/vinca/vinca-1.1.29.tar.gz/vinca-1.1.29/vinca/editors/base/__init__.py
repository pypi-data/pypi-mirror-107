# this is the base editor for creation of simple front/back plaintext cards
# TODO no filename
#      no buffer titles
#      no tildes
import subprocess
from pathlib import Path

path = Path(__file__).parent #  '/home/oscar/vinka/editors/base/'
vimrc_path = path / '.vimrc'

vimrc_modes = {'a': ['-c', 'startinsert'],
	       'e': [],
	       'f': [],
               'b': ['-c', 'wincmd W'],
               't': ['-c', 'wincmd j']}


def edit(card, mode):
	# possible modes are a, e, f, b
	# they stand for add, edit, front_edit, and back_edit
	implemented_modes = ['a','e','f','b','t']
	if mode not in implemented_modes:
		return

	if mode == 'a':
		card.make_auxfile('front')
		card.make_auxfile('back')

	assert 'front' in card.auxfiles
	assert 'back' in card.auxfiles

	# we are going to run vim...
	vim_cmd = ['vim']
	# to edit the fron and back sides of the cards...
	vim_cmd += ['-o',f'{card.path}/front',
	            f'{card.path}/back',f'{card.path}/tags']
	# using a vimrc file to make a few custom bindings...
	vim_cmd += ['-Nu', vimrc_path]
	# with special options depending on the editing mode.
	vim_cmd += vimrc_modes[mode]
	# launch
	subprocess.run(vim_cmd)
