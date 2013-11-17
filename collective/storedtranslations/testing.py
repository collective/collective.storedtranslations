# -*- coding: utf-8 -*-

from collective.storedtranslations import initialize
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
        # Apparently, the initialize function is not applied.  We
        # require it because it registers our catalogs.
        initialize(None)

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
