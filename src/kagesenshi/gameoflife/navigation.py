from pysiphae.interfaces import INavigationProvider
from zope.interface import implements

class NavigationProvider(object):
    implements(INavigationProvider)

    def get_links(self):
        return [{
            'href': '/kagesenshi.gameoflife',
            'label': 'kagesenshi.gameoflife Dashboard',
            'order': 1
        }]

