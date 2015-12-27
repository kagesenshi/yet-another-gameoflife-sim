from pysiphae.interfaces import IConfigurator
from zope.interface import implements
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from .models import initialize_sql

def db(request):
    maker = request.registry.dbmaker
    session = maker()

    def cleanup(request):
        if request.exception is not None:
            session.rollback()
        else:
            session.commit()
        session.close()
    request.add_finished_callback(cleanup)

    return session

class SQLAlchemyConfigurator(object):
    implements(IConfigurator)

    def configure(self, config, settings):
        engine = engine_from_config(settings, prefix='sqlalchemy.')
        config.registry.dbmaker = sessionmaker(bind=engine)
        config.add_request_method(db, reify=True)
        initialize_sql(engine)
        import pdb;pdb.set_trace()
