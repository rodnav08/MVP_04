from model.avaliador import Avaliador
from model.carregador import Carregador
from model.preprocessador import PreProcessador
from model.modelo import Model
from sklearn.preprocessing import LabelEncoder

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
#modelo = Model()
avaliador = Avaliador()
preprocessador = PreProcessador()

# Parâmetros    
url_dados = "database/database_YT.csv"
colunas = ['subscribers', 'video views', 'uploads', 'Country', 'Category', 'video_views_for_the_last_30_days', 'highest_monthly_earnings','Pay well']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

le = LabelEncoder()
dataset['Country'] = le.fit_transform(dataset['Country'])
dataset['Category'] = le.fit_transform(dataset['Category'])

# Separando em dados de entrada e saída
X_train, X_test, Y_train, Y_test = preprocessador.pre_processar(dataset, percentual_teste=0.9, seed=8)

    
# Método para testar o modelo de Arvore de Decisão a partir do arquivo correspondente
# O nome do método a ser testado necessita começar com "test_"
def test_modelo():  
    # Importando o modelo KNN
    path = 'ml_model/model.pkl'
    modelo_catr = Model.carrega_modelo(path)

    # Obtendo as métricas da Regressão Logística
    acuracia_catr = avaliador.avaliar(modelo_catr, X_test, Y_test)
    
    # Testando as métricas da Regressão Logística 
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_catr >= 0.8


