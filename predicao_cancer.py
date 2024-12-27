# -*- coding: utf-8 -*-
"""predicao_cancer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CQa_gsk0lpCCubzeQGVyq8PR-B1gxr1N

Bibliotecas necessárias
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.decomposition import PCA

"""Leitura dos dados"""

df = pd.read_csv("brca_mirnaseq.csv", sep = ';', header =0,decimal =',')
df

df.shape #Analisar tamanho (linhas,colunas)

"""Análise exploratória

"""

ax = sns.countplot(x = 'class', data = df) #Criando gráfico de barras para ver a != de TP e NT

df['class'].value_counts() #Verificando a quantidade de TP e NT

"""Está desbalanceado"""

df['class'].value_counts(normalize = True) #Verificando a % de TP e NT

df.describe() #Verificando estatísticas básicas

"""Valores muito diferentes

Estabelecer baseline comparativo - uma solução simples
"""

x = df.drop(columns = 'class') #todas as colunas exceto class = variável alvo,x agora contém todas as variáveis independentes (features), ou seja, os atributos que serão usados para treinar o modelo.
y = df['class'] #variável dependente (target)
x_train, x_test, y_train, y_test = train_test_split(x,y, test_size = 0.30, stratify=y, random_state= 42) #30% p/ teste e 70% treino = quanto vai aprender, stratify garante que a proporção de classes no conjunto de treino e teste seja a mesma que no dataset original

y_train.value_counts(normalize = True) #Nota-se que o stratify está ok

y_test.value_counts(normalize = True)

#Usando o modelo de classificação = regressão logística
lr = LogisticRegression(random_state=42)
cv_list_lr = cross_val_score(lr, x_train, y_train, cv=10, scoring='balanced_accuracy') #Pega a lr e o conjunto e faz uma validação cruzada, p/ testar o modelo, garante generalização e não memorização
cv_list_lr
#cv = 10, numero de divisões , scoring = métrica de avaliação

mean_cv_lr = np.mean(cv_list_lr)
std_cv_lr = np.std(cv_list_lr)
print(F"Acurácia média da regressão logística com validação cruzada: {mean_cv_lr:.3f}")
print(F"Desvio padrão da regressão logística com validação cruzada: {std_cv_lr:.3f}")

"""Outro modelo de classificação = knn"""

knn = Pipeline(
    [
        ('mms', MinMaxScaler()),
        ('skb', SelectKBest(chi2, k=10)), #SELECIONA AS 10 FEATURES MAIS IMPORTANTES
        ('knn', KNeighborsClassifier(
            n_neighbors=3,
            p=2, #distancia euclidiana
            weights='uniform', #peso uniforme
        )),
    ]
)

cv_list_knn = cross_val_score(knn, x_train, y_train, cv=10, scoring='balanced_accuracy')

mean_cv_knn = np.mean(cv_list_knn)
std_cv_knn = np.std(cv_list_knn)
print(  F"Acurácia média do kNN : {mean_cv_knn:.3f}")
print(  F"Desvio padrão do kNN : {std_cv_knn:.3f}")

"""Knn com distancia de manhattan"""

knn = Pipeline(
    [
        ('mms', MinMaxScaler()),
        ('skb', SelectKBest(chi2, k=10)), #SELECIONA AS 10 FEATURES MAIS IMPORTANTES
        ('knn', KNeighborsClassifier(
            n_neighbors=3,
            p=1, #manhatan= mede apenas horizontal e vertical, mede os passos como andar a pe de um vizinho a outro
            weights='uniform', #peso uniforme
        )),
    ]
)

cv_list_knn_man = cross_val_score(knn, x_train, y_train, cv=10, scoring='balanced_accuracy')

mean_cv_knn_man = np.mean(cv_list_knn_man)
std_cv_knn_man = np.std(cv_list_knn_man)
print(  F"Acurácia média do kNN com manhattan: {mean_cv_knn_man:.3f}")
print(  F"Desvio padrão do kNN com manhattan: {std_cv_knn_man:.3f}")

"""Tentando melhorar a regressão logistica e a convergingo a mesma"""

lr = Pipeline(
    [
        ('scaler', StandardScaler()),
        ('lr', LogisticRegression(random_state=42, penalty='l2' #para evitar overfitting, reduz a influencia de variaveis n importantes
                                  , C=1, #regularização
                                  fit_intercept=True, class_weight='balanced')),
    ]
)

cv_list_lr_l2 = cross_val_score(lr, x_train, y_train, cv=10, scoring='balanced_accuracy')

mean_cv_lr_l2 = np.mean(cv_list_lr_l2)
std_cv_lr_l2 = np.std(cv_list_lr_l2)
print(F"Acurácia média da regressão logística: {mean_cv_lr_l2:.3f}")
print(F"Desvio padrão da regressão logística : {std_cv_lr_l2:.3f}")

lr = Pipeline(
    [
        ('scaler', StandardScaler()),
        ('lr', LogisticRegression(random_state=42, penalty='l1' #para evitar overfitting, ignora os nao importantes
                                  , C=1, #regularização
                                  fit_intercept=True, class_weight='balanced', solver= 'liblinear')),
    ]
)

cv_list_lr_l1 = cross_val_score(lr, x_train, y_train, cv=10, scoring='balanced_accuracy')

mean_cv_lr_l1 = np.mean(cv_list_lr_l1)
std_cv_lr_l1 = np.std(cv_list_lr_l1)
print(F"Acurácia média da regressão logística : {mean_cv_lr_l1:.3f}")
print(F"Desvio padrão da regressão logística : {std_cv_lr_l1:.3f}")

"""Análise de componente prncipal PCA - tentando preservar as informações"""

lr = Pipeline(
    [
        ('scaler', StandardScaler()),
        ('pca',PCA(n_components=10)),
        ('lr', LogisticRegression(random_state=42, penalty='l2' #para evitar overfitting, reduz a influencia de variaveis n importantes
                                  , C=1, #regularização
                                  fit_intercept=True, class_weight='balanced')),
    ])

cv_list_lr_pca = cross_val_score(lr, x_train, y_train, cv=10, scoring='balanced_accuracy')
mean_cv_lr_pca = np.mean(cv_list_lr_pca)
std_cv_lr_pca = np.std(cv_list_lr_pca)
print(F"Acurácia média PCA: {mean_cv_lr_pca:.3f}")
print(F"Desvio padrão PCA: {std_cv_lr_pca:.3f}")

"""Avaliação Experimental"""

# Criando o DataFrame
df_results = pd.DataFrame(
    {
        'knn': cv_list_knn,
        'knn_man': cv_list_knn_man,
        'lr': cv_list_lr,
        'lr_l1': cv_list_lr_l1,
        'lr_l2': cv_list_lr_l2,
        'lr_pca': cv_list_lr_pca
    }
)

# Boxplot
plt.figure(figsize=(10, 6))
sns.boxplot(data=df_results)
plt.title('Boxplot da Acurácia dos Modelos')
plt.ylabel('Acurácia')
plt.show()

# Violin plot
plt.figure(figsize=(10, 6))
sns.violinplot(data=df_results)
plt.title('Violin Plot da Acurácia dos Modelos')
plt.ylabel('Acurácia')
plt.show()

# Histograma (por modelo)
plt.figure(figsize=(10, 6))
for column in df_results.columns:
    sns.histplot(data=df_results[column], kde=True, label=column, bins=10)
plt.title('Histograma da Acurácia dos Modelos')
plt.xlabel('Acurácia')
plt.ylabel('Frequência')
plt.legend(title='Modelos')
plt.show()

# Swarm plot
plt.figure(figsize=(10, 6))
df_results_long = df_results.melt(var_name='Modelo', value_name='Acurácia')
sns.swarmplot(data=df_results_long, x='Modelo', y='Acurácia')
plt.title('Swarm Plot da Acurácia dos Modelos')
plt.ylabel('Acurácia')
plt.show()

"""Matriz de confusão para analisar os resultados do melhor método (pca)"""

from sklearn.metrics import confusion_matrix

# Treinar o modelo PCA com os dados de treino
lr.fit(x_train, y_train)

# Fazer previsões nos dados de teste
y_pred = lr.predict(x_test)

# Calcular a matriz de confusão
cm = confusion_matrix(y_test, y_pred)

# Plotar a matriz de confusão
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
            xticklabels=['Predicted Negative', 'Predicted Positive'],
            yticklabels=['Actual Negative', 'Actual Positive'])
plt.title('Confusion Matrix for PCA')
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.show()

"""4 pessoas não tinham e deu que tem"""