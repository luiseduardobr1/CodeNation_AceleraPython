import pandas as pd
from datetime import datetime

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]


# Calcular valores variáveis por minuto
def checar_taxa_horaria(minutos):
    if 360 <= minutos <= 1320:
        return(0.09*1)
    else:
        return(0)


def classify_by_phone_number(records):

    # Criando dataframe
    df = pd.DataFrame(records)

    # Calculando o tempo de ligação em minutos
    df['tempo de ligacao'] = (df['end'] - df['start'])/60
    df['tempo de ligacao'] = df['tempo de ligacao'].astype(int)

    # Convertendo o timestamp da data inicial e final para datetime
    df['data_inicial'] = pd.to_datetime(df['start'].astype(int), unit='s')
    df['data_final'] = pd.to_datetime(df['end'].astype(int), unit='s')

    # O gabarito está no horário local, logo, converte-se UTC -> LOCAL
    df['data_inicial'] = df['data_inicial'].dt.tz_localize('UTC').dt.tz_convert('America/Fortaleza')
    df['data_final'] = df['data_final'].dt.tz_localize('UTC').dt.tz_convert('America/Fortaleza')

    # Convertendo a data inicial para minutos
    df['data_inicial_minutos'] = df.data_inicial.dt.hour*60
    + df.data_inicial.dt.minute
    + df.data_inicial.dt.second/60
    df['data_inicial_minutos'] = df['data_inicial_minutos'].astype(int)

    # Calculando a taxa por minuto de cada ligação
    for linha in range(len(df)):
        multipla_taxa_horaria = 0
        minuto_inicial = df.iloc[linha, 7]
        tempo_ligacao = df.iloc[linha, 4]
        pagamento_minuto = 0

        # Valor variável de cada ligação
        while tempo_ligacao > 0:
            minuto_inicial = minuto_inicial + 1
            pagamento_minuto += checar_taxa_horaria(minuto_inicial)
            if (pagamento_minuto != 0) and (checar_taxa_horaria(minuto_inicial) == 0):

                # Se '1' indica que há duas faixas de preço
                multipla_taxa_horaria = 1

            tempo_ligacao = tempo_ligacao - 1

        # Valor total de cada ligação
        df.loc[linha, 'total'] = pagamento_minuto + 0.36*(multipla_taxa_horaria + 1)

    # Agrupando a tabela por 'source' e colocando em ordem decrescente do 'Total'
    tabela_agrupada = df.groupby("source")["total"].sum()
    convertido = tabela_agrupada.sort_values(ascending=False).round(2).reset_index()

    # Convertendo para dicionário
    return(convertido.to_dict(orient='records'))


# Resultado final
classify_by_phone_number(records)
