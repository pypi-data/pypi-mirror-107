from . import parsing, functions

args = parsing.args
func = args.func
func = getattr(functions, func)
func(args)
