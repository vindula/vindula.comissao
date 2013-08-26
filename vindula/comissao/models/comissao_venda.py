# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from vindula.comissao.models import ComissaoBase

# from vindula.comissao.models.comissao_usuario import ComissaoUsuario

 
class ComissaoVenda(Storm, ComissaoBase):
	__storm_table__ = 'vin_comissao_venda'

	id = Int(primary=True)
	sequencia = Int()
	ci_usuario = Unicode()
	nome_cliente = Unicode()
	competencia = Unicode()
	cpf = Unicode()
	data_atd = Date()
	situacao = Unicode()
	situacao_financeiro = Unicode()
	status = Bool()
	pontos = Int()
	# comissao_usuario_id = Int()
	date_created = DateTime()
	date_modified = DateTime()

	# comissao_usuario = Reference(comissao_usuario_id, "ComissaoUsuario.id")

	def next_sequencia(self):
		numero_atual = self.store.find(ComissaoVenda).max(ComissaoVenda.sequencia) or 0
		return numero_atual + 1
	
	def manage_comissao_venda(self, **kwargs):
		# ci_usuarioc = kwargs.pop('ci_usuario')
		# competencia = kwargs.pop('competencia') 		

		# data_usuario = self.store.find(ComissaoUsuario,
		# 							   ComissaoUsuario.ci==ci_agente,
		#    							   ComissaoUsuario.competencia==competencia).one()
		

		# if data_usuario:
		# 	comissao_usuario_id = data_usuario.id

		# 	cpf_cliente = kwargs.get('cpf')
		# 	data_atd = kwargs.get('data_atd')
		# 	data = self.store.find(ComissaoVenda,
		# 						   ComissaoVenda.comissao_usuario_id==comissao_usuario_id,
		# 						   ComissaoVenda.cpf==cpf_cliente,
		# 						   ComissaoVenda.data_atd==data_atd).one()
		# 	if data:

		# 		for attribute, value in kwargs.items():
		# 			setattr(self,attribute,value)

		# 		self.store.flush()
		# 	else:
		# 		kwargs['comissao_usuario_id'] = comissao_usuario_id

		comissao_venda = ComissaoVenda(**kwargs)
		self.store.add(comissao_venda)
		self.store.flush()

	def remove_sequencia_venda(self, sequencia):
		results = self.store.find(ComissaoVenda, ComissaoVenda.sequencia==sequencia)

		if results.count() > 0:
			for result in results:
				self.store.remove(result)
				self.store.flush()


	def get_bloco_importacao_venda(self):
		select = Select(ComissaoVenda.sequencia,
						distinct=True)

		data = self.store.execute(select)
		L = []
		for item in data:
			tmp = self.store.find(ComissaoVenda, ComissaoVenda.sequencia==item[0]).any()
			if tmp:
				L.append(tmp)

		return L

