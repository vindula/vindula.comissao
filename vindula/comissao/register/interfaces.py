# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema

from vindula.comissao import MessageFactory as _

class IVindulaComissao(Interface):
    """
        Vindula Comissao interface
    """
    
    titulo_comissoes = schema.TextLine(title=_(u"Titulo do extrato de comissões"))
    regras_comissoes = schema.Text(title=_(u"Regras Gerais das comissões"))
    validacao_comissoes = schema.Text(title=_(u"Termo de validação das comissões"))

    