# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from vindula.comissao.models import ComissaoBase
from vindula.comissao.models.comissao_venda import ComissaoVenda
from vindula.comissao.models.comissao_validacao import ComissaoValidacao
from vindula.comissao.models.comissao_adicional import ComissaoAdicional

from datetime import date
 
class ComissaoUsuario(Storm,ComissaoBase):
	__storm_table__ = 'vin_comissao_usuario'

	id = Int(primary=True)
	ci = Unicode()
	cpf = Unicode()
	name = Unicode()
	pv_bonus = Int()
	pv_mensal = Int()
	pv_total = Decimal()
	pv_meta = Unicode()
	valor_inicial = Decimal()
	me_meta = Bool()
	me_porcentagem = Int()
	equipe = Unicode()
	valor_final = Decimal()
	competencia = Unicode()
	sequencia = Int()

	# faltas = Int()
	# atrasos = Int()
	# adicional1 = Decimal()
	# head_shot = Int()
	# adicional2 = Decimal()
	# bv_porcentagem = Int()
	# adicional3 = Decimal()
	# q_proposta = Int()
	# media_dia = Int()
	# adicional4 = Decimal()
	# ticket = Int()
	# adicional5 = Decimal()
	
	deleted = Bool()
	date_created = DateTime()
	date_modified = DateTime()

	adicionais = ReferenceSet(id, "ComissaoAdicional.id_usuario")


	@property
	def vendas(self):
		# sequencia_atual = ComissaoVenda().store.find(ComissaoVenda,
		# 										 	 ComissaoVenda.competencia==self.competencia).max(ComissaoVenda.sequencia) or 0
		comissao = ComissaoVenda().store.find(ComissaoVenda, ComissaoVenda.ci_usuario==self.ci,
											  ComissaoVenda.competencia==self.competencia,
											  # ComissaoVenda.sequencia==sequencia_atual
											  ComissaoVenda.deleted==False).order_by(ComissaoVenda.data_atd)
		return comissao

	@property
	def vendas_validas(self):
		valido = self.vendas.find(status=True)
		return valido

	@property
	def vendas_invalidas(self):
		invalido = self.vendas.find(status=False)
		return invalido


	@property
	def cont_vendas_validas(self):
		return self.vendas_validas.count()


	@property
	def cont_vendas_invalidas(self):
		return self.vendas_invalidas.count()

	@property
	def is_usuario_validada(self):
		data = ComissaoVenda().store.find(ComissaoValidacao, ComissaoValidacao.id_venda==self.id)
		if data.count() >= 1:
			return True

		return False


	def next_sequencia(self):
		numero_atual = self.store.find(ComissaoUsuario).max(ComissaoUsuario.sequencia) or 0
		return numero_atual + 1

	def remove_sequencia_usuario(self, sequencia):
		results = self.store.find(ComissaoUsuario, ComissaoUsuario.sequencia==sequencia)

		if results.count() > 0:
			for result in results:
				self.store.remove(result)
				self.store.flush()

	def manage_comissao_usuario(self, **kwargs):
		list_adicional = []
		cont_adicional = kwargs.pop('cont_adicional')
		import_adicional = False

		
		for index_adicional in range(1,cont_adicional+1):
			list_adicional.append(kwargs.pop('adicional'+str(index_adicional)))

		data_usuario = self.store.find(ComissaoUsuario,
				 				       ComissaoUsuario.ci==kwargs.get('ci'),
		   							   ComissaoUsuario.competencia==kwargs.get('competencia'),
									   ComissaoUsuario.cpf==kwargs.get('cpf'),
										ComissaoUsuario.deleted==False
									   ).one()

		if data_usuario:
			if not data_usuario.is_usuario_validada:
				#Marcando como deletada a  comissão do usuario importada anteriormente
				data_usuario.deleted = True
				self.store.flush()

				#adicionando a nova Importação
				comissao_usuario = ComissaoUsuario(**kwargs)
				self.store.add(comissao_usuario)
				self.store.flush()
				import_adicional = True
		else:
			comissao_usuario = ComissaoUsuario(**kwargs)
			self.store.add(comissao_usuario)
			self.store.flush()
			import_adicional = True

		if import_adicional:
			id_usuario = comissao_usuario.id
			ComissaoAdicional().manage_comissao_adicional(id_usuario,list_adicional)



	def get_comissao_by_cpf(self, cpf_user):
		data = self.store.find(ComissaoUsuario,
							   ComissaoUsuario.cpf==cpf_user,
							   ComissaoUsuario.deleted==False
							   ).order_by(ComissaoUsuario.competencia)
		return data


	def get_bloco_importacao_comissao(self):
		select = Select(ComissaoUsuario.sequencia,
						distinct=True)

		data = self.store.execute(select)
		L = []
		for item in data:
			tmp = self.store.find(ComissaoUsuario, ComissaoUsuario.sequencia==item[0]).any()
			if tmp:
				L.append(tmp)

		return L

	def get_comisoes_byCompetencia(self,competencia):
		last_sequencia = self.next_sequencia() - 1

		data = self.store.find(ComissaoUsuario,
							   ComissaoUsuario.competencia==competencia,
							   ComissaoUsuario.sequencia==last_sequencia).order_by(ComissaoUsuario.name)
		return data

	def get_comissoes_lastCompetencia(self):
		data = date.today()
		competencia_atual = u'%s/%s' %(data.month,data.year)

		last_competencia = self.store.find(ComissaoUsuario).max(ComissaoVenda.competencia) or competencia_atual

		return self.get_comisoes_byCompetencia(last_competencia)

