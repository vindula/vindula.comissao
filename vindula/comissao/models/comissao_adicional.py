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

	@property
	def head(self):
		dados = self.dict_itens
		L = []
		for i in dados.split('|'):
			if i: L.append(i.split(':')[0])
		return L
	
	@property
	def values(self):
		dados = self.dict_itens
		L = []
		for i in dados.split('|'):
			if i: L.append(i.split(':')[-1])
		return L

	@property
	def cont(self):
		return len(self.values)

	
	def manage_comissao_adicional(self,id_usuario,list_adicional):

		for adicional in list_adicional:
			adicional['id_usuario'] = id_usuario

			comissao_adicional = ComissaoAdicional(**adicional)
			self.store.add(comissao_adicional)
			self.store.flush()



