# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import login
from plone.app.textfield import RichTextValue
import transaction
import unittest2 as unittest
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from Products.TinyMCE.interfaces.utility import ITinyMCE
from collective.tinymcetiles.testing import TILES_INTEGRATION_TESTING
from plone.testing.z2 import Browser


class IntegrationTestCase(unittest.TestCase):
    layer = TILES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

    def test_dependencies_installed(self):
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('plone.app.blocks'))
        self.assertTrue(qi.isProductInstalled('plone.app.tiles'))

    def test_js_installed(self):
        pj = getToolByName(self.portal, 'portal_javascripts')
        self.assertIn(
            '++resource++collective.tinymcetiles.plugin/event.js', pj.getResourceIds())

    def test_tinymce_configured(self):
        tinymce = getUtility(ITinyMCE)
        self.assertIn(
            'plonetiles|/++resource++collective.tinymcetiles.plugin/editor_plugin.js', tinymce.customplugins)
        self.assertIn('plonetiles', tinymce.customtoolbarbuttons)

    def test_tile_rendering(self):
        try:
            self.portal.invokeFactory('Folder', 'test-folder')
        except:
            self.portal.invokeFactory('Document', 'test-folder')
        self.folder = self.portal['test-folder']
        self.folder.invokeFactory('Document', 'd1')
        d1 = self.folder.get('d1')
        d1.setTitle(u'New title')
        d1.text = RichTextValue(u"""\
<p>
    <img
        src="/++resource++collective.tinymcetiles.plugin/placeholder.gif"
        alt="./@@dummy.tile/tile-1"
        class="mceItem mceTile"
        />
</p>
""", 'text/html', 'text/x-html-safe', 'utf-8')

        transaction.commit()

        browser = Browser(self.portal)
        browser.handleErrors = False

        browser.open(d1.absolute_url())
        self.assertIn('Test tile rendered', browser.contents)
        self.assertIn('<p>With child tags</p>', browser.contents)
        self.assertIn('And tail text', browser.contents)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
