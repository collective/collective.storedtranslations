from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.i18n.interfaces import IGlobalMessageCatalog
from zope.interface import implements

REGISTRY_BASE = 'collective.storedtranslations.translationdomains'


class StoredCatalog(object):
    implements(IGlobalMessageCatalog)

    def __init__(self, domain, language):
        self.domain = domain
        self.language = language

    def queryMessage(self, msgid, default=None):
        # Note: msgid may be a unicode or an instance of
        # zope.i18nmessageid.message.Message.  In the last case it may
        # have its own default.
        #default = getattr(msgid, 'default', default)
        registry = queryUtility(IRegistry, None)
        if registry is None:
            return default
        # Note: there is no need to make a unicode of the Message when
        # querying the registry.
        try:
            msgstr = registry[REGISTRY_BASE][self.domain][self.language][msgid]
        except KeyError:
            # Options, possibly based on environment variables or
            # registry settings:
            # - return default
            # - return formatted string with domain and msgid.
            #   Do this in a different catalog?
            # - show default of msgid if it is a Message.  This is
            #   something else than the default of this method.
            # - auto add msgid to the registry with an empty translation
            #
            #return u'[[{0}][{1}][[{2}]]'.format(self.domain, msgid, default)
            return default
        return msgstr

    getMessage = queryMessage

    def getIdentifier(self):
        return 'collective.storedtranslations.{0}.{1}'.format(self.domain, self.language)

    def reload(self):
        pass
