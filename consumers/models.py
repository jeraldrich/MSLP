from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP


Base = declarative_base()


class ChatMessage(Base):
    __tablename__ = 'chat_messages'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column('id', String(255), primary_key=True)
    _from = Column('from', String(255), nullable=False)
    _type = Column('type', String(50))
    site_id = Column('site_id', String(50), nullable=False, index=True)
    data = Column('data', String(255), default='')
    timestamp = Column('timestamp', TIMESTAMP, nullable=False, index=True)

    def __repr__(self):
        return "id='{id}',ts='{ts}',type='{t}',data='{data}'>".format(
            id=self.id,
            ts=self.timestamp,
            t=self._type,
            data=self.data,
        )
