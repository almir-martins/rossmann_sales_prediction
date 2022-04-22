# Previsão de vendas para rede de drogarias Rossmann

![Rossmann Store](https://raw.githubusercontent.com/almir-martins/rossmann_sales_prediction/main/img/rossmann_markt.jpg)

# 1 - Sobre a Rossmann Drugstore

## 1.1 - Contexto do Negócio

A Rossmann é uma das maiores redes de drogarias da Europa com cerca de 56.200 funcionários e mais de 4.000 lojas. Em 2019 a Rossmann teve um faturamento de mais de € 10 bilhões na Alemanha, Polônia, Hungria, República Tcheca, Turquia, Albânia, Kosovo e Espanha. A companhia está em grande expansão e num ritmo elevado, com investimentos para serem utilizados nas mais diversas áreas. Dessa forma é muito importante que a gestão da empresa consiga fazer uma previsão de vendas para um determinado intervalo de tempo no futuro.

## 1.2 - Problema do Negócio

A rede Rossmann pretende renovar a fachada das lojas alterando sua identidade visual com intuito de melhorar sua imagem e vincular a marca à suas novas metas e valores. O setor financeiro da rede solcitou aos gerentes de cada loja que façam uma previsão das vendas diárias para seis semanas no futuro, para calcular o impacto financeiro da medida. As vendas de cada loja são influenciadas por muitos fatores, entre eles: promoções, concorrência, feriados, sazonalidade e localização. Com milhares de gerentes fazendo suas predições baseado nas circunstâncais de sua loja a acurácia dos resultados pode ser bastante variada e assim a tarefa se torna um grande desafio para a rede.

## 1.3 - Sobre os dados

Para solucionar o problema acima a empresa disponibilizou o histórico de vendas de 1.115 lojas no [Kaggle](https://www.kaggle.com/c/rossmann-store-sales). O histórico consiste em um Dataset com os dados de vendas destas lojas de 2015 até 2017, lembrando que algumas lojas do dataset estão fechadas temprariamente para reforma. O dataset apresenta as seguintes features:

| Atributos | Descrição |
| ------ | ------- |
| Id | Identificador da transação |
| Store | Identificador único para cada loja |
| Sales | Volume de vendas no dia (Variável target) |
| Customers | Número de clientes no dia |
| Open | Indica se a loja está aberta ou fechada |
| StateHoliday | Indica feriado estadual, algumas lojas fecham nos feriados |
| SchoolHoliday | Indica feriado escolar |
| StoreType | Tipo da loja |
| Assortment | Indica o nível de variedade de produtos da loja |
| CompetitionDistance | Distância em metros do concorrente mais próximo |
| CompetitionOpenSince | Mês e ano que abriu o concorrente mais próximo |
| Promo | Indica se está ocorrendo alguma promoção na loja |
| Promo2 | Indica se o prazo final da promoção foi extendido |
| Promo2Since | Indica mês e ano que a loja iniciou a Promo2 |
| PromoInterval | Indica os intervalos consecutivos em que a Promo2 é iniciada |

## 3 - Business Assumptions

- All stores contain a basic sortment, but some of them contain (different kinds of) extra sortments.
- The store's opening on weekends and holidays vary from place to place.
- The stores participate in seasonal promotions. In some of these cases, the promotion is continued for a longer time.

## 4 - Solution Strategy

The strategy adopted was the following:

Step 01. Data Description: I searched for NAs, checked data types (and adapted some of them for analysis) and presented a statistical description.

Step 02. Feature Engineering: New features were created to make possible a more thorough analysis.

Step 03. Data Filtering: Entries containing no information or containing information which does not match the scope of the project were filtered out.

Step 04. Exploratory Data Analysis: I performed univariate, bivariate and multivariate data analysis, obtaining statistical properties of each of them, correlations and testing hypothesis (the most important of them are detailed in the following section).

Step 05. Data Preparation: Numerical data was rescaled, categorical data was transformed and cyclic data (such as months, weeks and days) was transformed using mathematical trigonometrical functions.

Step 06. Feature selection: The statistically most relevant features were selected using the Boruta package.

Step 07. Machine learning modelling: Some machine learning models were trained. The one that presented best results after cross-validation went through a further stage of hyperparameter fine tunning to optimize the model's generalizability.

Step 08. Model-to-business: The models performance is converted into business values.

Step 09. Deploy Model to Production: The model is deployed on a cloud environment to make possible that other stakeholders and services access its results.
5 Top 3 Data insights

    Stores with larger assortment do not sell more.
    Stores with closer competitors do sell more.
    Stores sell less at school holidays (except during summer).

## 6 - Machine Learning Model Applied

The following machine learning models were trained:

- Linear Regression;
- Regularized Linear Regression;
- Random Forest Regressor;
- XGBoost Regressor.

All of them were cross-validated and their performance was compared against a random model.

## 7  - Machine Learning Model Performance

The performance of every trained model, after cross-validation. The columns correspond to the metrics: Mean Absolute Error, Mean Absolute Percentage Error and Root Mean Squared Error.

picture alt

## 8 - Conclusions

The sales forecast and the generated insights provide the CEO with valuable tools to decide the amount of budget that is going to be dedicated to the restoration of each store.
9 Lessons Learned

- The exploratory data analysis provides important insights to the business problem, many of which contradict the initial hypothesis. This information is valuable for the understanding of business and for planning future actions. This step also provides a preview of the result of the feature selection step.
- The machine learning model performance must be evaluated in the learning and generalization stages. A balance between bias and variance must be achieved based on the uniqueness of the problem.

## 10 - Next steps and improvements

Some hypothesis made when filling missing data would be reviewed in a following CRISP cycle, and other ones would be tested in the exploratory data analysis step. Also, other machine learning models would be employed (in particular, gradient boost models).

Besides, the model is deployed to production in an App at Heroku. One can send a request from an external application (such as Postman, for example). The app receives a JSON file and returns the sales forecast for the following six weeks (the amount is displayed in the Brazilian currency BRL). This app is also receiving requests from another app hooked to a Telegram Bot. In this case, one must only pass the number of the store to the Bot to obtain the sales forecast. This second App is also hosted at Heroku.

Este repositório contém código para a previsão de vendas da rede de drogarias Rossmann. Os dados usados estão disponíveis no [Kaggle](https://www.kaggle.com/c/rossmann-store-sales). Todas as informações adicionais foram criadas para dar contexto ao problema.
