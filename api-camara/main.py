from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

import requests
import pandas as pd
from pathlib import Path
from tqdm import tqdm
import glob

import io
import matplotlib.pyplot as plt

app = FastAPI()

# Permitir CORS de qualquer origem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs da API oficial
URL = "https://dadosabertos.camara.leg.br/api/v2/deputados?nome=&ordem=ASC&ordenarPor=nome"
URL_ID = "https://dadosabertos.camara.leg.br/api/v2/deputados"

# =========================
#  CARREGAMENTO DOS CSVs
# =========================

# Caminho para os CSVs
arquivos = sorted(glob.glob("dados/Ano-*.csv"))

# Colunas que realmente interessam
colunas_interessantes = [
    "txNomeParlamentar",
    "ideCadastro",
    "sgUF",
    "sgPartido",
    "txtDescricao",
    "txtFornecedor",
    "vlrLiquido",
    "numAno",
    "numMes",
]

dfs = []

print(f"\n🧾 Encontrados {len(arquivos)} arquivos CSV para processar.\n")

for arquivo in tqdm(arquivos, desc="📊 Lendo arquivos", ncols=100):
    try:
        # Lê todo o CSV
        df = pd.read_csv(arquivo, sep=";", encoding="utf-8", low_memory=False)

        # Limpa espaços e aspas do header
        df.columns = [c.strip().replace('"', '') for c in df.columns]

        # Filtra apenas as colunas que interessam e que existem no CSV
        cols_existentes = [c for c in colunas_interessantes if c in df.columns]
        df = df[cols_existentes]

        dfs.append(df)
    except Exception as e:
        print(f"⚠️ Erro ao ler {arquivo}: {e}")

# Concatena todos os dataframes
dados = pd.concat(dfs, ignore_index=True)

# Limpeza
dados["txNomeParlamentar"] = dados["txNomeParlamentar"].str.title().str.strip()
dados["vlrLiquido"] = pd.to_numeric(dados["vlrLiquido"], errors="coerce").fillna(0)

print(f"\n✅ Total de registros combinados: {len(dados):,}")
print(f"👥 Deputados únicos: {dados['txNomeParlamentar'].nunique():,}")

# =========================
#  ROTAS DA API
# =========================

@app.get("/python/api-camara/deputados")
def get_deputados():
    response = requests.get(URL)
    response.raise_for_status()
    return response.json()

@app.get("/python/api-camara/deputado/{id}")
def get_deputado(id: int):
    response = requests.get(f"{URL_ID}/{id}")
    
    if response.status_code == 404:
        raise HTTPException(status_code=404, detail="Deputado não encontrado")
    
    response.raise_for_status()
    return response.json()

# Rota que usa os dados CSV carregados
@app.get("/python/api-camara/grafico/{ideCadastro}")
def grafico_gastos(ideCadastro: int):
    # Filtrar os dados do deputado
    filtro = dados[dados["ideCadastro"] == ideCadastro]

    if filtro.empty:
        raise HTTPException(status_code=404, detail="Nenhum gasto encontrado para este deputado")

    # Agrupar por ano e mês
    filtro["ano_mes"] = filtro["numAno"].astype(str) + "-" + filtro["numMes"].astype(str).str.zfill(2)
    gastos = (
        filtro.groupby("ano_mes")["vlrLiquido"]
        .sum()
        .reset_index()
        .sort_values("ano_mes")
    )

    # Criar o gráfico de linha
    plt.figure(figsize=(10, 5))
    plt.plot(gastos["ano_mes"], gastos["vlrLiquido"], marker="o", linewidth=2, color="steelblue")

    # Ajustar layout do eixo X para não sobrecarregar
    plt.xticks(gastos["ano_mes"][::max(len(gastos)//10, 1)], rotation=45, ha="right")

    plt.xlabel("Ano-Mês")
    plt.ylabel("Valor (R$)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    # Converter o gráfico em PNG
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

@app.get("/python/api-camara/gastos_mensais/{ideCadastro}")
def gastos_mensais(ideCadastro: int):
    # Filtra os registros do deputado
    filtro = dados[dados["ideCadastro"] == ideCadastro]

    if filtro.empty:
        raise HTTPException(status_code=404, detail="Nenhum gasto encontrado para este deputado")

    # Agrupa por ano e mês e soma os valores
    filtro["ano_mes"] = filtro["numAno"].astype(str) + "-" + filtro["numMes"].astype(str).str.zfill(2)
    gastos = (
        filtro.groupby("ano_mes")["vlrLiquido"]
        .sum()
        .reset_index()
        .sort_values("ano_mes")
    )

    # Converte para JSON amigável
    resultado = [
        {"ano_mes": row["ano_mes"], "gasto_total": float(row["vlrLiquido"])}
        for _, row in gastos.iterrows()
    ]

    return {"ideCadastro": ideCadastro, "total_meses": len(resultado), "gastos": resultado}

@app.get("/python/api-camara/gastos/{ideCadastro}/{ano}/{mes}")
def gastos_por_mes(ideCadastro: int, ano: int, mes: int):
    # Filtra pelo deputado, ano e mês
    filtro = dados[
        (dados["ideCadastro"] == ideCadastro)
        & (dados["numAno"] == ano)
        & (dados["numMes"] == mes)
    ]

    if filtro.empty:
        raise HTTPException(status_code=404, detail="Nenhum gasto encontrado para este período")

    # Agrupa por descrição da despesa e soma os valores
    resumo = (
        filtro.groupby("txtDescricao")["vlrLiquido"]
        .sum()
        .reset_index()
        .sort_values("vlrLiquido", ascending=False)
    )

    # Converte para JSON legível
    resultado = [
        {
            "descricao": row["txtDescricao"],
            "valor_total": float(row["vlrLiquido"])
        }
        for _, row in resumo.iterrows()
    ]

    # Retorna também o total geral do mês
    total_mes = float(resumo["vlrLiquido"].sum()) if not resumo.empty else 0

    return {
        "ideCadastro": ideCadastro,
        "ano": ano,
        "mes": mes,
        "total_mes": total_mes,
        "gastos_detalhados": resultado
    }
