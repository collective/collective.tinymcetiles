# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.registry.interfaces import IRegistry
from plone.testing import z2
from plone.testing.z2 import ZSERVER_FIXTURE
from plone.tiles import Tile
from zope.component import getUtility
from zope.configuration import xmlconfig

import collective.tinymcetiles
import plone.app.contentlistingtile
import plone.app.contenttypes
import plone.app.event


class DummyTile(Tile):
    def __call__(self):
        return u"""\
<html>
<body>Test tile rendered<p>With child tags</p>And tail text</body>
</html>
"""


class TilesLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package

#        xmlconfig.file('configure.zcml', Products.DateRecurringIndex,
#                       context=configurationContext)
#        xmlconfig.file('configure.zcml', plone.app.event,
#                       context=configurationContext)
        z2.installProduct(app, 'Products.DateRecurringIndex')
        xmlconfig.file('configure.zcml', plone.app.contenttypes,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', collective.tinymcetiles,
                       context=configurationContext)
        xmlconfig.file('configure.zcml', plone.app.contentlistingtile,
                       context=configurationContext)
        xmlconfig.string("""\
<configure package="collective.tinymcetiles" xmlns="http://namespaces.plone.org/plone">
    <tile
        name="dummy.tile"
        title="Dummy tile"
        description="dummy"
        add_permission="cmf.ModifyPortalContent"
        class=".testing.DummyTile"
        permission="zope2.View"
        for="*"
        />
</configure>
""", context=configurationContext)

    def tearDownZope(self, app):
        # Uninstall products installed above
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'plone.app.contenttypes:default')
        applyProfile(portal, 'collective.tinymcetiles:default')
        applyProfile(portal, 'plone.app.contentlistingtile:default')
        #        applyProfile(portal, 'plone.app.texttile:default')
        registry = getUtility(IRegistry)
        registry["plone.app.tiles"].append('dummy.tile')


"""
<?xml version="1.0"?>
<registry>

    <record name="plone.app.tiles">
        <value purge="false">
            <element>plone.app.texttile</element>
        </value>
    </record>

</registry>
"""

TILES_FIXTURE = TilesLayer()

TILES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TILES_FIXTURE,),
    name="collective.tinymcetiles:Integration")
TILES_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TILES_FIXTURE,),
    name="collective.tinymcetiles:Functional")

TILES_ROBOT_TESTING = FunctionalTesting(
    bases=(TILES_FIXTURE,
           REMOTE_LIBRARY_BUNDLE_FIXTURE,
           ZSERVER_FIXTURE),
    name='collective.tinymcetiles:Robot')

ROBOT_TESTING = TILES_ROBOT_TESTING
