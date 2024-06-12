#!/usr/bin/env python3

import requests
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Função para obter resultados do Palmeiras usando a API do Football Data
def obter_resultados_palmeiras(api_key, team_id, season):
    url = f"https://api.football-data.org/v4/teams/{team_id}/matches?season={season}"
    headers = {
        'X-Auth-Token': api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Erro ao acessar a API: {response.status_code}")

# Função para processar os resultados e extrair os dados relevantes
def processar_resultados(resultados, team_id):
    dados = []
    for jogo in resultados['matches']:
        print(jogo)
        if jogo['status'] == 'FINISHED':
            if jogo['score']['winner'] == 'HOME_TEAM' and jogo['homeTeam']['id'] == team_id:
                resultado = 'vitoria'
            elif jogo['score']['winner'] == 'AWAY_TEAM' and jogo['awayTeam']['id'] == team_id:
                resultado = 'vitoria'
            elif jogo['score']['winner'] == 'DRAW' and jogo['homeTeam']['id'] == team_id:
                resultado = 'empate'
            elif jogo['score']['winner'] == 'DRAW' and jogo['awayTeam']['id'] == team_id:
                resultado = 'empate'
            elif jogo['awayTeam']['id'] == team_id or jogo['homeTeam']['id'] == team_id:
                resultado = 'derrota'
            
            humor = 'feliz' if resultado == 'vitoria' else 'neutro' if resultado == 'empate' else 'irritado'
            
            dados.append({'resultado': resultado, 'humor': humor})
    
    return dados

# Substitua pelos valores reais
api_key = '4fa1d5cd6b754599b234c3fc684eca44'
team_id = 1769  # ID do Palmeiras na API Football Data
season = 2024  # Temporada atual

resultados = obter_resultados_palmeiras(api_key, team_id, season)
# print(resultados)

# Processar os resultados do Palmeiras
dados_jogos = processar_resultados(resultados, team_id)
print(dados_jogos)

# Criar DataFrame
df = pd.DataFrame(dados_jogos)

# Mapear os valores para números
mapeamento_resultado = {'vitoria': 1, 'empate': 0, 'derrota': -1}
mapeamento_humor = {'feliz': 1, 'neutro': 0, 'irritado': -1}

df['resultado'] = df['resultado'].map(mapeamento_resultado)
df['humor'] = df['humor'].map(mapeamento_humor)

# Separar os dados em características (X) e alvo (y)
X = df[['resultado']]
y = df['humor']

# Dividir os dados em conjunto de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar um modelo de Random Forest
modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)

# Avaliar a precisão do modelo
y_pred = modelo.predict(X_test)
# print(f"Acurácia do modelo: {accuracy_score(y_test, y_pred)}")

# Função para prever o humor com base em um novo resultado
def prever_humor(resultado):
    # Mapear o resultado para o valor numérico correspondente
    resultado_mapeado = mapeamento_resultado[resultado]
    # Criar um DataFrame com o mesmo formato dos dados de treinamento
    entrada = pd.DataFrame([[resultado_mapeado]], columns=['resultado'])
    # Fazer a previsão
    humor_previsto = modelo.predict(entrada)
    # Mapear de volta para o valor de humor correspondente
    mapeamento_humor_inverso = {1: 'feliz', 0: 'neutro', -1: 'irritado'}
    return mapeamento_humor_inverso[humor_previsto[0]]

# Fazer uma previsão de acordo com o ultimo jogo
print(f"Humor previsto: {prever_humor(dados_jogos[-1]['resultado'])}")
