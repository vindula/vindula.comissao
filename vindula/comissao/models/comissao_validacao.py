# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from vindula.comissao.models import ComissaoBase

 
class ComissaoValidacao(Storm,ComissaoBase):
	__storm_table__ = 'vin_comissao_validacao'

	id = Int(primary=True)
	username = Unicode()
	cpf = Unicode()
	competencia = Unicode()

	id_venda = Int()
	id_usuario = Int()

	date_created = DateTime()



	def manage_comissao_validacao(self, **kwargs):

		comissao_validacao = ComissaoValidacao(**kwargs)
		self.store.add(comissao_validacao)
		self.store.flush()

	# def get_comissao_isValid(self,cpf,competencia,sequencia,tipo_sequencia):

	# 	data = self.store.find(ComissaoValidacao, ComissaoValidacao.cpf==cpf,
	# 											  ComissaoValidacao.competencia==competencia)

	# 	# if tipo_sequencia == 'venda':
	# 	# 	data = data.find(ComissaoValidacao.sequencia_venda==sequencia)

	# 	# elif tipo_sequencia == 'usuario':
	# 	# 	data = data.find(ComissaoValidacao.sequencia_usuario==sequencia)

	# 	if data.count() >= 1:
	# 		return True

	# 	return False
