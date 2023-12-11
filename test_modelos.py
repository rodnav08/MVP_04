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
url_dados = "database/database_YT_test.csv"
colunas = ['subscribers', 'video views', 'uploads', 'Country', 'Category', 'video_views_for_the_last_30_days', 'highest_monthly_earnings','Pay well']

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

le = LabelEncoder()
dataset['Country'] = le.fit_transform(dataset['Country'])
dataset['Category'] = le.fit_transform(dataset['Category'])

# Separando em dados de entrada e saída
X_train, X_test, Y_train, Y_test = preprocessador.pre_processar(dataset = dataset, percentual_teste=0.2, seed=8)

    
# Método para testar o modelo de SVM a partir do arquivo correspondente
# O nome do método a ser testado necessita começar com "test_"
def test_modelo():  
    # Importando o modelo SVM
    path = 'ml_model/model.pkl'
    modelo_SVM = Model.carrega_modelo(path)
    scaler_path = 'ml_model/scaler.pkl'
    scaler = Model.carrega_modelo(scaler_path)

    # Obtendo as métricas da Regressão Logística
    acuracia_svm, recall_svm, precisao_svm, f1_svm = avaliador.avaliar(modelo_SVM, scaler, X_test, Y_test)

    # Testando as métricas
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_svm >= 0.9
    assert recall_svm >= 0.9
    assert precisao_svm >= 0.9
    assert f1_svm >= 0.9


