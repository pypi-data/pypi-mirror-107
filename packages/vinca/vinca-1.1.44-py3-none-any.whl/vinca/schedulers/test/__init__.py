# A dummy scheduler that always schedules for the next day
import datetime

def schedule(card):
	
	last_seen = card.history[-1][0]
	# [-1] means most recent entry in history
	# [-1][0] means to get the date (each entry is date, difficulty)

	# test interval is one day
	interval = datetime.timedelta(days=1)

	due_date = last_seen + interval

	card.set_due_date(due_date)

	# indicate that it is not necessary to review this card again today by putting it in the queue
	return 0

