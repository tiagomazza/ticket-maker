import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Sistema de Tickets",
    page_icon="🎫",
    layout="wide"
)

st.title("🎫 Sistema de Tickets")
st.caption("Abertura, acompanhamento e análise de chamados.")

# Estado inicial
if "tickets" not in st.session_state:
    np.random.seed(42)
    descricoes = [
        "Erro ao acessar o sistema",
        "Falha na impressão",
        "Lentidão no computador",
        "Problema de login",
        "VPN não conecta",
        "Sistema travando ao abrir",
        "Erro no e-mail corporativo",
        "Banco de dados indisponível",
        "Permissão negada na pasta compartilhada",
        "Atualização causando incompatibilidade",
    ]

    dados = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1050, -1)],
        "Solicitante": np.random.choice(["Ana", "Bruno", "Carlos", "Diana", "Eduardo"], size=50),
        "Categoria": np.random.choice(["Hardware", "Software", "Rede", "Acesso"], size=50),
        "Descrição": np.random.choice(descricoes, size=50),
        "Status": np.random.choice(["Aberto", "Em andamento", "Fechado"], size=50),
        "Prioridade": np.random.choice(["Alta", "Média", "Baixa"], size=50),
        "Data Abertura": [
            datetime.date(2026, 1, 1) + datetime.timedelta(days=random.randint(0, 120))
            for _ in range(50)
        ],
    }
    st.session_state.tickets = pd.DataFrame(dados)

# Sidebar
with st.sidebar:
    st.header("Filtros")
    filtro_status = st.multiselect(
        "Status",
        ["Aberto", "Em andamento", "Fechado"],
        default=["Aberto", "Em andamento", "Fechado"]
    )
    filtro_prioridade = st.multiselect(
        "Prioridade",
        ["Alta", "Média", "Baixa"],
        default=["Alta", "Média", "Baixa"]
    )

# Formulário
st.subheader("Abrir novo ticket")

with st.form("form_ticket", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        solicitante = st.text_input("Solicitante")
        categoria = st.selectbox("Categoria", ["Hardware", "Software", "Rede", "Acesso"])
        prioridade = st.selectbox("Prioridade", ["Alta", "Média", "Baixa"])

    with col2:
        titulo = st.text_input("Título do problema")
        descricao = st.text_area("Descrição detalhada", height=120)

    enviar = st.form_submit_button("Criar ticket")

if enviar:
    if not solicitante or not titulo or not descricao:
        st.error("Preencha Solicitante, Título e Descrição.")
    else:
        ultimo_id = st.session_state.tickets["ID"].str.replace("TICKET-", "", regex=False).astype(int).max()
        novo_ticket = pd.DataFrame([{
            "ID": f"TICKET-{ultimo_id + 1}",
            "Solicitante": solicitante,
            "Categoria": categoria,
            "Descrição": f"{titulo} - {descricao}",
            "Status": "Aberto",
            "Prioridade": prioridade,
            "Data Abertura": datetime.date.today()
        }])

        st.session_state.tickets = pd.concat([novo_ticket, st.session_state.tickets], ignore_index=True)
        st.success("Ticket criado com sucesso.")
        st.dataframe(novo_ticket, use_container_width=True, hide_index=True)

# Filtros aplicados
df = st.session_state.tickets[
    st.session_state.tickets["Status"].isin(filtro_status)
    & st.session_state.tickets["Prioridade"].isin(filtro_prioridade)
].copy()

# Métricas
st.subheader("Indicadores")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total de tickets", len(df))
c2.metric("Abertos", int((df["Status"] == "Aberto").sum()))
c3.metric("Em andamento", int((df["Status"] == "Em andamento").sum()))
c4.metric("Fechados", int((df["Status"] == "Fechado").sum()))

# Tabela editável
st.subheader("Tickets")

df_editado = st.data_editor(
    df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            options=["Aberto", "Em andamento", "Fechado"],
            required=True,
        ),
        "Prioridade": st.column_config.SelectboxColumn(
            "Prioridade",
            options=["Alta", "Média", "Baixa"],
            required=True,
        ),
        "Data Abertura": st.column_config.DateColumn("Data Abertura", format="DD/MM/YYYY"),
    },
    disabled=["ID", "Data Abertura"],
)

# Atualiza estado principal
st.session_state.tickets.update(df_editado)

# Gráficos
st.subheader("Análise")

g1, g2 = st.columns(2)

with g1:
    st.markdown("#### Tickets por status")
    graf_status = (
        alt.Chart(df_editado)
        .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
        .encode(
            x=alt.X("Status:N", sort=["Aberto", "Em andamento", "Fechado"]),
            y="count():Q",
            color=alt.Color("Status:N", legend=None),
            tooltip=["Status:N", "count():Q"]
        )
        .properties(height=320)
    )
    st.altair_chart(graf_status, use_container_width=True)

with g2:
    st.markdown("#### Tickets por prioridade")
    graf_prioridade = (
        alt.Chart(df_editado)
        .mark_arc(innerRadius=70)
        .encode(
            theta="count():Q",
            color="Prioridade:N",
            tooltip=["Prioridade:N", "count():Q"]
        )
        .properties(height=320)
    )
    st.altair_chart(graf_prioridade, use_container_width=True)