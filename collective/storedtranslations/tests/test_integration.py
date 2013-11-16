# -*- coding: utf-8 -*-

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.i18n import translate
import unittest

from collective.storedtranslations.registrycatalog import REGISTRY_BASE
from collective.storedtranslations.registrycatalog import RegistryCatalog
from collective.storedtranslations.testing import INTEGRATION_TESTING
from collective.storedtranslations.testing import EXTRA_INTEGRATION_TESTING


class CatalogTestCase(unittest.TestCase):
    # This does NOT have the testfixture profile installed.
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.registry = getUtility(IRegistry)

    def test_getIdentifier(self):
        cat = RegistryCatalog('plone', 'nl')
        self.assertEqual(
            cat.getIdentifier(),
            'collective.storedtranslations.plone.nl')
        cat = RegistryCatalog('collective.storedtranslations', 'de')
        self.assertEqual(
            cat.getIdentifier(),
            'collective.storedtranslations.collective.storedtranslations.de')

    def test_getMessage(self):
        cat = RegistryCatalog('plone', 'nl')
        self.assertEqual(cat.getMessage('Hello world'), None)
        self.assertEqual(cat.getMessage('Hello world', 'foobar'), 'foobar')
        self.registry[REGISTRY_BASE] = \
            {u'plone': {u'nl': {u'Hello world': u'Hallo wereld'}}}
        self.assertEqual(cat.getMessage('Hello world'), 'Hallo wereld')

    def test_queryMessage(self):
        cat = RegistryCatalog('plone', 'nl')
        self.assertEqual(cat.queryMessage('Hello world'), None)
        self.assertEqual(cat.queryMessage('Hello world', 'foobar'), 'foobar')
        self.registry[REGISTRY_BASE] = \
            {u'plone': {u'nl': {u'Hello world': u'Hallo wereld'}}}
        self.assertEqual(cat.queryMessage('Hello world'), 'Hallo wereld')

    def test_reload(self):
        # This does not do anything, but should not give problems.
        cat = RegistryCatalog('plone', 'nl')
        self.assertEqual(cat.reload(), None)


class ExtraIntegrationTestCase(unittest.TestCase):
    # This has the testfixture profile installed.
    layer = EXTRA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
