from pyramid.view import view_config
from pysiphae.views import Views as BaseViews
from sqlalchemy.engine import create_engine
from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPFound
from wraptor.decorators import memoize
from sqlalchemy.sql import text
from kagesenshi.gameoflife.models.shorturl import ShortUrl
import json
import re

class Views(BaseViews):

    @view_config(route_name='shorturl', renderer='templates/shorturl.pt')
    def short_url(self):
        if not 'url' in self.request.params:
            return {'short_url': None}

        session = self.request.db
        url = self.request.params.get('url')
        if not re.match(r'(http|https)://.*', url):
            url = 'http://' + url

        # check if url already exist in db, if yes theres no need to duplicate
        surl = session.query(ShortUrl).filter(ShortUrl.url==url).first()
        if not surl:
            surl = ShortUrl(url)
            session.add(surl)

        return {'short_url': self.request.resource_url(self.request.context,
                            's', surl.short_id)}

    @view_config(route_name='resolve_url')
    def resolve_url(self):
        sid = self.request.matchdict['short_id']
        session = self.request.db
        url = session.query(ShortUrl).filter(ShortUrl.short_id==sid).first()
        if url:
            return HTTPFound(location=url.url)
        raise NotFound

