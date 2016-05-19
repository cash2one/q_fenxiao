#encoding:utf-8
__author__ = 'binpo'

from base_handler import BaseHandler
from utils.card_check import checkIdcard
class CardCheckHandler(BaseHandler):
    def get(self):
        card = self.get_argument('card')
        card = card.strip()
        self.write(checkIdcard(card))


