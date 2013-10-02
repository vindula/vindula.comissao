# -*- coding: utf-8 -*-
from plone.z3cform import layout
from plone.directives import form
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from vindula.comissao.register.interfaces import IVindulaComissao

class ComissaoEditForm(RegistryEditForm):
   """
   	Define form logic
   """
   schema = IVindulaComissao

ComissaoEditView = layout.wrap_form(ComissaoEditForm, ControlPanelFormWrapper)
ComissaoEditView.label = u"Vindula: Comissão Settings"