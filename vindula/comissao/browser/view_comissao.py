# coding: utf-8
from five import grok
from zope.interface import Interface


from vindula.comissao.browser.my_comissao import MyComissaoView


from vindula.comissao.models.comissao_usuario import ComissaoUsuario

from datetime import date


grok.templatedir('templates')

class ViewComissaoView(MyComissaoView):
	grok.context(Interface)
	grok.require('zope2.View')
	grok.name('visao-comissao')

	def update(self):
		self.request['disable_border'] = True
		self.request['disable_plone.leftcolumn'] = True
		self.request['disable_plone.rightcolumn'] = True


	def comissoes(self):
		request = self.context.REQUEST
		if 'cpf_user' in request.keys():
			cpf_user = self.Convert_utf8(request.get('cpf_user',''))

			comissoes = ComissaoUsuario().get_comissao_by_cpf(cpf_user)
			return comissoes

		return None


	def comissao(self):
		comissoes = self.comissoes()
		if comissoes:
			return comissoes.last() 

		return None


	def prefs_user(self):
		data = self.comissao()
		if data:
			return {'name':data.name,
					'cpf':data.cpf}

		return {}