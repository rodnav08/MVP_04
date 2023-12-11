from pydantic import BaseModel
from typing import Optional, List
from model.youtuber import Youtuber
import json
import numpy as np

class YoutuberSchema(BaseModel):
    """ Define como um novo youtuber a ser inserido deve ser representado
    """
    name: str = "Mangaq"
    subs: int =  26800674545
    vidview: int =303780000
    uploads: int = 750
    country: str = "Brazil"
    category: str = "Entertainment"
    video_views_30: int = 815949000
    highest_earnings: float = 2400000.00

    
class YoutuberViewSchema(BaseModel):
    """Define como um Youtuber será retornado
    """
    id: int = 1
    name: str = "Mangaq"
    subs: int =  26800674545
    vidview: int =303780000
    uploads: int = 750
    country: str = "Brazil"
    category: str = "Entertainment"
    video_views_30: int = 815949000
    highest_earnings: float = 2400000.00
    outcome: int = None
    
class YoutuberBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no nome do canal do Youtuber.
    """
    name: str = "Mangaq"

class ListaYoutuberSchema(BaseModel):
    """Define como uma lista de youtuber será representada
    """
    youtuber: List[YoutuberSchema]

    
class YoutuberDelSchema(BaseModel):
    """Define como um youtuber para deleção será representado
    """
    name: str = "Mangaq"
    
# Apresenta apenas os dados de um youtuber    
def apresenta_youtuber(youtuber: Youtuber):
    """ Retorna uma representação do youtuber seguindo o schema definido em
        YoutuberViewSchema.
    """
    return {
            "id": youtuber.id,
            "name": youtuber.name,
            "subs": youtuber.subs,
            "vidview": youtuber.vidview,
            "uploads": youtuber.uploads,
            "country": youtuber.country,
            "category": youtuber.category,
            "video_views_30": youtuber.video_views_30,
            "highest_earnings": youtuber.highest_earnings,
            "outcome": youtuber.outcome
        }
    
# Apresenta uma lista de youtubers
def apresenta_youtubers(youtubers: List[Youtuber]):
    """ Retorna uma representação do youtuber seguindo o schema definido em
        YoutuberViewSchema.
    """
    result = []
    for youtuber in youtubers:
        result.append({
            "id": youtuber.id,
            "name": youtuber.name,
            "subs": youtuber.subs,
            "vidview": youtuber.vidview,
            "uploads": youtuber.uploads,
            "country": youtuber.country,
            "category": youtuber.category,
            "video_views_30": youtuber.video_views_30,
            "highest_earnings": youtuber.highest_earnings,
            "outcome": youtuber.outcome
        })

    return {"youtubers": result}

