# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from vindula.comissao.models import ComissaoBase


 
class ComissaoAdicional(Storm, ComissaoBase):
	__storm_table__ = 'vin_comissao_adicional'

	id = Int(primary=True)
	name = Unicode()
	direito = Bool()
	valor = Decimal()
	dict_itens = Unicode()
	id_usuario = Int()

	
	def manage_comissao_adicional(self, **kwargs):

		comissao_adicional = ComissaoAdicional(**kwargs)
		self.store.add(comissao_adicional)
		self.store.flush()



