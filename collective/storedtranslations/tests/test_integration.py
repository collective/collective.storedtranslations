# -*- coding: utf-8 -*-

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.i18n import translate
import unittest

from collective.storedtranslations.registrycatalog import RegistryCatalog
from collective.storedtranslations.testing import INTEGRATION_TESTING
from collective.storedtranslations.testing import EXTRA_INTEGRATION_TESTING


class IntegrationTestCase(unittest.TestCase):
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


class ExtraIntegrationTestCase(unittest.TestCase):
    # This has the testfixture profile installed.
    layer = EXTRA_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
