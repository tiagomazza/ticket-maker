import base64
from pathlib import Path

import qrcode
import streamlit as st

st.set_page_config(page_title='Ingresso EuroFollia', page_icon='🎟️', layout='wide')

ASSETS = Path(__file__).parent / 'assets'


def img_to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode()


def qr_to_base64(text: str) -> str:
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    from io import BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()


banner_b64 = img_to_base64(ASSETS / 'banner.jpg')
logo_b64 = img_to_base64(ASSETS / 'lebillet.png')

st.sidebar.title('Configuração do ingresso')
nome = st.sidebar.text_input('Nome no ingresso', value='NOME DO CLIENTE')
tipo = st.sidebar.selectbox(
    'Tipo de ingresso',
    [
        'Quaduplo sem casa de banho',
        'Duplo sem casa de banho',
        'Duplo com casa de banho',
        'Day use',
        'Festa unica',
    ],
)
data_evento = st.sidebar.text_input('Data e hora', value='04/Jul/2026 - 12:00h')
local_evento = st.sidebar.text_input('Local', value='Quinta Santo António')
cidade = st.sidebar.text_input('Cidade', value='Porto - POR')
evento = st.sidebar.text_input('Evento', value='EUROFOLLIA 2026 PORTO')

qr_b64 = qr_to_base64(nome)

html = f"""
<style>
    .page {{
        background:#f4f4f4;
        padding: 28px 0;
        display:flex;
        justify-content:center;
    }}
    .ticket {{
        width: 420px;
        background:white;
        border-radius: 0;
        overflow:hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        font-family: Arial, Helvetica, sans-serif;
        color:#141414;
    }}
    .hero img {{
        width:100%;
        display:block;
    }}
    .body {{
        padding: 14px 12px 24px;
        background:white;
    }}
    .card {{
        position:relative;
        border:2px solid #e2e2e2;
        border-radius: 12px;
        background:#fff;
        overflow:visible;
    }}
    .card:before, .card:after, .qr-card:before, .qr-card:after {{
        content:'';
        position:absolute;
        width:38px;
        height:38px;
        background:#f4f4f4;
        border:2px solid #e2e2e2;
        border-radius:50%;
    }}
    .card:before {{ left:-22px; bottom:-22px; border-right:none; }}
    .card:after {{ right:-22px; bottom:-22px; border-left:none; }}
    .header-info {{
        padding: 22px 30px 8px;
    }}
    .title {{
        font-size:18px;
        font-weight:800;
        text-align:center;
        letter-spacing:.3px;
        margin-bottom:18px;
    }}
    .subtitle {{
        font-size:21px;
        font-weight:400;
        margin-bottom:10px;
    }}
    .muted {{
        font-size:14px;
        color:#7f7f7f;
        margin-bottom:8px;
    }}
    .date {{
        font-size:18px;
        font-weight:800;
        margin-bottom:6px;
    }}
    .divider {{
        border-top:2px dashed #d4d4d4;
        margin: 0 24px;
    }}
    .qr-card {{
        position:relative;
        border:2px solid #e2e2e2;
        border-top:none;
        border-radius: 0 0 12px 12px;
        margin-top:-2px;
        padding: 34px 24px 30px;
        text-align:center;
        background:#fff;
    }}
    .qr-card:before {{ left:-22px; top:-22px; border-right:none; }}
    .qr-card:after {{ right:-22px; top:-22px; border-left:none; }}
    .ticket-type {{
        font-size:17px;
        font-weight:800;
        margin-bottom:26px;
    }}
    .qr-img {{
        width: 280px;
        height: 280px;
        object-fit: contain;
        display:block;
        margin: 0 auto 14px;
        image-rendering: pixelated;
    }}
    .name {{
        font-size:18px;
        font-weight:800;
        margin-top:6px;
        word-break:break-word;
    }}
    .footer {{
        text-align:center;
        padding: 22px 0 8px;
    }}
    .footer img {{
        width:74px;
        margin:0 auto;
        display:block;
    }}
    .hint {{
        font-size:12px;
        color:#6e6e6e;
        text-align:center;
        margin-top:14px;
    }}
</style>
<div class='page'>
    <div class='ticket'>
        <div class='hero'><img src='data:image/jpeg;base64,{banner_b64}' alt='Banner do evento'></div>
        <div class='body'>
            <div class='card'>
                <div class='header-info'>
                    <div class='title'>{evento}</div>
                    <div class='subtitle'>{local_evento}</div>
                    <div class='muted'>{cidade}</div>
                    <div class='date'>{data_evento}</div>
                </div>
            </div>
            <div class='divider'></div>
            <div class='qr-card'>
                <div class='ticket-type'>{tipo}</div>
                <img class='qr-img' src='data:image/png;base64,{qr_b64}' alt='QR Code do ingresso'>
                <div class='name'>{nome}</div>
            </div>
            <div class='footer'>
                <img src='data:image/png;base64,{logo_b64}' alt='LeBillet'>
            </div>
        </div>
    </div>
</div>
"""

st.title('Gerador de Ingresso EuroFollia')
st.caption('Preencha os dados na barra lateral para personalizar o ingresso.')

col1, col2 = st.columns([1.05, 1.25], gap='large')

with col1:
    st.subheader('Dados atuais')
    st.write(f'**Nome:** {nome}')
    st.write(f'**Tipo:** {tipo}')
    st.write(f'**Evento:** {evento}')
    st.write(f'**Local:** {local_evento}')
    st.write(f'**Cidade:** {cidade}')
    st.write(f'**Data:** {data_evento}')
    st.info('O QR code é gerado com o próprio nome informado no campo "Nome no ingresso".')

with col2:
    st.subheader('Pré-visualização')
    st.components.v1.html(html, height=930, scrolling=False)

st.download_button(
    'Baixar HTML do ingresso',
    data=html,
    file_name='ingresso_eurofollia.html',
    mime='text/html'
)