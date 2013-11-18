import os
from zope.i18n.zcml import handler
from zope.i18n.zcml import config
from collective.storedtranslations.registrycatalog import StoredCatalog

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
            catalog = StoredCatalog(domain, lang)
            handler([catalog], domain)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    register_catalogs(DOMAINS, LANGUAGES)
