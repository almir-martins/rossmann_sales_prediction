# Classe Rossmann
import math
import pickle
import datetime
import inflection
import numpy as np
import pandas as pd


class Rossmann(object):
    def __init__(self):
        # O caminho precisa ser absoluto pois trata-se de arquivos no servidor
        self.home_path = "C:/Users/Baby/Documents/Python/repos/ds_em_producao/rossmann_sales_prediction/"
        self.competition_distance_scaler = pickle.load(
            open(self.home_path + "parameter/competition_distance_scaler.pkl", "rb")
        )
        self.promo_time_week_scaler = pickle.load(
            open(self.home_path + "parameter/promo_time_week_scaler.pkl", "rb")
        )
        self.competition_time_month_scaler = pickle.load(
            open(self.home_path + "parameter/competition_time_month_scaler.pkl", "rb")
        )
        self.year_scaler = pickle.load(
            open(self.home_path + "parameter/year_scaler.pkl", "rb")
        )
        self.store_type_scaler = pickle.load(
            open(self.home_path + "parameter/store_type_scaler.pkl", "rb")
        )

    def data_cleaning(self, df1):
        # 1.0. PASSO 1 - DESCRIÇÃO DOS DADOS
        ## 1.1. Rename Columns
        # colunas originais do dataset pego com ctrl-c no columns
        col_old = [
            "Store",
            "DayOfWeek",
            "Date",
            "Open",
            "Promo",
            "StateHoliday",
            "SchoolHoliday",
            "StoreType",
            "Assortment",
            "CompetitionDistance",
            "CompetitionOpenSinceMonth",
            "CompetitionOpenSinceYear",
            "Promo2",
            "Promo2SinceWeek",
            "Promo2SinceYear",
            "PromoInterval",
        ]

        # Usando a função underscore da biblioteca inflection para substituir camelCase por snake_case
        col_new = list(map(lambda x: inflection.underscore(x), col_old))
        df1.columns = col_new

        # 1.3. Data Types
        df1["date"] = pd.to_datetime(df1["date"])

        # 1.5. FILLOUT NA
        # Preenchendo valores faltantes de competition_distance
        df1["competition_distance"] = df1["competition_distance"].apply(
            lambda x: 200000 if math.isnan(x) else x
        )

        # Preenchendo valores faltantes de competition_open_since_month
        df1["competition_open_since_month"] = df1.apply(
            lambda x: x["date"].month
            if math.isnan(x["competition_open_since_month"])
            else x["competition_open_since_month"],
            axis=1,
        )

        # Preenchendo valores faltantes de competition_open_since_year
        df1["competition_open_since_year"] = df1.apply(
            lambda x: x["date"].year
            if math.isnan(x["competition_open_since_year"])
            else x["competition_open_since_year"],
            axis=1,
        )

        # Preenchendo valores faltantes de promo2_since_week
        df1["promo2_since_week"] = df1.apply(
            lambda x: x["date"].week
            if math.isnan(x["promo2_since_week"])
            else x["promo2_since_week"],
            axis=1,
        )

        # Preenchendo valores faltantes de promo2_since_year
        df1["promo2_since_year"] = df1.apply(
            lambda x: x["date"].year
            if math.isnan(x["promo2_since_year"])
            else x["promo2_since_year"],
            axis=1,
        )

        # Preenchendo valores faltantes de promo_interval
        # Criando um dicionário para auxiliar
        # Na aula foi usado Fevereiro == Fev e Setembro == Sep mas
        # no dataset está Fevereiro == Feb e Setembro == Sept
        month_map = {
            1: "Jan",
            2: "Fev",
            3: "Mar",
            4: "Apr",
            5: "May",
            6: "Jun",
            7: "Jul",
            8: "Aug",
            9: "Sep",
            10: "Oct",
            11: "Nov",
            12: "Dec",
        }

        # Completa com zeros os valores faltantes
        df1["promo_interval"].fillna(0, inplace=True)
        # Coluna que recebe o mês (num) de df['date'] convertido para a sigla
        df1["month_map"] = df1["date"].dt.month.map(month_map)
        # Recebe 1 caso o mês de month_map esteja em promo_interval caso contrário 0
        df1["is_promo"] = df1.apply(
            lambda x: 0
            if x["promo_interval"] == 0
            else 1
            if x["month_map"] in x["promo_interval"].split(",")
            else 0,
            axis=1,
        )

        # 1.6. Change Types
        # Alterando os tipos de dados
        df1["competition_open_since_month"] = df1[
            "competition_open_since_month"
        ].astype("int64")
        df1["competition_open_since_year"] = df1["competition_open_since_year"].astype(
            "int64"
        )
        df1["promo2_since_week"] = df1["promo2_since_week"].astype("int64")
        df1["promo2_since_year"] = df1["promo2_since_year"].astype("int64")

        return df1

    def feature_engineering(self, df2):

        # 2.4. Feature Engineering
        # year
        df2["year"] = df2["date"].dt.year

        # month
        df2["month"] = df2["date"].dt.month

        # day
        df2["day"] = df2["date"].dt.day

        # week of year
        df2["week_of_year"] = df2["date"].dt.weekofyear

        # year week
        df2["year_week"] = df2["date"].dt.strftime("%Y-%W")

        # competition since
        df2["competition_since"] = df2.apply(
            lambda x: datetime.datetime(
                year=x["competition_open_since_year"],
                month=x["competition_open_since_month"],
                day=1,
            ),
            axis=1,
        )

        df2["competition_time_month"] = (
            ((df2["date"] - df2["competition_since"]) / 30)
            .apply(lambda x: x.days)
            .astype(int)
        )

        # promo since
        df2["promo_since"] = (
            df2["promo2_since_year"].astype(str)
            + "-"
            + df2["promo2_since_week"].astype(str)
        )
        df2["promo_since"] = df2["promo_since"].apply(
            lambda x: datetime.datetime.strptime(x + "-1", "%Y-%W-%w")
            - datetime.timedelta(days=7)
        )
        df2["promo_time_week"] = (
            ((df2["date"] - df2["promo_since"]) / 7).apply(lambda x: x.days).astype(int)
        )

        # assortment
        df2["assortment"] = df2["assortment"].apply(
            lambda x: "basic" if x == "a" else "extra" if x == "b" else "extended"
        )

        # state holiday
        df2["state_holiday"] = df2["state_holiday"].apply(
            lambda x: "public_holiday"
            if x == "a"
            else "easter_holiday"
            if x == "b"
            else "christmas"
            if x == "c"
            else "regular_day"
        )

        # 3.0. PASSO 3 - FILTRAGEM DE VARIÁVEIS
        # 3.1. Filtragem de linhas
        # Apagar as linhas não utilizadas
        df2 = df2[df2["open"] != 0]

        # 3.2. Filtragem de colunas
        # Apagar as colunas não utilizadas
        drop_col = ["open", "promo_interval", "month_map"]
        df2.drop(drop_col, inplace=True, axis=1)

        return df2

    def data_preparation(self, df5):
        # 5.0. PASSO 5 - DATA PREPARATION
        ## 5.2. Rescaling
        # Fazendo o rescaling das features
        # competition_distance
        df5["competition_distance"] = self.competition_distance_scaler.fit_transform(
            df5[["competition_distance"]].values
        )

        # competition_time_month
        df5[
            "competition_time_month"
        ] = self.competition_time_month_scaler.fit_transform(
            df5[["competition_time_month"]].values
        )

        # promo_time_week
        df5["promo_time_week"] = self.promo_time_week_scaler.fit_transform(
            df5[["promo_time_week"]].values
        )

        # year
        df5["year"] = self.year_scaler.fit_transform(df5[["year"]].values)

        # 5.3. Transformação
        # 5.3.1. Encoding
        # state_holiday - Aplicando o One Hot Encoding
        df5 = pd.get_dummies(df5, prefix=["state_holiday"], columns=["state_holiday"])

        # store_type - Aplicando o Label Encoding
        df5["store_type"] = self.store_type_scaler.fit_transform(df5["store_type"])

        # assortment - Aplicando o Ordinal Encoding
        assortment_dict = {"basic": 1, "extra": 2, "extended": 3}
        df5["assortment"] = df5["assortment"].map(assortment_dict)

        # 5.3.2. Nature Transformation
        # Transformação das features de natureza cíclica
        # month
        df5["month_sin"] = df5["month"].apply(lambda x: np.sin(x * (2.0 * np.pi / 12)))
        df5["month_cosin"] = df5["month"].apply(
            lambda x: np.cos(x * (2.0 * np.pi / 12))
        )

        # day
        df5["day_sin"] = df5["day"].apply(lambda x: np.sin(x * (2.0 * np.pi / 30)))
        df5["day_cosin"] = df5["day"].apply(lambda x: np.cos(x * (2.0 * np.pi / 30)))

        # week_of_year
        df5["week_of_year_sin"] = df5["week_of_year"].apply(
            lambda x: np.sin(x * (2.0 * np.pi / 52))
        )
        df5["week_of_year_cosin"] = df5["week_of_year"].apply(
            lambda x: np.cos(x * (2.0 * np.pi / 52))
        )

        # day_of_week
        df5["day_of_week_sin"] = df5["day_of_week"].apply(
            lambda x: np.sin(x * (2.0 * np.pi / 7))
        )
        df5["day_of_week_cosin"] = df5["day_of_week"].apply(
            lambda x: np.cos(x * (2.0 * np.pi / 7))
        )

        cols_selected = [
            "store",
            "promo",
            "store_type",
            "assortment",
            "competition_distance",
            "competition_open_since_month",
            "competition_open_since_year",
            "promo2",
            "promo2_since_week",
            "promo2_since_year",
            "competition_time_month",
            "promo_time_week",
            "month_sin",
            "month_cosin",
            "day_sin",
            "day_cosin",
            "week_of_year_sin",
            "week_of_year_cosin",
            "day_of_week_sin",
            "day_of_week_cosin",
        ]

        return df5[cols_selected]

    def get_prediction(self, model, original_data, test_data):
        # Prediction
        pred = model.predict(test_data)

        # Juntar a coluna de predição (target) ao dataframe original enviada
        original_data["prediction"] = np.expm1(pred)

        # Passando para o formato json para responder ao request e colocando datas no formato ISO
        return original_data.to_json(orient="records", date_format="iso")
