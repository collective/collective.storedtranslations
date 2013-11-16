import os
from zope.i18n.zcml import handler
from zope.i18n.zcml import config
from collective.storedtranslations.registrycatalog import RegistryCatalog

DOMAINS_KEY = 'collective_storedtranslations_domains'
DOMAINS = os.environ.get(DOMAINS_KEY, ['plone'])
LANGUAGES = config.ALLOWED_LANGUAGES or ['nl', 'de']


def register_catalogs(domains, languages):
    for domain in domains:
        for lang in languages:
            catalog = RegistryCatalog(domain, lang)
            handler([catalog], domain)


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    register_catalogs(DOMAINS, LANGUAGES)
