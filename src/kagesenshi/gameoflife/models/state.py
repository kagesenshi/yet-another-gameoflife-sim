from . import Base
from sqlalchemy import Column
from sqlalchemy import Unicode
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import Text
from datetime import datetime
import json

class State(Base):
    __tablename__ = 'state'
    ts = Column(DateTime, primary_key=True)
    session = Column(Text)
    encoded_value = Column(Text)
    living_cells = Column(Integer)
    dead_cells = Column(Integer)
    total_cells = Column(Integer)

    def __init__(self, session, value):
        self.ts = datetime.now()
        self.session = session
        self.value = value
        all_ = []
        for r in value:
            all_ += r
        self.total_cells = len(all_)
        self.living_cells = sum(all_)
        self.dead_cells = len(all_) - sum(all_)

    def _get_value(self):
        return json.loads(self.encoded_value)

    def _set_value(self, value):
        self.encoded_value = json.dumps(value)

    value = property(_get_value, _set_value)
