# coding: utf-8

from vindula.myvindula.models.base import BaseStore
from datetime import datetime

class ComissaoBase(BaseStore):

	def __init__(self, *args, **kwargs):
		super(ComissaoBase,self).__init__(*args, **kwargs)

		self.date_created = datetime.now()
		self.date_modified = datetime.now()
