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

	def get_regras_gerais(self):
		settings_comissao = self.get_register_regras_gerais()

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
				 'pv_bonus': convert_str2int(dados.get('Bonus','0')),
				 'pv_mensal': convert_str2int(dados.get('Mensal','')),
				 'pv_total': convert_str2int(dados.get('Total','')),
				 'pv_meta': convert_str2unicode(dados.get('Meta','')),
				 'valor_inicial': convert_str2decimal(dados.get('Valor Inicial','')),
				 'me_porcentagem': convert_str2int(dados.get('Meta Porcentagem','0').replace('%','')),
				 'equipe': convert_str2unicode(dados.get('Equipe','')),
				 'valor_final': convert_str2decimal(dados.get('V. Final','0')),

				 'competencia': convert_str2unicode(dados.get('Competencia','')),
				 'faltas': convert_str2int(dados.get('Faltas','0')),
				 'atrasos': convert_str2int(dados.get('Atrasos','0')),
				 'adicional1': convert_str2decimal(dados.get('Adicional 1','0')),
				 'head_shot': convert_str2int(dados.get('Head Shot','0')),
				 'adicional2': convert_str2decimal(dados.get('Adicional 2','0')),
				 'bv_porcentagem': convert_str2int(dados.get('BV Porcentagem','0').replace('%','')),
				 'adicional3': convert_str2decimal(dados.get('Adicional 3','0')),
				 'q_proposta': convert_str2int(dados.get('Q. Proposta','0')),
				 'media_dia': convert_str2int(dados.get('Dias Uteis','0')),
				 'adicional4': convert_str2decimal(dados.get('Adicional 4','0')),
				 'ticket': convert_str2int(dados.get('Tickte','0')),
				 'adicional5': convert_str2decimal(dados.get('Adicional 5','0')),
				 'sequencia': sequencia,

				}

			if dados.get('Meta Equipe')=='Sim':
				D['me_meta'] = True
			else:
				D['me_meta'] = False

			ComissaoUsuario().manage_comissao_usuario(**D)
			cont += 1

		return cont

	def import_vendas(self, rows):
		sequencia = ComissaoVenda().next_sequencia()
		dados_import = convert_csv2list_dict(rows)
		cont = 0

		for dados in dados_import:

			D = {'ci_usuario': convert_str2unicode(dados.get('agente')),
				 'competencia': convert_str2unicode(dados.get('competencia')),
				 'nome_cliente': convert_str2unicode(dados.get('nome_cliente','')),
				 'cpf': convert_str2unicode(dados.get('CPF','')),
				 'data_atd': convert_str2date(dados.get('data_ATD','')),
				 'situacao': convert_str2unicode(dados.get('Situacoes')),
				 'situacao_financeiro': convert_str2unicode(dados.get('Situacao Financeiro','')),
				 'pontos': convert_str2int(dados.get('Pontos Comissoes','')),
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
