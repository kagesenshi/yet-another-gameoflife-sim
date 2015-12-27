from pyramid.view import view_config
from pysiphae.views import Views as BaseViews
from sqlalchemy.engine import create_engine
from pyramid.exceptions import NotFound
from wraptor.decorators import memoize
from sqlalchemy.sql import text

class Views(BaseViews):

    @view_config(route_name='kagesenshi.gameoflife', renderer='templates/default.pt')
    def default_view(self):
        return { 'page_header': 'kagesenshi.gameoflife Dashboard' }
