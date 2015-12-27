from pysiphae.interfaces import INavigationProvider, IHomeViewResolver
from zope.interface import implements

class NavigationProvider(object):
    implements(INavigationProvider)

    def get_links(self):
        return [{
            'href': '/kagesenshi.gameoflife',
            'label': 'kagesenshi.gameoflife Dashboard',
            'order': 1
        }]

class HomeViewResolver(object):
    implements(IHomeViewResolver)

    def resolve(self, request, groups):
        # just use this as default
        return request.resource_url(request.context, 'kagesenshi.gameoflife')

