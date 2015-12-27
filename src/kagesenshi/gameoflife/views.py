from pyramid.view import view_config
from pysiphae.views import Views as BaseViews
from sqlalchemy.engine import create_engine
from pyramid.exceptions import NotFound
from pyramid.httpexceptions import HTTPFound
from wraptor.decorators import memoize
from sqlalchemy.sql import text
from .models.state import State
from .models.shorturl import ShortUrl
from .engine import GameOfLife
import json
import re

def flatten_grid(data):
    for y, row in enumerate(data):
        for x, val in enumerate(row):
            yield {'x': x, 'y':y, 'val': val}

class Views(BaseViews):

    @view_config(route_name='gameoflife', renderer='templates/default.pt')
    def default_view(self):
        return { 'sessionid': 'default' }

    @view_config(route_name='golsession', renderer='json')
    def game_of_life_json(self):
        sessionid = self.request.matchdict['sessionid']
        session = self.request.db
        state = (session.query(State)
                        .filter(State.session==sessionid)
                        .order_by(State.ts.desc()).first())
        if not state:
            gol = GameOfLife()
            gol.randomize(80,80)
            state = State(session=sessionid,value=gol._data)
            session.add(state)
            return list(flatten_grid(gol._data))

        step = int(self.request.params.get('step', '0'))
        if step:
            gol = GameOfLife(state.value)
            gol.step()
            state.value = gol._data
            session.add(state)
            return list(flatten_grid(gol._data))
        return list(flatten_grid(state.value))

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
