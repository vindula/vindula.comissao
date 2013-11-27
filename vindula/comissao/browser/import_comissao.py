# coding: utf-8
from five import grok
from zope.interface import Interface
from Products.statusmessages.interfaces import IStatusMessage

from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from vindula.comissao.tools import convert_csv2list_dict, convert_str2int,\
								   convert_str2decimal, convert_str2unicode, convert_str2date, convert_str2bool

from vindula.comissao import MessageFactory as _
from vindula.comissao.models.comissao_usuario import ComissaoUsuario
from vindula.comissao.models.comissao_venda import ComissaoVenda
from vindula.comissao.models.comissao_adicional import ComissaoAdicional

import transaction

grok.templatedir('templates')

class ImportComissaoView(grok.View):
	grok.context(Interface)
	grok.require('cmf.ManagePortal')
	grok.name('importar-comissao')

	def update(self):
		self.retorno_import = 0
		form = self.request.form

		if 'txt_file' in form.keys():
			file_import = form.get('txt_file','')

			if file_import and 'importa_usuario' in form.keys():            
				rows = file_import.readlines()
				# rows = texto #.replace('\r','').replace('\x1b2','')

				self.retorno_import =  self.import_usuarios(rows)

			elif file_import and 'importa_venda' in form.keys():            
				rows = file_import.readlines()
				# rows = texto.replace('\r','').replace('\x1b2','')

				self.retorno_import =  self.import_vendas(rows)
			
			elif not file_import:  
				IStatusMessage(self.request).addStatusMessage(_(u'Adicione o arquivo a ser importado.'),"error")

			if self.retorno_import:
				IStatusMessage(self.request).addStatusMessage(_(u'Forão importados %s registros.'% self.retorno_import ),"info")				

		elif 'sequencia' in form.keys():
			sequencia = int(form.get('sequencia','0'))
			if sequencia and 'remove_usuario' in form.keys():
				ComissaoUsuario().remove_sequencia_usuario(sequencia)
				IStatusMessage(self.request).addStatusMessage(_(u'Foi removido com sucesso o bloco'),"info")

			elif sequencia and 'remove_venda' in form.keys():
				ComissaoVenda().remove_sequencia_venda(sequencia)
				IStatusMessage(self.request).addStatusMessage(_(u'Foi removido com sucesso o bloco'),"info")

		elif 'regras_gerais' in form.keys():
			regras_gerais = form.get('text_regras_gerais','')
			
			settings_comissao = self.get_register_regras_gerais()
			settings_comissao.value = unicode(regras_gerais, 'utf-8')
			
			transaction.commit()

			IStatusMessage(self.request).addStatusMessage(_(u'As regras gerais foram salvas com sucesso.'),"info")


		elif 'regras_validacao' in form.keys():
			regras_validacao = form.get('text_regras_validacao','')

			settings_comissao = self.get_register_regras_validacao()
			settings_comissao.value = unicode(regras_validacao, 'utf-8')

			transaction.commit()

			IStatusMessage(self.request).addStatusMessage(_(u'As regras de validação gerais foram salvas com sucesso.'),"info")


		elif 'titulo_comissao' in form.keys():
			titulo_comissao = form.get('text_titulo_comissao','')

			settings_comissao = self.get_register_titulo()
			settings_comissao.value = unicode(titulo_comissao, 'utf-8')

			transaction.commit()

			IStatusMessage(self.request).addStatusMessage(_(u'O Titulo do extrato foi salvo com sucesso.'),"info")

		
	def list_import_venda(self):
		return ComissaoVenda().get_bloco_importacao_venda()


	def list_import_usuario(self):
		return ComissaoUsuario().get_bloco_importacao_comissao()
		

	def get_register_regras_gerais(self):
		registry = getUtility(IRegistry)
		try:
			settings_comissao = registry.records['vindula.comissao.register.interfaces.IVindulaComissao.regras_comissoes']
		except:
			settings_comissao = False		

		return settings_comissao

	def get_register_regras_validacao(self):
		registry = getUtility(IRegistry)
		try:
			settings_comissao = registry.records['vindula.comissao.register.interfaces.IVindulaComissao.validacao_comissoes']
		except:
			settings_comissao = False		

		return settings_comissao

	def get_register_titulo(self):
		registry = getUtility(IRegistry)
		try:
			settings_comissao = registry.records['vindula.comissao.register.interfaces.IVindulaComissao.titulo_comissoes']
		except:
			settings_comissao = False		

		return settings_comissao

	def get_titulo_comissao(self):
		settings_comissao = self.get_register_titulo()

		if settings_comissao:
			return settings_comissao.value
		else:
			return ""


	def get_regras_gerais(self):
		settings_comissao = self.get_register_regras_gerais()

		if settings_comissao:
			return settings_comissao.value
		else:
			return ""

	def get_regras_validacao(self):
		settings_comissao = self.get_register_regras_validacao()

		if settings_comissao:
			return settings_comissao.value
		else:
			return ""



	def import_usuarios(self,rows):
		dados_import = convert_csv2list_dict(rows)
		sequencia = ComissaoUsuario().next_sequencia()
		cont = 0

		for dados in dados_import:

			D = {'ci':convert_str2unicode(dados.get('CI', '')),
				 'cpf':convert_str2unicode(dados.get('CPF','')),
				 'name':convert_str2unicode(dados.get('Nome','')),
				 'pv_bonus': convert_str2int(dados.get('Bonus','0')),
				 'pv_mensal': convert_str2int(dados.get('Mensal','')),
				 'pv_total': convert_str2int(dados.get('Total','')),
				 'pv_meta': convert_str2unicode(dados.get('Meta','')),
				 'valor_inicial': convert_str2decimal(dados.get('Valor Inicial','')),
				 'me_porcentagem': convert_str2int(dados.get('Meta Porcentagem','0').replace('%','')),
				 'equipe': convert_str2unicode(dados.get('Equipe','')),
				 'valor_final': convert_str2decimal(dados.get('V. Final','0')),
				 'competencia': convert_str2unicode(dados.get('Competencia')),
				 'sequencia': sequencia,
				}

			if dados.get('Meta Equipe')=='Sim':
				D['me_meta'] = True
			else:
				D['me_meta'] = False

			id_usuario = ComissaoUsuario().manage_comissao_usuario(**D)
			E = {}
			for adicional in dados.keys():
				if 'Adicional' in adicional:
					# import pdb;pdb.set_trace()
					
					if len(E.keys()) == 5:
						# ComissaoAdicional().manage_comissao_adicional(**E)
						E = {}

					E['id_usuario'] = id_usuario
				
					adicional_s = adicional.split('-')
					adicional_v = dados.get(adicional,'')

					if adicional_s[0] == 'Item':
						if not 'dict_itens' in E.keys():
							E['dict_itens']	= ''
							
						E['dict_itens'] += u"%s:%s|" %(adicional_s[1],adicional_v)


					E['valor'] = convert_str2decimal(dados.get('Valor-Adicional-'+adicional_s[-1]))

					valor_direito = dados.get('Direito-Adicional-'+adicional_s[-1])
					if valor_direito == "SIM":
						E['direito'] = True
					else:
						E['direito'] = False

					E['name'] = convert_str2unicode(dados.get('Nome-Adicional-'+adicional_s[-1]))

			cont += 1

		return cont

	def import_vendas(self, rows):
		sequencia = ComissaoVenda().next_sequencia()
		dados_import = convert_csv2list_dict(rows)
		cont = 0

		for dados in dados_import:

			D = {'ci_usuario': convert_str2unicode(dados.get('Agente')),
				 'competencia': convert_str2unicode(dados.get('Competencia')),
				 'nr_proposta': convert_str2unicode(dados.get('nro_proposta')),
				 'nome_cliente': convert_str2unicode(dados.get('Nome_Cliente','')),
				 'cpf': convert_str2unicode(dados.get('CPF','')),
				 'data_atd': convert_str2date(dados.get('Data_ATD','')),
				 'situacao': convert_str2unicode(dados.get('Situação')),
				 'situacao_financeiro': convert_str2unicode(dados.get('Situação Financeiro','')),
				 'pontos': convert_str2int(dados.get('Pontuação Comissões','')),
				 'sequencia': sequencia,
				 'aprovado' : convert_str2bool(dados.get('Aprovado',''))
				}

			if dados.get('Status Vendas') == 'Vendas Validas':
				D['status'] = True
			else:
				D['status'] = False

	 		ComissaoVenda().manage_comissao_venda(**D)
	 		cont += 1

	 	return cont
