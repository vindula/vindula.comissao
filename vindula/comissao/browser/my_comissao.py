# coding: utf-8
from five import grok
from zope.interface import Interface
from Products.statusmessages.interfaces import IStatusMessage

from Products.CMFCore.utils import getToolByName

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.comissao import MessageFactory as _
from vindula.comissao.models.comissao_usuario import ComissaoUsuario

from datetime import date, datetime, timedelta

grok.templatedir('templates')

class MyComissaoView(grok.View, UtilMyvindula):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('minha-comissao')
    
    comissao = None
    prefs_user = None

    def static_url(self):
        url_portal = self.context.portal_url()
        return url_portal + '/++resource++vindula.comissao'

    def update(self):
        membership = getToolByName(self.context, 'portal_membership')
        user_login = membership.getAuthenticatedMember().getUserName()

        self.prefs_user = self.get_prefs_user(user_login)

        cpf = self.prefs_user.get('cpf') or self.prefs_user.get('teaching_research') or ''

        try:cpf = unicode(cpf, 'utf-8')
        except:pass

        # import pdb;pdb.set_trace()
        comissoes = ComissaoUsuario().get_comissao_by_cpf(cpf)

        self.comissao = comissoes.last() 


    def validateUser(self):
        cpf_valid = False
        request = self.context.REQUEST

        if 'cpf' not in request.SESSION.keys():
            if 'cpf_validate' in request.keys():
                cpf_valid = self.CPFValid(request)
                if not cpf_valid:
                    IStatusMessage(self.request).addStatusMessage(_(u'CPF não é valido.'),"error")
        elif 'cpf_time' in request.SESSION.keys():
            if request.SESSION.get('cpf_time') < datetime.now() - timedelta(minutes=10):
                if 'cpf_validate' in request.keys():
                    cpf_valid = self.CPFValid(request)
                    if not cpf_valid:
                        IStatusMessage(self.request).addStatusMessage(_(u'CPF não é valido.'),"error")
            else:
                cpf_valid = True
        else:
            cpf_valid = True

        return cpf_valid

    def CPFValid(self, request):
        membership = getToolByName(self.context, 'portal_membership')
        user_login = membership.getAuthenticatedMember().getUserName()
        prefs_user = self.get_prefs_user(user_login)
        if prefs_user:
            cpf = prefs_user.get('cpf') or prefs_user.get('teaching_research') or ''
            cpf_validate = request.get('cpf_validate')
            cpf = cpf.replace('.', '').replace('-', '')
            cpf_validate = cpf_validate.replace('.', '').replace('-', '')
            if cpf == cpf_validate:
                request.SESSION['cpf'] = cpf
                request.SESSION['cpf_time'] = datetime.now()
                return True

        return False