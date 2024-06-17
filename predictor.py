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

# Criar DataFrame
df = pd.DataFrame(dados_jogos)

# Mapear os valores para números
mapeamento_resultado = {'vitoria': 1, 'empate': 0, 'derrota': -1}

df['resultado'] = df['resultado'].map(mapeamento_resultado)

soma = sum(df['resultado'])

media = soma/len(df['resultado'])

media = -0.7

if media == -1:
    print('O homem esta Enfurecido >_<')
elif media > -1 and media <= -0.7:
    print(r'O homem esta Irritado ಠ_ಠ')
elif media > -0.7 and media <= -0.4:
    print('O homem esta Frustrado -_-')
elif media > -0.4 and media <= -0.1:
    print('O homem esta Chateado :-(')
elif media > -0.1 and media < 0:
    print('O homem esta Desanimado T_T')
elif media == 0:
    print('O homem esta Neutro :-|')
elif media > 0 and media <= 0.3:
    print('O homem esta Contente :-)')
elif media > 0.3 and media <= 0.6:
    print('O homem esta Animado ^_^')
elif media > 0.6 and media < 1:
    print('O homem esta Eufórico \\(^o^)/')
elif midia == 1:
    print('O homem esta Radiante (*^▽^*)')

