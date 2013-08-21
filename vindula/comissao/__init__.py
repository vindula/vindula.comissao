# coding: utf-8
from zope.i18nmessageid import MessageFactory

# Set up the i18n message factory for our package
MessageFactory = MessageFactory('vindula.comissao')

#Variavel para habilitar aba de comissão no perfil do usuario
import os
os.environ['enable_comissao'] = 'True'