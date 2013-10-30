# coding: utf-8
from five import grok
from zope.interface import Interface
from Products.statusmessages.interfaces import IStatusMessage

from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from vindula.myvindula.tools.utils import UtilMyvindula
from vindula.comissao import MessageFactory as _
from vindula.comissao.models.comissao_usuario import ComissaoUsuario

from datetime import date, datetime, timedelta
import locale

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

        comissoes = ComissaoUsuario().get_comissao_by_cpf(cpf)

        self.comissoes = comissoes
        request = self.context.REQUEST
        if 'id' in request.keys():
            id_comissao = request.get('id','') 

            self.comissao = comissoes.find(id='id_comissao').one()
        else:
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

    def getRegrasGerais(self):
        registry = getUtility(IRegistry)
        try:
            settings_comissao = registry.records['vindula.comissao.register.interfaces.IVindulaComissao.regras_comissoes']
        except:
            settings_comissao = False

        if settings_comissao:
            return settings_comissao.value
        else:
            return ""

    def get_titulo_extrato(self):
        registry = getUtility(IRegistry)
        try:
            settings_comissao = registry.records['vindula.comissao.register.interfaces.IVindulaComissao.titulo_comissoes']
        except:
            settings_comissao = False       

        if settings_comissao:
            return settings_comissao.value
        else:
            return ''


    def format_data(self,data):
        if data:
            return data.strftime('%d/%m/%Y')
        return ''
    
    def format_cpf( self, cpf ):
        """ 
            Method that formats a brazilian CPF

            Tests:
            >>> print Cpf().format('91289037736')
            912.890.377-36
        """
        try:
            return "%s.%s.%s-%s" % ( cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])
        except:
            return ''

    def format_moeda(self, val):
        '''
            Vamos adicionar a linha 
            $ sudo echo “pt_BR.UTF-8 UTF-8" >> /var/lib/locales/supported.d/local
            Reconfigurando locales
            $ sudo dpkg-reconfigure locales

            mais informações
            http://teago.futuria.com.br/howto/python-26-configurando-locales-pt-br-utf-8/
        '''
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.currency( float(val), grouping=True)


    def format_number(self, val):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return locale.format('%d', val, grouping=True)
        