from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Youtuber, Model
from logger import logger
from schemas import *
from flask_cors import CORS

import pdb
# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)
# Ative o modo de depuração
app.debug = True

# Definindo tags para agrupamento das rotas
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
youtuber_tag = Tag(name="Youtuber", description="Adição, visualização, remoção e predição de sucesso de canais do Youtube")


# Rota home
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# Rota de listagem de canais do YouTube
@app.get('/youtubers', tags=[youtuber_tag],
         responses={"200": YoutuberViewSchema, "404": ErrorSchema})
def get_youtubers():
    """Lista todos os canais de youtube cadastrados na base
    Retorna uma lista de canais do youtube cadastrados na base.
    
    Args:
        nome (str): nome do canal do Youtube
        
    Returns:
        list: lista de canais do Youtube cadastrados na base
    """
    session = Session()
    
    # Buscando todos os youtubers
    youtubers = session.query(Youtuber).all()
    
    if not youtubers:
        logger.warning("Não há youtubers cadastrados na base :/")
        return {"message": "Não há youtubers cadastrados na base :/"}, 404
    else:
        logger.debug(f"%d youtubers econtrados" % len(youtubers))
        return apresenta_youtubers(youtubers), 200


# Rota de adição de canal do YouTube
@app.post('/youtuber', tags=[youtuber_tag],
          responses={"200": YoutuberViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def predict(form: YoutuberSchema):
    """Adiciona um novo youtuber à base de dados
    Retorna uma representação dos youtubers.
    
    Args:
            name: nome do canal
            subs: número de inscritos no canal do YouTube
            vidview: número total de views
            uploads: quantidade de uploads de vídeos realizados
            country: país de origem do canal
            category: categoria dos vídeos: Música, Entretenimento, Futebol, etc...
            video_views_30: número de views nos últimos 30 dias
            highest_earnings: Renda mais alta do último mês

    Returns:
        dict: representação do canal do YouTube e avaliação de sucesso.
    """
    
    # Carregando modelo
    ml_path = 'ml_model/model.pkl'
    modelo = Model.carrega_modelo(ml_path)
    
    youtuber = Youtuber(
        name=form.name.strip(),
        subs=form.subs, 
        vidview=form.vidview, 
        uploads=form.uploads, 
        country=form.country, 
        category=form.category, 
        video_views_30=form.video_views_30, 
        highest_earnings=form.highest_earnings, 
        outcome= Model.preditor(modelo, form)
    )
    
    logger.debug(f"Adicionando canal do Youtube de nome: '{youtuber.name}'")
    
    try:
        # Criando conexão com a base
        session = Session()
        
        # Checando se canal do YouTube já existe na base
        if session.query(Youtuber).filter(Youtuber.name == form.name).first():
            error_msg = "Canal de YouTube já existente na base :/"
            logger.warning(f"Erro ao adicionar canal do Youtube '{youtuber.name}', {error_msg}")
            return {"message": error_msg}, 409
        # Adicionando Canal do YouTube
        session.add(youtuber)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado canal do YouTube de nome: '{youtuber.name}'")
        return apresenta_youtuber(youtuber), 200
    
    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo canal de Youtube :/"
        logger.warning(f"Erro ao adicionar '{youtuber.name}', {error_msg}")
        return {"message": error_msg}, 400
    

# Métodos baseados em nome
# Rota de busca de canal do YouTube por nome
@app.get('/youtuber', tags=[youtuber_tag],
         responses={"200": YoutuberViewSchema, "404": ErrorSchema})
def get_youtuber(query: YoutuberBuscaSchema):    
    """Faz a busca por um canal do YouTube cadastrado na base a partir do nome

    Args:
        nome (str): nome do canal do YouTube
        
    Returns:
        dict: representação do canal do YouTube e resposta se o canal é bem sucedido ou não
    """
    
    youtuber_nome = query.name
    logger.debug(f"Coletando dados sobre Canal #{youtuber_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    youtuber = session.query(Youtuber).filter(Youtuber.name == youtuber_nome).first()
    
    if not youtuber:
        # se o canal do YouTube não foi encontrado
        error_msg = f"Canal do Youtube {youtuber_nome} não encontrado na base :/"
        logger.warning(f"Erro ao buscar canal '{youtuber_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Canal do Youtube econtrado: '{youtuber.name}'")
        # retorna a representação do canal do YouTube
        return apresenta_youtuber(youtuber), 200
   
    
# Rota de remoção de canal do YouTube por nome
@app.delete('/youtuber', tags=[youtuber_tag],
            responses={"200": YoutuberViewSchema, "404": ErrorSchema})
def delete_youtuber(query: YoutuberBuscaSchema):
    """Remove um canal de Youtube cadastrado na base a partir do nome

    Args:
        nome (str): nome do canal do YouTube
        
    Returns:
        msg: Mensagem de sucesso ou erro
    """
    
    youtuber_nome = unquote(query.name)
    logger.debug(f"Deletando dados sobre canal do Youtube #{youtuber_nome}")
    
    # Criando conexão com a base
    session = Session()
    
    # Buscando canal do Youtube
    youtuber = session.query(Youtuber).filter(Youtuber.name == youtuber_nome).first()
    
    if not youtuber:
        error_msg = "Canal do YouTube não encontrado na base :/"
        logger.warning(f"Erro ao deletar canal '{youtuber_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(youtuber)
        session.commit()
        logger.debug(f"Deletado canal do YouTube #{youtuber_nome}")
        return {"message": f"Canal do YouTube {youtuber_nome} removido com sucesso!"}, 200