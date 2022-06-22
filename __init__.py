try:
    from src import (Rule34Paheal, Logger, load, Luscious)
except ImportError:
    from .src import (Rule34Paheal, Logger, load, Luscious)
    

__all__ = [Rule34Paheal, Logger, load, Luscious]
