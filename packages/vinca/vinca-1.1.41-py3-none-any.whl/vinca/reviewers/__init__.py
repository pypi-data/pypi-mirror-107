import importlib

def review(card, mode):
	m = importlib.import_module('.'+card.reviewer, package = 'vinca.reviewers')
	return m.review(card, mode)
