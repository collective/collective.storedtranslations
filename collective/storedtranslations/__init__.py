import os
from zope.i18n.zcml import handler
from zope.i18n.zcml import config
from collective.storedtranslations.registrycatalog import RegistryCatalog

DOMAINS_KEY = 'collective_storedtranslations_domains'
DOMAINS = os.environ.get(DOMAINS_KEY, ['plone'])
LANGUAGES = config.ALLOWED_LANGUAGES or ['nl', 'de']


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    for domain in DOMAINS:
        for lang in LANGUAGES:
            catalog = RegistryCatalog(domain, lang)
            handler([catalog], domain)
