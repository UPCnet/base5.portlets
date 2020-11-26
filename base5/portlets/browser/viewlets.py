from base5.portlets import messageFactory as _
from plone import api
from plone.app.controlpanel.interfaces import IPloneControlPanelView
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.portlets.browser import interfaces as pap_interfaces
from plone.app.portlets.browser.interfaces import IManagePortletsView
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletRetriever
from zope.component import getMultiAdapter
from zope.component import ComponentLookupError
from zope.component import getUtility
from base5.portlets.browser.manager import IColStorage


class ContentWellPortletsViewlet(ViewletBase):
    name = ""
    manage_view = ""

    @property
    def dont_show(self):
        return IPloneControlPanelView.providedBy(self.view)

    @property
    def dont_show_links(self):
        """Show links to portlet manager management views only in manage
        portlets view.
        """
        return not IManagePortletsView.providedBy(self.view)

    def update(self):
        context_state = getMultiAdapter(
            (self.context,
             self.request),
            name=u'plone_context_state')

        if pap_interfaces.IManageContentTypePortletsView.providedBy(self.view):
            key = self.request.form.get('key')
            self.manageUrl = '%s/%s?key=%s' % (
                context_state.view_url(), self.manage_type_view, key)
        else:
            self.manageUrl = '%s/%s' % (
                context_state.view_url(), self.manage_view)

        # This is the way it's done in plone.app.portlets.manager, so we'll do
        # the same
        mt = api.portal.get_tool(name='portal_membership')
        self.canManagePortlets = not self.dont_show_links and mt.checkPermission(
            'Portlets: Manage portlets', self.context)

    def showPortlets(self):
        return not self.dont_show\
            and '@@manage-portlets' not in self.request.get('URL')

    def portletManagers(self):
        managers = []
        try:
            for n in range(1, 4):
                name = 'ContentWellPortlets.%s%s' % (self.name, n)
                mgr = getUtility(
                    IPortletManager,
                    name=name,
                    context=self.context)
                managers.append((mgr, name))
            return managers
        except ComponentLookupError:
            return []

    def portletManagersToShow(self):
        visibleManagers = []
        for mgr, name in self.portletManagers():
            if mgr(self.context, self.request, self).visible:
                visibleManagers.append(name)

        managers = []
        numManagers = len(visibleManagers)
        for counter, name in enumerate(visibleManagers):
            col = "col-md-%s" % str(self.getColValueForManager(name))
            managers.append(
                (name, 'cell %s %s' % (name.split('.')[-1], col)))
        return managers

    def num_portlets_for_manager(self, name):
        """Return the number of portlets for a given portlet manager name.

        :param name: Portlet manager name
        :type name: String
        :returns: Number of portlets for the given manager name.
        :rtype: Integer
        """
        mgr = getUtility(IPortletManager,
                         name=name,
                         context=self.context)
        retriever = getMultiAdapter((self.context, mgr), IPortletRetriever)
        portlets = retriever.getPortlets()
        return len(portlets)

    def getColValueForManager(self, manager):
        portletManager = getUtility(IPortletManager, manager)
        colstorage = getMultiAdapter((self.context, portletManager), IColStorage)
        col = colstorage.col
        if col:
            return col
        else:
            return '4'

class PortletsBelowTitleViewlet(ContentWellPortletsViewlet):
    name = 'BelowTitlePortletManager'
    manage_view = '@@manage-portletsbelowtitlecontent'
    manage_type_view = '@@manage-typeportletsbelowtitlecontent'
    cssid = 'portlets-below-title'
    manage_portlets_link_class = 'managePortletsBelowTitleLink'

    @property
    def manage_portlets_link_text(self):
        return _(
            'manage_portlets_below_title_link',
            default=u'Add, edit or remove a portlet below the content title')


class PortletsAboveViewlet(ContentWellPortletsViewlet):
    name = 'AbovePortletManager'
    manage_view = '@@manage-portletsabovecontent'
    manage_type_view = '@@manage-typeportletsabovecontent'
    cssid = 'portlets-above'
    manage_portlets_link_class = 'managePortletsAboveLink'

    @property
    def manage_portlets_link_text(self):
        return _(
            'manage_portlets_above_link',
            default=u'Add, edit or remove a portlet above the content')


class PortletsBelowViewlet(ContentWellPortletsViewlet):
    name = 'BelowPortletManager'
    manage_view = '@@manage-portletsbelowcontent'
    manage_type_view = '@@manage-typeportletsbelowcontent'
    cssid = 'portlets-below'
    manage_portlets_link_class = 'managePortletsBelowLink'

    @property
    def manage_portlets_link_text(self):
        return _(
            'manage_portlets_below_link',
            default=u'Add, edit or remove a portlet below the content')
