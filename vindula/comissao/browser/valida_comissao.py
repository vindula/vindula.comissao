# coding: utf-8
from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName

from vindula.myvindula.tools.utils import UtilMyvindula
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from vindula.comissao.models.comissao_validacao import ComissaoValidacao
from vindula.comissao.models.comissao_usuario import ComissaoUsuario

grok.templatedir('templates')

class ValidaComissaoView(grok.View, UtilMyvindula):
	grok.context(Interface)
	grok.require('zope2.View')
	grok.name('valida-comissao')

	def update(self):
		form = self.request.form

		if 'submitted' in form.keys():
			prefs_user = self.get_dados_user()

			D = {}
			D['cpf'] = prefs_user.get('cpf','')
			D['username'] = prefs_user.get('username','')
			D['competencia'] = self.Convert_utf8(form.get('competencia',''))

			D['id_usuario'] = int(form.get('id_usuario','0'))
			
			ComissaoValidacao().manage_comissao_validacao(**D)
			D.pop('id_usuario')

			for venda in form.get('id_venda',[]):
				D['id_venda'] = int(venda)
				ComissaoValidacao().manage_comissao_validacao(**D)

			self.request.response.redirect(self.context.absolute_url() + '/minha-comissao')


	def get_dados_user(self):
		membership = getToolByName(self.context, 'portal_membership')
		user_login = membership.getAuthenticatedMember().getUserName()

		prefs_user = self.get_prefs_user(user_login)
		prefs_user['username'] = self.Convert_utf8(user_login)

		return prefs_user


	def data_atual(self):
		from datetime import datetime
		return datetime.now().strftime('%d/%m/%Y às %H:%M:%S')


	def get_termo_valida(self):
		registry = getUtility(IRegistry)
		try:
			settings_comissao = registry.records['vindula.comissao.register.interfaces.IVindulaComissao.validacao_comissoes']
		except:
			settings_comissao = False

		if settings_comissao:
			return settings_comissao.value
		else:
			return ""

	def get_comissao(self,cpf):

		comissoes = ComissaoUsuario().get_comissao_by_cpf(cpf)
		return comissoes.last() 

	def get_fimMes(sef, competencia):
		data = competencia.split('/')

		import calendar
		return calendar.monthrange(int(data[1]),int(data[0]))[1]