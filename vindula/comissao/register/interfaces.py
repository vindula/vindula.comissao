# -*- coding: utf-8 -*-
from zope.interface import Interface
from zope import schema

from vindula.comissao import MessageFactory as _

class IVindulaComissao(Interface):
    """
        Vindula Comissao interface
    """
    
    regras_comissoes = schema.Text(title=_(u"Regras Gerais das comissões"))
    
    
    