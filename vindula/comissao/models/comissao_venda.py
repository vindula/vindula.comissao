# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from vindula.comissao.models import ComissaoBase

# from vindula.comissao.models.comissao_usuario import ComissaoUsuario

from vindula.comissao.models.comissao_validacao import ComissaoValidacao
 
class ComissaoVenda(Storm, ComissaoBase):
	__storm_table__ = 'vin_comissao_venda'

	id = Int(primary=True)
	sequencia = Int()
	ci_usuario = Unicode()
	nr_proposta = Unicode()
	nome_cliente = Unicode()
	competencia = Unicode()
	cpf = Unicode()
	data_atd = Date()
	situacao = Unicode()
	situacao_financeiro = Unicode()
	status = Bool()
	pontos = Int()
	aprovado = Bool()
	# comissao_usuario_id = Int()
	deleted = Bool()
	date_created = DateTime()
	date_modified = DateTime()

	# comissao_usuario = Reference(comissao_usuario_id, "ComissaoUsuario.id")

	def next_sequencia(self):
		numero_atual = self.store.find(ComissaoVenda).max(ComissaoVenda.sequencia) or 0
		return numero_atual + 1
	
	@property
	def is_venda_validada(self):
		data = ComissaoVenda().store.find(ComissaoValidacao, ComissaoValidacao.id_venda==self.id)
		if data.count() >= 1:
			return True

		return False


	def manage_comissao_venda(self, **kwargs):
		ci_usuario = kwargs.get('ci_usuario')
		competencia = kwargs.get('competencia') 		
		nr_proposta = kwargs.get('nr_proposta') 

		data_venda = self.store.find(ComissaoVenda,
				 				     ComissaoVenda.ci_usuario==ci_usuario,
		   							 ComissaoVenda.competencia==competencia,
									 ComissaoVenda.nr_proposta==nr_proposta).one()

		if data_venda:
			if not data_venda.is_venda_validada:
				#Marcando como deletada a venda importada anteriormente
				data_venda.deleted = True
				self.store.flush()

				#adicionando a nova Importação
				comissao_venda = ComissaoVenda(**kwargs)
				self.store.add(comissao_venda)
				self.store.flush()

		else:
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

