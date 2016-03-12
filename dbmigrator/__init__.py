# -*- coding: utf-8 -*-

import logging
import sys

logger = logging.getLogger('dbmigrator')
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(name)s (%(filename)s) - %(message)s'))
logger.addHandler(handler)


__all__ = ('logger',)
