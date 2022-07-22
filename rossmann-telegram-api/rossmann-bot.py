import json
import requests
import pandas as pd


def load_dataset(store_id):
    # Carregando o dataset de teste
    df10 = pd.read_csv(
        "C:/Users/Baby/Documents/Python/repos/ds_em_producao/rossmann_sales_prediction/data/test.csv"
    )
    df_store_raw = pd.read_csv(
        "C:/Users/Baby/Documents/Python/repos/ds_em_producao/rossmann_sales_prediction/data/store.csv"
    )

    # Juntanto o dataset de teste e o das lojas
    df_test = pd.merge(df10, df_store_raw, on="Store", how="left")

    # Selecionando as lojas para rodar no modelo
    df_test = df_test[df_test["Store"] == store_id]

    # Remove os dias fechados e a coluna id
    df_test = df_test[df_test["Open"] != 0]
    df_test = df_test[~df_test["Open"].isnull()]
    df_test = df_test.drop("Id", axis=1)

    # Converter o dataframe para json usando a orientação (tipo) records
    data = json.dumps(df_test.to_dict(orient="records"))

    return data


def get_predict():
    # Chamada da API HEROKU
    url = "https://rossmann-store.herokuapp.com/rossmann/predict"
    header = {"Content-type": "application/json"}
    data = data
    r = request.post(url, data=data, headers=header)
    print(f"Status code {r.status_code}")

    # Conversão de json para dataframe
    d1 = pd.DataFrame(r.json, columns=r.json()[0].keys())

    return d1


# d2 = d1[["store", "prediction"]].groupby("store").sum().reset_index()

# # Imprimindo o resultado da predição
# for i in range(len(d2)):
#     print(
#         "Store number {} will sell £$ {:,.2f} in the next 6 weeks".format(
#             d2.loc[i, "store"], d2.loc[i, "prediction"]
#         )
#     )
