from base5.portlets.browser.interfaces import IContentWellPortletManager
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.manager import ColumnPortletManagerRenderer
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer

from zope.component import adapts, getUtility, getMultiAdapter
from plone.app.portlets.browser.manage import ManageContextualPortlets
from plone.portlets.interfaces import IPortletManager
from zope.annotation.interfaces import IAnnotations, IAttributeAnnotatable
from zope.interface import Interface, implements
from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from zope import schema


COL_KEY = 'portlets.col.'


class ContentWellPortletRenderer(ColumnPortletManagerRenderer):
    """A renderer for the content-well portlets
    """
    adapts(
        Interface,
        IDefaultBrowserLayer,
        IBrowserView,
        IContentWellPortletManager)
    template = ViewPageTemplateFile('templates/renderer.pt')


class MyManageContextualPortlets(ManageContextualPortlets):
    """ Define our very own view for manage portlets """

    def getValue(self, manager):
        portletManager = getUtility(IPortletManager, name=manager)
        colstorage = getMultiAdapter((self.context, portletManager), IColStorage)
        return colstorage.col


class IColStorage(IAttributeAnnotatable):
    """Marker persistent used to store col number for portlet managers"""
    col = schema.TextLine(title=u"Number of cols for this portletManager.")

class ColStorage(object):
    """Multiadapter that adapts any context and IPortletManager to provide IColStorage"""
    implements(IColStorage)
    adapts(Interface, IPortletManager)

    def __init__(self, context, manager):
        self.context = context
        self.manager = manager
        self.key_id = COL_KEY + manager.__name__

        annotations = IAnnotations(context)
        self._col = annotations.setdefault(self.key_id, '')

    def get_col(self):
        annotations = IAnnotations(self.context)
        self._col = annotations.setdefault(self.key_id, '')
        return self._col

    def set_col(self, value):
        annotations = IAnnotations(self.context)
        annotations.setdefault(self.key_id, value)
        annotations[self.key_id] = value

    col = property(get_col, set_col)

class setPortletCols(BrowserView):
    """ View that stores the col number assigned to this portletManager for
        this context.
    """

    def __call__(self):
        manager = self.request.form['manager']
        col = self.request.form['col']
        context = aq_inner(self.context)
        portletManager = getUtility(IPortletManager, manager)
        colstorage = getMultiAdapter((context, portletManager), IColStorage)
        colstorage.col = col
        self.request.RESPONSE.setStatus('200')
        self.request.RESPONSE.setHeader('Content-type', 'application/json')
        return '{"status": "Saved!"}'
