# -*- coding: utf-8 -*-

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.app.testing.interfaces import SITE_OWNER_NAME
from plone.app.testing.interfaces import SITE_OWNER_PASSWORD
from plone.registry.interfaces import IRegistry
from plone.testing.z2 import Browser
from zope.component import getUtility
from zope.i18n import translate
import unittest

from collective.storedtranslations.registrycatalog import REGISTRY_BASE
from collective.storedtranslations.registrycatalog import StoredCatalog
from collective.storedtranslations.testing import INTEGRATION_TESTING
from collective.storedtranslations.testing import EXTRA_INTEGRATION_TESTING
from collective.storedtranslations.testing import UNINSTALLED_FUNCTIONAL_TESTING
from zope.i18n.zcml import handler


class UninstalledTestCase(unittest.TestCase):
    # This does NOT have our profiles installed.
    layer = UNINSTALLED_FUNCTIONAL_TESTING

    def test_qi(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ['Manager'])
        portal.portal_languages.setDefaultLanguage('nl')
        portal.prefs_install_products_form()
        portal.prefs_install_products_form()

    def test_view_qi(self):
        # There is something funky and disruptive going on when
        # viewing the add-ons control panel.  Let's check it by
        # visiting it two times, because the first time seems to go
        # fine always.
        app = self.layer['app']
        portal = self.layer['portal']
        portal.portal_languages.setDefaultLanguage('nl')
        browser = Browser(app)
        browser.handleErrors = False
        portal_url = portal.absolute_url()
        browser.open(portal_url + '/login')
        browser.getControl(name='__ac_name').value = SITE_OWNER_NAME
        browser.getControl(name='__ac_password').value = SITE_OWNER_PASSWORD
        browser.getControl(name='submit').click()
        browser.open(portal_url + '/prefs_install_products_form')
        browser.open(portal_url + '/prefs_install_products_form')


class CatalogTestCase(unittest.TestCase):
    # This does NOT have the testfixture profile installed.
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.registry = getUtility(IRegistry)
        # Create a catalog for domain plone and language Dutch
        # (nl == The Netherlands).
        self.cat = StoredCatalog('plone', 'nl')
        # Register catalog in the same way as is done on zope startup.
        handler([self.cat], 'plone')

    def test_getIdentifier(self):
        self.assertEqual(
            self.cat.getIdentifier(),
            'collective.storedtranslations.stored.plone.nl')
        cat_de = StoredCatalog('collective.storedtranslations', 'de')
        self.assertEqual(
            cat_de.getIdentifier(),
            'collective.storedtranslations.stored.collective.storedtranslations.de')

    def test_getMessage(self):
        self.assertEqual(self.cat.getMessage('Hello world'), None)
        self.assertEqual(self.cat.getMessage('Hello world', 'foobar'), 'foobar')
        self.registry[REGISTRY_BASE] = \
            {'plone': {'nl': {u'Hello world': u'Hallo wereld'}}}
        self.assertEqual(self.cat.getMessage('Hello world'), 'Hallo wereld')

        # Try other language and domain.  This should not find the
        # existing translation.
        cat_de = StoredCatalog('plone', 'de')
        self.assertEqual(cat_de.getMessage('Hello world'), None)
        cat_other = StoredCatalog('other_domain', 'nl')
        self.assertEqual(cat_other.getMessage('Hello world'), None)

    def test_queryMessage(self):
        self.assertEqual(self.cat.queryMessage('Hello world'), None)
        self.assertEqual(self.cat.queryMessage('Hello world', 'foobar'), 'foobar')
        self.registry[REGISTRY_BASE] = \
            {'plone': {'nl': {u'Hello world': u'Hallo wereld'}}}
        self.assertEqual(self.cat.queryMessage('Hello world'), 'Hallo wereld')

        # Try other language and domain.  This should not find the
        # existing translation.
        cat_de = StoredCatalog('plone', 'de')
        self.assertEqual(cat_de.getMessage('Hello world'), None)
        cat_other = StoredCatalog('other_domain', 'nl')
        self.assertEqual(cat_other.getMessage('Hello world'), None)

    def test_reload(self):
        # This does not do anything, but should not give problems.
        self.assertEqual(self.cat.reload(), None)

    def test_translate(self):
        # For the translate call to work, we must register the catalog
        # in the same way as is done on zope startup.  We register
        # some other catalogs as well.
        cat_de = StoredCatalog('plone', 'de')
        cat_fr = StoredCatalog('plone', 'fr')
        handler([cat_de, self.cat, cat_fr], 'plone')
        # For some reason, if the next two lines are used AND you use
        # queryUtility in the registrycatalog, the IRegistry utility
        # is not found there.  Using a try/except around getUtility
        # does work.  This is not just some corner case only
        # encountered in the tests, but a real problem.  So if these
        # tests start failing, you should not fix the tests, but fix
        # the code.  Just a friendly warning. :-)
        cat_other = StoredCatalog('other_domain', 'nl')
        handler([cat_other], 'other_domain')

        # No translation is found, so the default is returned.
        self.assertEqual(
            translate('Hello world', 'plone', target_language='nl'),
            'Hello world')

        # Add translations.
        self.registry[REGISTRY_BASE] = \
            {'plone':
                {'de': {u'Hello world': u'Hallo Welt'},
                 'nl': {u'Hello moon': u'Hallo maan',
                        u'Hello world': u'Hallo wereld',
                        u'Goodbye world': u'Dag wereld'},
                 'fr': {u'Hello world': u'Allô monde'}},
             'other_domain':
                {'nl': {u'Hello world': u'Hallo andere wereld'}},
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
        self.assertEqual(
            translate('Hello world', 'other_domain', target_language='nl'),
            'Hallo andere wereld')


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
