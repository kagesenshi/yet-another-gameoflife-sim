from . import Base
from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import Text
from datetime import datetime
import json
from shortid import ShortId

class ShortUrl(Base):
    __tablename__ = 'shorturl'
    short_id = Column(Unicode(255), primary_key=True)
    ts = Column(DateTime)
    url = Column(Text)

    def __init__(self, url):
        self.ts = datetime.now()
        self.url = url
        sid = ShortId()
        self.short_id = sid.generate()
