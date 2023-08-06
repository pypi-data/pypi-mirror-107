import argparse
from . import cards
from pathlib import Path
collection = cards.Collection()
decklist = cards.Decklist()

# type checking
def deck_type(arg):
	if arg.isdigit(): arg = int(arg)
	if arg in decklist.keys():
		return cards.Deck(arg)
	raise argparse.ArgumentTypeError('\n\nThat is not a deck. Use [-d] to list decks')
def card_type(arg):
	if arg.isdigit(): arg = int(arg)
	if arg in [card.id for card in collection]:
		return cards.Card(arg) 
	raise argparse.ArgumentTypeError('\n\nThat is not a valid card id. Use [-q] to search for a card id.')
def deck_or_card(arg):
	if arg.isdigit(): arg = int(arg)
	if arg in decklist.keys():
		return cards.Deck(arg)
	if arg in [card.id for card in collection]:
		return cards.Card(arg) 
	raise argparse.ArgumentTypeError('\n\nThat is neither a deck nor a card.\n' + 
					 'Valid arguments are: \n' +
					 '1) A deck name \n' +
					 '2) A deck id (d will list deck ids) \n' +
					 '3) A card id (use q to search for a car id)')

# argument parsing
parser = argparse.ArgumentParser()
parser.set_defaults(deck = None, card = None, deck_or_card = None, func = 'statistics')
subparsers = parser.add_subparsers()
# commands which take a deck as an argument
line_add_parser = subparsers.add_parser('line_add',aliases=['1'], help='add a basic card quickly')
line_add_parser.add_argument('deck',type=deck_type,nargs='?')
line_add_parser.set_defaults(func = 'line_add')

add_parser = subparsers.add_parser('add',aliases=['a'], help='add a basic card')
add_parser.add_argument('deck',type=deck_type,nargs='?')
add_parser.set_defaults(func = 'add')

image_cloze_parser = subparsers.add_parser('image_cloze',aliases=['ic'], help='generate an image cloze card')
image_cloze_parser.add_argument('image_path',type=Path)
image_cloze_parser.set_defaults(func = 'image_cloze')

query_parser = subparsers.add_parser('query',aliases=['q'], help='search collection for regexp')
query_parser.add_argument('pattern',nargs='?',default='.')
query_parser.set_defaults(func = 'query')
# TODO miscellaneous filter options (due_date/studied_time/creation_date/deleted) for the query
visual_query_parser = subparsers.add_parser('visual_query',aliases=['vq'], help='search collection for regexp and perform a command on the selected card')
visual_query_parser.add_argument('pattern',nargs='?',default='.')
visual_query_parser.set_defaults(func = 'visual_query')
# commands which take a deck or several cards as an argument 
study_parser = subparsers.add_parser('study',aliases=['s'], help='study the collection or selected deck')
study_parser.add_argument('deck_or_card', type=deck_or_card, nargs='*')
study_parser.add_argument('--date', type=int, help='study as if today was [date]')
study_parser.set_defaults(func = 'study')
statistics_parser = subparsers.add_parser('statistics',aliases=['S'], help='statistics about the selected deck or card')
statistics_parser.add_argument('deck_or_card', type=deck_or_card, nargs='*')
statistics_parser.set_defaults(func = 'statistics')
# TODO miscellaneous options for more advanced statistics
edit_parser = subparsers.add_parser('edit',aliases=['e'], help='edit the selected deck or card')
edit_parser.add_argument('deck_or_card',type=deck_or_card,nargs='?')
edit_parser.set_defaults(func = 'edit')
delete_parser = subparsers.add_parser('delete',aliases=['x'], help='delete the selected deck or card')
delete_parser.add_argument('deck_or_card',type=deck_or_card)
delete_parser.set_defaults(func = 'delete')
# commands which take no arguments
list_decks_parser = subparsers.add_parser('list_decks',aliases=['d'], help='list decks')
list_decks_parser.set_defaults(func = 'list_decks')
visual_decks_parser = subparsers.add_parser('visual_decks',aliases=['vd'], help='select a deck and perform a command on it')
visual_decks_parser.set_defaults(func = 'visual_decks')
purge_parser = subparsers.add_parser('purge',aliases=['p'], help='permanently delete all cards scheduled for deletion')
purge_parser.set_defaults(func = 'purge')
# commands which take a path as an argument (import / backup)
backup_parser = subparsers.add_parser('backup',aliases=['b'], help='backup all cards')
backup_parser.add_argument('backup_dest',type=Path)
backup_parser.set_defaults(func = 'backup')
# TODO allow for selective export (e.g. we could query, get the first field, and pipe to export)
import_parser = subparsers.add_parser('import',aliases=['i'], help='import a collection of cards')
import_parser.add_argument('import_dest',type=Path)
import_parser.add_argument('-o','--overwrite',action='store_true',help='overwrite the existing collection')
import_parser.set_defaults(func = 'import_collection')
#
args = parser.parse_args()
args.card = args.deck_or_card if type(args.deck_or_card) is cards.Card else args.card
args.deck = args.deck_or_card if type(args.deck_or_card) is cards.Deck else args.deck

