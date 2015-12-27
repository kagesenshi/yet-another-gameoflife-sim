from pysiphae.interfaces import IHomeViewResolver
from zope.interface import implements

class HomeViewResolver(object):
    implements(IHomeViewResolver)

    def resolve(self, request, groups):
        # just use this as default
        return request.resource_url(request.context, 'kagesenshi.gameoflife')
