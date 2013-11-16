from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.i18n.interfaces import IGlobalMessageCatalog
from zope.interface import implements

REGISTRY_BASE = 'collective.storedtranslations.translationdomains'


class RegistryCatalog(object):
    implements(IGlobalMessageCatalog)

    def __init__(self, domain, language):
        self.domain = domain
        self.language = language

    def queryMessage(self, msgid, default=None):
        registry = queryUtility(IRegistry, None)
        if registry is None:
            return default
        try:
            msgstr = registry[REGISTRY_BASE][self.domain][self.language][msgid]
        except KeyError:
            return default
        return msgstr

    getMessage = queryMessage

    def getIdentifier(self):
        return 'collective.storedtranslations.{0}.{1}'.format(self.domain, self.language)

    def reload(self):
        pass
