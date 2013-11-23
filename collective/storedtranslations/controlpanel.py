from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from collective.storedtranslations import _
from collective.storedtranslations.interfaces import IStoredTranslationsSettings
from collective.storedtranslations.interfaces import ITranslationDomain
from collective.storedtranslations.registrycatalog import REGISTRY_BASE
#from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from z3c.form import form, button
from zope.component import getUtility
from plone.autoform.form import AutoExtensibleForm


class ControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IStoredTranslationsSettings


class ControlPanelFormWrapper(layout.FormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
    panel layout.
    """

    index = ViewPageTemplateFile('controlpanel_layout.pt')

ControlPanelView = layout.wrap_form(ControlPanelForm, ControlPanelFormWrapper)
ControlPanelView.label = _(u"Stored translation settings")
#ControlPanelView.index = ViewPageTemplateFile('controlpanel_layout.pt')


class TranslationDomainEditForm(AutoExtensibleForm, form.EditForm):
    """Edit the messages of a single language and domain.
    """
    #form.extends(form.EditForm)
    schema = ITranslationDomain
    domain = u''
    language = u''

    def update(self):
        self.domain = self.request.get('domain', u'')
        self.language = self.request.get('language', u'')
        self.updateWidgets()

    def getContent(self):
        registry = getUtility(IRegistry)
        content = registry[REGISTRY_BASE][self.domain][self.language]
        return {u'messages': content}

    def updateActions(self):
        super(RegistryEditForm, self).updateActions()
        self.actions['save'].addClass("context")
        self.actions['cancel'].addClass("standalone")

    @button.buttonAndHandler(_(u"Save"), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes saved."),
            "info")
        self.request.response.redirect(self.request.getURL())

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes canceled."),
            "info")
        self.request.response.redirect("%s/%s" % (
            self.context.absolute_url(),
            self.control_panel_view))

TranslationDomainEdit = layout.wrap_form(TranslationDomainEditForm, ControlPanelFormWrapper)
TranslationDomainEdit.label = _(u"Stored translation messages")
