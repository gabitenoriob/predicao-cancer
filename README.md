# Predição de Câncer com Machine Learning

Este projeto utiliza algoritmos de aprendizado de máquina para analisar dados de expressão genética e prever a presença de câncer. São explorados diferentes modelos de classificação, incluindo Regressão Logística e KNN, além de técnicas de seleção de atributos e redução de dimensionalidade.

## **Estrutura do Projeto**

O projeto está dividido nas seguintes etapas:

### **1. Bibliotecas Necessárias**
- Importação de bibliotecas essenciais como `pandas`, `numpy`, `seaborn`, `matplotlib`, e pacotes do `sklearn`.

### **2. Leitura dos Dados**
- O dataset é carregado a partir de um arquivo CSV chamado `brca_mirnaseq.csv`.
- As colunas e dimensões do dataset são analisadas.

### **3. Análise Exploratória**
- Visualização das classes com gráficos de barras (`countplot`).
- Cálculo da proporção de classes (`TP` e `NT`).
- Estatísticas descritivas básicas.

### **4. Preparação dos Dados**
- Divisão dos dados em variáveis independentes (`X`) e dependentes (`y`).
- Separação em conjuntos de treino e teste com proporção de 70% para treino e 30% para teste, utilizando a técnica de `stratify` para manter a proporção das classes.

### **5. Modelagem**
- **Regressão Logística:** Avaliada usando validação cruzada com 10 folds.
- **KNN (K-Nearest Neighbors):** Configurado com diferentes métricas de distância:
  - Distância Euclidiana.
  - Distância Manhattan.
- **Regressão Logística Regularizada:**
  - Penalidade L1 (sparse).
  - Penalidade L2 (reduz overfitting).
- **PCA (Análise de Componentes Principais):** Utilizado para redução de dimensionalidade.

### **6. Avaliação Experimental**
- Comparação entre os modelos com métricas de acurácia balanceada (média e desvio padrão).
- Visualizações incluem:
  - **Boxplots:** Distribuição de acurácia por modelo.
  - **Violin plots:** Densidade da acurácia por modelo.
  - **Histograma:** Frequência da acurácia por modelo.
  - **Swarm plots:** Distribuição pontual da acurácia.

### **7. Matriz de Confusão**
- O melhor modelo (PCA com Regressão Logística) é avaliado em um conjunto de teste.
- A matriz de confusão é gerada para analisar a performance em termos de Falsos Positivos, Falsos Negativos, Verdadeiros Positivos e Verdadeiros Negativos.

## **Dependências**
- Python 3.11+
- Pacotes:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `scikit-learn`

### **Instalação**
Para instalar as dependências, execute o seguinte comando:

```bash
pip install -r requirements.txt
´´´

### **Como Executar**

Certifique-se de que o arquivo brca_mirnaseq.csv está na mesma pasta do script ou notebook.
Execute o predicao_cancer.py em um ambiente python.

Arquivos
predicao_cancer.py: Código principal para análise e modelagem.
brca_mirnaseq.csv: Dataset utilizado para treinar e avaliar os modelos.

Resultados
Os modelos de aprendizado de máquina apresentam diferentes níveis de desempenho. O uso de PCA combinado com Regressão Logística mostrou ser a abordagem mais eficaz, alcançando uma acurácia média superior às demais abordagens, conforme os experimentos realizados.
