import numpy as np
import pickle


class Model:
    
    def carrega_modelo(path):
        """Dependendo se o final for .pkl ou .joblib, carregamos de uma forma ou de outra
        """
        if path.endswith('.pkl'):
            model = pickle.load(open(path, 'rb'))
        else:
            raise Exception('Formato de arquivo não suportado')
        return model
    
    def preditor(model,scaler, form):
        """Realiza a predição se um youtuber ganha bem com base no modelo treinado
        """
        lista_country = ["Afghanistan", "Andorra", "Argentina", "Australia", "Bangladesh", "Barbados",
        "Brazil", "Canada", "Chile", "China", "Colombia", "Cuba", "Ecuador", "Egypt",
        "El Salvador", "Finland", "France", "Germany", "Global", "India", "Indonesia",
        "Iraq", "Italy", "Japan", "Jordan", "Kuwait", "Latvia", "Malaysia", "Mexico",
        "Morocco", "nan", "Netherlands", "Pakistan", "Peru", "Philippines", "Russia",
        "Samoa", "Saudi Arabia", "Singapore", "South Korea", "Spain", "Sweden",
        "Switzerland", "Thailand", "Turkey", "Ukraine", "United Arab Emirates",
        "United Kingdom", "United States", "Venezuela", "Vietnam"]

        lista_category = ["Animals", "Autos", "Comedy", "Education", "Entertainment", "Film", "Games",
        "Howto", "Music", "News", "Nonprofit", "People", "Sports", "Tech"]
        
        # Obtém os índices dos país de origem do canal do Youtube e a Cateogria dos videos na lista
        country_index = lista_country.index(form.country)
        category_index = lista_category.index(form.category)
        

        X_input = np.array([form.subs, 
                            form.vidview, 
                            form.uploads, 
                            country_index, 
                            category_index, 
                            form.video_views_30, 
                            form.highest_earnings
                            
                        ])
        X_input_scaled = scaler.transform(X_input.reshape(1, -1))
        # Faremos o reshape para que o modelo entenda que estamos passando
        diagnosis = model.predict(X_input_scaled)
        return int(diagnosis[0])
