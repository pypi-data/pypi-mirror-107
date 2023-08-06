import importlib

def edit(card, mode):
	m = importlib.import_module('.' + card.editor, package = 'vinca.editors')
	return m.edit(card, mode)
