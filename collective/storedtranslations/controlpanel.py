from collective.storedtranslations import _
from collective.storedtranslations.interfaces import IStoredTranslationsSettings
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from z3c.form import form


class ControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IStoredTranslationsSettings


ControlPanelView = layout.wrap_form(ControlPanelForm, ControlPanelFormWrapper)
ControlPanelView.label = _(u"Stored translation settings")
