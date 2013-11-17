# -*- coding: utf-8 -*-

from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.i18n import translate
import unittest

from collective.storedtranslations.registrycatalog import REGISTRY_BASE
from collective.storedtranslations.registrycatalog import RegistryCatalog
from collective.storedtranslations.testing import INTEGRATION_TESTING
from collective.storedtranslations.testing import EXTRA_INTEGRATION_TESTING
from zope.i18n.zcml import handler


class CatalogTestCase(unittest.TestCase):
    # This does NOT have the testfixture profile installed.
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.registry = getUtility(IRegistry)
        # Create a catalog for domain plone and language Dutch
        # (nl == The Netherlands).
        self.cat = RegistryCatalog('plone', 'nl')
        # Register catalog in the same way as is done on zope startup.
        handler([self.cat], 'plone')

    def test_getIdentifier(self):
        self.assertEqual(
            self.cat.getIdentifier(),
            'collective.storedtranslations.plone.nl')
        cat_de = RegistryCatalog('collective.storedtranslations', 'de')
        self.assertEqual(
            cat_de.getIdentifier(),
            'collective.storedtranslations.collective.storedtranslations.de')

    def test_getMessage(self):
        self.assertEqual(self.cat.getMessage('Hello world'), None)
        self.assertEqual(self.cat.getMessage('Hello world', 'foobar'), 'foobar')
        self.registry[REGISTRY_BASE] = \
            {u'plone': {u'nl': {u'Hello world': u'Hallo wereld'}}}
        self.assertEqual(self.cat.getMessage('Hello world'), 'Hallo wereld')

        # Try other language and domain.  This should not find the
        # existing translation.
        cat_de = RegistryCatalog('plone', 'de')
        self.assertEqual(cat_de.getMessage('Hello world'), None)
        cat_other = RegistryCatalog('other_domain', 'nl')
        self.assertEqual(cat_other.getMessage('Hello world'), None)

    def test_queryMessage(self):
        self.assertEqual(self.cat.queryMessage('Hello world'), None)
        self.assertEqual(self.cat.queryMessage('Hello world', 'foobar'), 'foobar')
        self.registry[REGISTRY_BASE] = \
            {u'plone': {u'nl': {u'Hello world': u'Hallo wereld'}}}
        self.assertEqual(self.cat.queryMessage('Hello world'), 'Hallo wereld')

        # Try other language and domain.  This should not find the
        # existing translation.
        cat_de = RegistryCatalog('plone', 'de')
        self.assertEqual(cat_de.getMessage('Hello world'), None)
        cat_other = RegistryCatalog('other_domain', 'nl')
        self.assertEqual(cat_other.getMessage('Hello world'), None)

    def test_reload(self):
        # This does not do anything, but should not give problems.
        self.assertEqual(self.cat.reload(), None)

    def test_translate(self):
        # For the translate call to work, we must register the catalog
        # in the same way as is done on zope startup.  We register
        # some other catalogs as well.
        cat_de = RegistryCatalog('plone', 'de')
        cat_fr = RegistryCatalog('plone', 'fr')
        handler([cat_de, self.cat, cat_fr], 'plone')
        # For some reason, if the next two lines are used, the
        # IRegistry utility is not found in the registrycatalog.
        # Seems to work fine in practice.  Weird.
        #
        #cat_other = RegistryCatalog('other_domain', 'nl')
        #handler([cat_other], 'other_domain')

        # No translation is found, so the default is returned.
        self.assertEqual(
            translate('Hello world', 'plone', target_language='nl'),
            'Hello world')

        # Add translations.
        self.registry[REGISTRY_BASE] = \
            {u'plone':
                {u'de': {u'Hello world': u'Hallo Welt'},
                 u'nl': {u'Hello moon': u'Hallo maan',
                         u'Hello world': u'Hallo wereld',
                         u'Goodbye world': u'Dag wereld'},
                 u'fr': {u'Hello world': u'Allô monde'}},
             u'other_domain':
                {u'nl': {u'Hello world': u'Hallo andere wereld'}},
             }
        self.assertEqual(
            translate('Hello world', 'plone', target_language='nl'),
            'Hallo wereld')
        self.assertEqual(
            translate('Hello world', 'plone', target_language='de'),
            'Hallo Welt')
        self.assertEqual(
            translate('Hello world', 'plone', target_language='fr'),
            u'Allô monde')
        # If adding the registry catalog for the other domain is done
        # without bad side effects, the translate call should work,
        # but for the moment it returns the default.
        self.assertEqual(
            translate('Hello world', 'other_domain', target_language='nl'),
            'Hello world')


class ExtraIntegrationTestCase(unittest.TestCase):
    # This has the testfixture profile installed.
    layer = EXTRA_INTEGRATION_TESTING

    def test_translate(self):
        # We have a translation for Dutch in the testfixture.
        self.assertEqual(
            translate('Hello world', 'plone', target_language='nl'),
            'Hallo wereld')
        # We have one for German too.
        self.assertEqual(
            translate('Hello world', 'plone', target_language='de'),
            'Hallo Welt')
        # We have one for Frysian, but this language is not registered
        # in the zope_i18n_allowed_languages variable.
        self.assertEqual(
            translate('Hello world', 'plone', target_language='fr'),
            'Hello world')
        # Try a different domain.  We have a Dutch and a German
        # translation, but not a Frysian.
        self.assertEqual(
            translate('Hello world', 'collective.storedtranslations',
                      target_language='nl'),
            u'Hallo vertaalde wereld')
        self.assertEqual(
            translate('Hello world', 'collective.storedtranslations',
                      target_language='de'),
            u'Hallo \xfcbersetzte Welt')
        self.assertEqual(
            translate('Hello world', 'collective.storedtranslations',
                      target_language='fy'),
            u'Hello world')
