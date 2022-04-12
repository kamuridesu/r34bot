try:
	from rule34 import Rule34Paheal
	from helpers import Logger
except:
	from .rule34 import Rule34Paheal
	from .helpers import Logger


__all__ = [Rule34Paheal, Logger]