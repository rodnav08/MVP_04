from sqlalchemy import Column, String, Integer,DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

# colunas = Name,Subscribers,Video Views,Uploads,Country,Category,Last Views,Earnings,Outcome

class Youtuber(Base):
    __tablename__ = 'youtuber'
    
    id = Column(Integer, primary_key=True)
    name = Column("Name", String(50))
    subs= Column("Subscribers", Integer)
    vidview = Column("Video Views", Integer)
    uploads = Column("Uploads", Integer)
    country = Column("Country", String(50))
    category = Column("Category", String(50))
    video_views_30 = Column("Views", Integer)
    highest_earnings = Column("Earnings", Float)
    outcome = Column("Pays Well", Integer, nullable=True)
    
    
    def __init__(self, name:str,subs:int, vidview:int, uploads:int, country:str,
                 category:str, video_views_30:int, highest_earnings:float,outcome:int):
        """
        Cria um Youtuber

        Arguments:
            name: nome do canal
            subs: número de inscritos no canal do YouTube
            vidview: número total de views
            uploads: quantidade de uploads de vídeos realizados
            country: país de origem do canal
            category: categoria dos vídeos: Música, Entretenimento, Futebol, etc...
            video_views_30: número de views nos últimos 30 dias
            highest_earnings: Renda mais alta do último mês
        """
        self.name = name
        self.subs = subs
        self.vidview = vidview
        self.uploads = uploads
        self.country = country
        self.category = category
        self.video_views_30 = video_views_30
        self.highest_earnings = highest_earnings
        self.outcome = outcome
