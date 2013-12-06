from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from StringIO import StringIO
from collective.storedtranslations import _
from collective.storedtranslations import DOMAINS
from collective.storedtranslations import LANGUAGES
from collective.storedtranslations.interfaces import IStoredTranslationsSettings
from collective.storedtranslations.interfaces import ITranslationDomain
from collective.storedtranslations.registrycatalog import REGISTRY_BASE
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from z3c.form import form, button
from z3c.form.interfaces import HIDDEN_MODE
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
    translation_export_view = u'storedtranslations-export'

    def update(self):
        self.domain = self.request.get('form.widgets.domain', '')
        self.language = self.request.get('form.widgets.language', '')
        if self.domain not in DOMAINS:
            self.domain = ''
        if self.language not in LANGUAGES:
            self.language = ''
        super(TranslationDomainEditForm, self).update()

    def getContent(self):
        registry = getUtility(IRegistry)
        try:
            content = registry[REGISTRY_BASE][self.domain][self.language]
        except KeyError:
            # Registry item will get created when we save.
            content = {}
        return {u'messages': content}

    def updateWidgets(self, prefix=None):
        super(TranslationDomainEditForm, self).updateWidgets(prefix)
        # Domain and language should be unchangeable and should be in
        # the data that gets posted.
        self.widgets['domain'].mode = HIDDEN_MODE
        self.widgets['language'].mode = HIDDEN_MODE

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
        self.request.response.redirect("%s/%s" % (
            self.context.absolute_url(),
            self.control_panel_view))

    @button.buttonAndHandler(_(u"Cancel"), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes canceled."),
            "info")
        self.request.response.redirect("%s/%s" % (
            self.context.absolute_url(),
            self.control_panel_view))

    @button.buttonAndHandler(_(u"Save and export translations"), name='export')
    def handleExport(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        # First save the changes, just like the Save button.
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Changes saved and exported."),
            "info")
        view = '{}?form.widgets.domain={}&form.widgets.language={}'.format(
            self.translation_export_view, self.domain, self.language)
        self.request.response.redirect("%s/%s" % (
            self.context.absolute_url(), view))

    def applyChanges(self, data):
        registry = getUtility(IRegistry)
        domain = data['domain']
        language = data['language']
        messages = data['messages']
        record = registry[REGISTRY_BASE]
        # Create the translationdomain.
        if domain not in record:
            record[domain] = {}
        domain_record = record[domain]
        if language not in domain_record:
            domain_record[language] = {}
        # Store the messages.
        domain_record[language] = messages
        # Explicitly set the record.  If you only update the
        # dictionaries, your changes will be lost after the next Plone
        # restart.
        registry[REGISTRY_BASE] = record

TranslationDomainEdit = layout.wrap_form(TranslationDomainEditForm, ControlPanelFormWrapper)
TranslationDomainEdit.label = _(u"Stored translation messages")
TranslationDomainEdit.index = ViewPageTemplateFile('controlpanel_messages.pt')


class TranslationExport(BrowserView):

    def __call__(self):
        self.domain = self.request.get('form.widgets.domain', '')
        self.language = self.request.get('form.widgets.language', '')
        if self.domain not in DOMAINS:
            self.domain = ''
        if self.language not in LANGUAGES:
            self.language = ''
        response = self.request.response
        filename = '{}-{}.po'.format(self.domain, self.language)
        response.setHeader('Content-type', 'text/x-gettext-translation')
        response.setHeader('Content-disposition',
                           'attachment; filename=%s' % filename)
        registry = getUtility(IRegistry)
        translations = registry[REGISTRY_BASE][self.domain][self.language]
        out = StringIO()
        for msgid, msgstr in translations.items():
            out.write('msgid "%s"\n' % msgid)
            # Avoid printing "None"
            out.write('msgstr "%s"\n' % (msgstr or ''))
            out.write('\n')
        return out.getvalue()
