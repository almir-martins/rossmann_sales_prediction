import pickle
import pandas as pd
from flask import Flask, request, Response
from rossmann.Rossmann import Rossmann

# Carregando o modelo salvo anteriormente
model = pickle.load(
    open(
        "C:/Users/Baby/Documents/Python/repos/ds_em_producao/rossmann_sales_prediction/model/model_rossmann.pkl",
        "rb",
    )
)

# Inicializando a API
app = Flask(__name__)

# URL a ser chamada e o método do request
@app.route("/rossmann/predict", methods=["POST"])
def rossmann_predict():
    # Pega o json que veio na requisição
    test_json = request.get_json()

    # Se o json tiver dados
    if test_json:
        # Se os dados são um dicionário (uma única linha)
        if isinstance(test_json, dict):
            test_raw = pd.DataFrame(test_json, index=[0])
        else:  # Se os dados são várias linhas
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())

        # Instanciando a classe Rossmann
        pipeline = Rossmann()
        
        # Limpando os dados
        df1 = pipeline.data_cleaning(test_raw)

        # Fazendo feature engineering
        df2 = pipeline.feature_engineering(df1)

        # Fazendo a transformação dos dados
        df3 = pipeline.data_preparation(df2)

        # Fazendo a predição
        df_response = pipeline.get_prediction(model, test_raw, df3)

        return df_response

    # Se o json não tiver dados
    else:
        return Response("{}", status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run("0.0.0.0")
    app.run(debug=True)