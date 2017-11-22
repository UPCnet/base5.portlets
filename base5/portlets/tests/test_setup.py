# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

from base5.portlets.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of base5.portlets into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if base5.portlets is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled('base5.portlets'))

    def test_uninstall(self):
        """Test if base5.portlets is cleanly uninstalled."""
        self.installer.uninstallProducts(['base5.portlets'])
        self.assertFalse(self.installer.isProductInstalled('base5.portlets'))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IBase5PortletsLayer is registered."""
        from base5.portlets.interfaces import IBase5PortletsLayer
        from plone.browserlayer import utils
        self.failUnless(IBase5PortletsLayer in utils.registered_layers())
