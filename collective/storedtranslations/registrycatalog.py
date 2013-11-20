from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component.interfaces import ComponentLookupError
from zope.i18n.interfaces import IGlobalMessageCatalog
from zope.interface import implements

REGISTRY_BASE = 'collective.storedtranslations.translationdomains'
SETTINGS_IFACE = 'collective.storedtranslations.interfaces.IStoredTranslationsSettings'


class StoredCatalog(object):
    implements(IGlobalMessageCatalog)
    identifier_base = 'collective.storedtranslations.stored'

    def __init__(self, domain, language):
        self.domain = domain
        self.language = language

    def queryMessage(self, msgid, default=None):
        # We need the registry.  This might not be available.  You
        # would think the following is the correct way to handle this:
        #
        # registry = queryUtility(IRegistry, None)
        #
        # Unfortunately, this leads to a strange problem.  When you
        # visit the Add-ons control panel in the Plone UI, all is
        # fine.  When you visit it a second time, the IRegistry
        # utility is gone, quickly leading to errors that break the
        # main template.  A zope restart is then needed before you can
        # view any page again.  The breakage seems to happen in
        # plonetheme.sunburst and/or plone.app.collection, but don't
        # take my word for that.  [Maurits, on Plone 4.3.2.]
        try:
            registry = getUtility(IRegistry)
        except ComponentLookupError:
            print "no registry"
            return default
        try:
            enabled = registry[SETTINGS_IFACE + '.use_stored_translations']
        except KeyError:
            print "no settings"
            return default
        if not enabled:
            print "stored translations not enabled"
            return default
        # Note: there is no need to make a unicode of the Message when
        # querying the registry.
        try:
            msgstr = registry[REGISTRY_BASE][self.domain][self.language][msgid]
        except KeyError:
            print "not found:", msgid
            return default
        return msgstr

    getMessage = queryMessage

    def getIdentifier(self):
        return '{0}.{1}.{2}'.format(self.identifier_base, self.domain, self.language)

    def reload(self):
        pass


class UntranslatedCatalog(StoredCatalog):
    identifier_base = 'collective.storedtranslations.untranslated'

    def queryMessage(self, msgid, default=None):
        try:
            registry = getUtility(IRegistry)
        except ComponentLookupError:
            return default
        try:
            enabled = registry[SETTINGS_IFACE].show_untranslated
        except KeyError:
            return default
        if not enabled:
            return default
        # Note: msgid may be a unicode or an instance of
        # zope.i18nmessageid.message.Message.  In the last case it may
        # have its own default.
        default = getattr(msgid, 'default', default)
        # TODO: auto add msgid to the registry with an empty translation?
        return u'[[{0}][{1}][[{2}]]'.format(self.domain, msgid, default)
