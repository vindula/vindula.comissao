# coding: utf-8
from five import grok
from zope.interface import Interface


from vindula.myvindula.tools.utils import UtilMyvindula


from vindula.comissao.models.comissao_usuario import ComissaoUsuario

from datetime import date


grok.templatedir('templates')

class ListaComissaoView(grok.View, UtilMyvindula):
	grok.context(Interface)
	grok.require('zope2.View')
	grok.name('lista-comissao')



	def lista_usuarios(self):
		# data = date.today()
		# competencia = u'%s/%s' %(data.month,data.year)

		return self.rs_to_list(ComissaoUsuario().get_comissoes_lastCompetencia())
	

	def  rs_to_list(self,rs):
		if rs:
			return [i for i in rs]
		return []



	# def prefs_user(self, cpf_usuario):
	# 	dados = ModelsDadosFuncdetails().get_DadosFuncdetails_byValueAndField(cpf_usuario,u'cpf')
	# 	if dados.count() == 0:
	# 		dados = ModelsDadosFuncdetails().get_DadosFuncdetails_byValueAndField(cpf_usuario,u'teaching_research')

	# 		if dados.count() >= 1:
	# 			username = dados[0].instance.username
	# 			return self.get_prefs_user(username)

	# 	return {}
