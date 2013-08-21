# coding: utf-8


#Imports regarding the connection of the database 'strom'
from storm.locals import *
from vindula.comissao.models import ComissaoBase

 
class ComissaoUsuario(Storm,ComissaoBase):
	__storm_table__ = 'vin_comissao_usuario'

	id = Int(primary=True)
	ci = Unicode()
	cpf = Unicode()
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
	faltas = Int()
	atrasos = Int()
	adicional1 = Decimal()
	head_shot = Int()
	adicional2 = Decimal()
	bv_porcentagem = Int()
	adicional3 = Decimal()
	q_proposta = Int()
	media_dia = Int()
	adicional4 = Decimal()
	ticket = Int()
	adicional5 = Decimal()

	date_created = DateTime()
	date_modified = DateTime()

	# vendas = ReferenceSet(id, "ComissaoVenda.comissao_usuario_id")

	@property
	def vendas(self):
		sequencia_atual = self.store.find(ComissaoVenda).max(ComissaoVenda.sequencia) or 0
		comissao = self.store.find(ComissaoVenda, ComissaoVenda.ci_usuario==self.ci,
												  ComissaoVenda.competencia==self.competencia,
												  ComissaoVenda.sequencia==sequencia_atual).order_by(ComissaoVenda.data_atd)
		return comissao

	@property
	def vendas_validas(self):
		valido = self.vendas.find(status=True)
		return valido

	@property
	def vendas_invalidas(self):
		invalido = self.vendas.find(status=False)
		return invalido

	def next_sequencia(self):
		numero_atual = self.store.find(ComissaoUsuario).max(ComissaoUsuario.sequencia) or 0
		return numero_atual + 1

	def manage_comissao_usuario(self, **kwargs):
		# competencia = kwargs.get('competencia') 		

		# data = self.store.find(ComissaoUsuario,
		# 					   ComissaoUsuario.cpf==cpf_user,
		#    					   ComissaoUsuario.competencia==competencia).one()

		# if data:
		# 	for attribute, value in kwargs.items():
		# 		setattr(self,attribute,value)

		# 	self.store.flush()
		# else:
		

		comissao_usuario = ComissaoUsuario(**kwargs)
		self.store.add(comissao_usuario)
		self.store.flush()


	def get_comissao_by_cpf(self, cpf_user):
		data = self.store.find(ComissaoUsuario,
							   ComissaoUsuario.cpf==cpf_user).order_by(ComissaoUsuario.competencia)
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

