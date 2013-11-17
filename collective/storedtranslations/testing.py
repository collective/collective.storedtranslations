# -*- coding: utf-8 -*-

from collective.storedtranslations import initialize
from collective.storedtranslations import register_catalogs
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.storedtranslations
        self.loadZCML(package=collective.storedtranslations)

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.storedtranslations:default')


class FixtureWithExtraProfile(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.storedtranslations
        self.loadZCML(package=collective.storedtranslations)
        # In the initialize function our catalogs are registered, but
        # apparently this is not applied during test setup.  We
        # require it though, so we call it manually.
        initialize(None)
        # Let's explicitly register some domains and languages.
        register_catalogs(['plone', 'collective.storedtranslations'],
                          ['nl', 'de'])

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'collective.storedtranslations:default')
        self.applyProfile(portal, 'collective.storedtranslations:testfixture')


FIXTURE = Fixture()
FIXTURE_WITH_EXTRA_PROFILE = FixtureWithExtraProfile()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='collective.storedtranslations:Integration',
)
EXTRA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE_WITH_EXTRA_PROFILE,),
    name='collective.storedtranslations:ExtraIntegration',
)
