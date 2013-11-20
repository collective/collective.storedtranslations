import os
from zope.i18n.zcml import handler
from zope.i18n.zcml import config
from zope.i18nmessageid import MessageFactory
from collective.storedtranslations.registrycatalog import StoredCatalog
from collective.storedtranslations.registrycatalog import UntranslatedCatalog

_ = MessageFactory('collective.storedtranslations')
LANGUAGES = config.ALLOWED_LANGUAGES
DOMAINS_KEY = 'collective_storedtranslations_domains'
DOMAINS = os.environ.get(DOMAINS_KEY, 'plone')
DOMAINS = DOMAINS.strip().replace(',', ' ')
DOMAINS = frozenset(DOMAINS.split())


def register_catalogs(domains, languages):
    if languages is None:
        return
    for domain in domains:
        for lang in languages:
            catalog1 = StoredCatalog(domain, lang)
            catalog2 = UntranslatedCatalog(domain, lang)
            handler([catalog1, catalog2], domain)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    register_catalogs(DOMAINS, LANGUAGES)
