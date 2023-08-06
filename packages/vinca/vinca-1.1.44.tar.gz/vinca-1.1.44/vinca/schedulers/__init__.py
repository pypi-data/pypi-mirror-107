import importlib

def schedule(card):

	if card.last_grade == -1:
		card.set_due_date('deleted')
		return 0
	elif card.last_grade == -2:
		card.set_due_date('suspended')
		return 0

	# import the specific scheduler module
	m = importlib.import_module('.' + card.scheduler, package = 'vinca.schedulers')
	# invoke the specific scheduler
	return m.schedule(card)
