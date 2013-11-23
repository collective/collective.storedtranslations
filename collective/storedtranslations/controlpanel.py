from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from collective.storedtranslations import _
from collective.storedtranslations import DOMAINS
from collective.storedtranslations import LANGUAGES
from collective.storedtranslations.interfaces import IStoredTranslationsSettings
from collective.storedtranslations.interfaces import ITranslationDomain
from collective.storedtranslations.registrycatalog import REGISTRY_BASE
#from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from z3c.form import form, button
from zope.component import getUtility


class ControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IStoredTranslationsSettings
    domains = DOMAINS
    languages = LANGUAGES


class ControlPanelFormWrapper(layout.FormWrapper):
    """Use this form as the plone.z3cform layout wrapper to get the control
    panel layout.
    """

    index = ViewPageTemplateFile('controlpanel_layout.pt')

ControlPanelView = layout.wrap_form(ControlPanelForm, ControlPanelFormWrapper)
ControlPanelView.label = _(u"Stored translation settings")


class TranslationDomainEditForm(form.EditForm):
    """Edit the messages of a single language and domain.
    """
    # Not sure if we want form.extends:
    form.extends(form.EditForm)
    fields = form.field.Fields(ITranslationDomain)
    domain = u''
    language = u''
    control_panel_view = u'storedtranslations-controlpanel'

    def update(self):
        # TODO: add these to the interface, readonly or hidden?  It is
        # necessary to submit the domain and language when clicking
        # 'Save', otherwise we have no idea where to save the
        # messages.
        self.domain = self.request.get('domain', u'')
        self.language = self.request.get('language', u'')
        if self.domain not in DOMAINS:
            self.domain = u''
        if self.language not in LANGUAGES:
            self.language = u''
        super(TranslationDomainEditForm, self).update()

    def getContent(self):
        registry = getUtility(IRegistry)
        try:
            content = registry[REGISTRY_BASE][self.domain][self.language]
        except KeyError:
            content = {}
        return {u'messages': content}

    def updateActions(self):
        super(TranslationDomainEditForm, self).updateActions()
        # Maybe change the title, maybe remove the existing cancel
        # button, because its action seems to get called anyway.
        del self.actions['apply']
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

    def applyChanges(self, data):
        # TODO: this probably needs special handling.
        super(TranslationDomainEditForm, self).applyChanges(data)

TranslationDomainEdit = layout.wrap_form(TranslationDomainEditForm, ControlPanelFormWrapper)
TranslationDomainEdit.label = _(u"Stored translation messages")
