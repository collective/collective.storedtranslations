import time
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from StringIO import StringIO
from collective.storedtranslations import DOMAINS
from collective.storedtranslations import LANGUAGES
from collective.storedtranslations import _
from collective.storedtranslations.interfaces import IStoredTranslationsSettings
from collective.storedtranslations.interfaces import ITranslationDomain
from collective.storedtranslations.registrycatalog import REGISTRY_BASE
from datetime import date
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.registry.interfaces import IRegistry
from plone.z3cform import layout
from z3c.form import form, button
from z3c.form.interfaces import HIDDEN_MODE
from zope.component import getUtility, queryUtility
from zope.schema.interfaces import IVocabularyFactory


def get_language_name(context, language):
    util = queryUtility(IVocabularyFactory,
                        'plone.app.vocabularies.AvailableContentLanguages')
    if util is None:
        return language
    vocab = util(context)
    try:
        language_name = vocab.getTerm(language).title
    except LookupError:
        language_name = language
    return language_name


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

    def languages_for_display(self):
        for language in self.form.languages:
            yield {'code': language,
                   'name': get_language_name(self.context, language)}


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

pot_header = """\
# SOME DESCRIPTIVE TITLE.
# Copyright (C) %(year)s %(organization)s
# %(translator)s, %(year)s.
msgid ""
msgstr ""
"Project-Id-Version: %(package)s %(version)s\\n"
"POT-Creation-Date: %(pot_time)s\\n"
"PO-Revision-Date: %(po_time)s\\n"
"Last-Translator: %(translator)s\\n"
"Language-Team: %(language_team)s\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Generated-By: collective.storedtranslations\\n"
"Language-Code: %(language)s\\n"
"Language-Name: %(language_name)s\\n"
"Domain: %(domain)s\\n"

"""


class TranslationExport(BrowserView):

    def __call__(self):
        domain = self.request.get('form.widgets.domain', '')
        language = self.request.get('form.widgets.language', '')
        if domain not in DOMAINS:
            domain = ''
        if language not in LANGUAGES:
            language = ''
        response = self.request.response
        filename = '{}-{}.po'.format(domain, language)
        response.setHeader('Content-type', 'text/x-gettext-translation')
        response.setHeader('Content-disposition',
                           'attachment; filename=%s' % filename)
        # Get headers for .po file.
        name = self.context.getProperty('email_from_name') or u'FULL NAME'
        email = self.context.getProperty('email_from_address') or \
            u'EMAIL@ADDRESS'
        organization = self.context.Title()
        timestamp = time.strftime('%Y-%m-%d %H:%M%z')
        translator = u'{} <{}>'.format(name, email)
        language_name = get_language_name(self.context, language)
        language_team = translator
        year = date.today().year

        info = dict(
            domain=domain,
            language=language,
            language_name=language_name,
            language_team=language_team,
            organization=organization,
            package=domain,
            po_time=timestamp,
            pot_time=timestamp,
            translator=translator,
            version='1.0',
            year=year,
            )
        out = StringIO()
        out.write(pot_header % info)
        # Get stored translations.
        registry = getUtility(IRegistry)
        translations = registry[REGISTRY_BASE][domain][language]
        for msgid, msgstr in translations.items():
            out.write('msgid "%s"\n' % msgid)
            # Avoid printing "None"
            out.write('msgstr "%s"\n' % (msgstr or ''))
            out.write('\n')
        return out.getvalue()
