import base64
from io import BytesIO
from pathlib import Path

import qrcode
import streamlit as st

st.set_page_config(page_title='Gerador de Ingresso', page_icon='🎟️', layout='wide')

st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"], [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
    font-family: 'Poppins', sans-serif;
}
</style>
""", unsafe_allow_html=True)

ASSETS = Path(__file__).parent / 'assets'
BANNER_PATH = ASSETS / 'capa_enf.png'
LOGO_PATH = ASSETS / 'logo_quinta.png'
MAPS_URL = 'https://www.google.com/maps/place/HI+Ovar+%E2%80%93+Pousada+de+Juventude/@40.8712312,-8.6477117,562m/data=!3m2!1e3!4b1!4m9!3m8!1s0xd2385e47117a33f:0x96aaa58f968b67fa!5m2!4m1!1i2!8m2!3d40.8712272!4d-8.6451368!16s%2Fg%2F11bwyy8q1x?entry=ttu&g_ep=EgoyMDI1MDkxNy4wIKXMDSoASAFQAw%3D%3D'


def img_to_base64(path: Path):
    if not path.exists():
        return None
    return base64.b64encode(path.read_bytes()).decode()


def qr_to_png_bytes(text: str) -> bytes:
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    return buffer.getvalue()


def qr_to_base64(text: str) -> str:
    return base64.b64encode(qr_to_png_bytes(text)).decode()


banner_b64 = img_to_base64(BANNER_PATH)
logo_b64 = img_to_base64(LOGO_PATH)

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
data_evento = st.sidebar.text_input('Data', value='04 de setembro de 2026 18:00')

qr_b64 = qr_to_base64(nome)

if banner_b64:
    hero_html = f"<div class='hero'><img src='data:image/png;base64,{banner_b64}' alt='Banner do evento'></div>"
else:
    hero_html = """
    <div class='hero fallback-hero'>
        <div>
            <div class='fallback-title'>II ENCONTRO NACIONAL</div>
            <div class='fallback-title'>DE FORROZEIROS</div>
        </div>
    </div>
    """

if logo_b64:
    logo_html = f"<img src='data:image/png;base64,{logo_b64}' alt='Logo Quinta'>"
else:
    logo_html = "<div class='mini-logo'>Logo</div>"

html = f"""
<link rel='preconnect' href='https://fonts.googleapis.com'>
<link rel='preconnect' href='https://fonts.gstatic.com' crossorigin>
<link href='https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap' rel='stylesheet'>

<style>
    * {{ box-sizing:border-box; }}
    a {{ color:#0d63c7; text-decoration:none; }}
    a:hover {{ text-decoration:underline; }}
    .page {{ background:#f3f3f3; padding:28px 0; display:flex; justify-content:center; }}
    .ticket {{ width:420px; background:#fff; box-shadow:0 10px 30px rgba(0,0,0,.08); font-family:'Poppins', sans-serif; color:#141414; overflow:hidden; }}
    .hero img {{ width:100%; display:block; height:auto; }}
    .fallback-hero {{ height:310px; background:linear-gradient(135deg,#ff00a8,#ff7a00,#ffe100); display:flex; align-items:center; justify-content:center; text-align:center; color:#fff; }}
    .fallback-title {{ font-size:28px; font-weight:800; line-height:1.05; text-shadow:0 2px 8px rgba(0,0,0,.25); }}
    .body {{ padding:14px 12px 24px; background:#fff; }}
    .card {{ position:relative; border:2px solid #e2e2e2; border-radius:12px; background:#fff; overflow:visible; }}
    .card:before, .card:after, .qr-card:before, .qr-card:after {{ content:''; position:absolute; width:38px; height:38px; background:#f3f3f3; border:2px solid #e2e2e2; border-radius:50%; }}
    .card:before {{ left:-22px; bottom:-22px; border-right:none; }}
    .card:after {{ right:-22px; bottom:-22px; border-left:none; }}
    .header-info {{ padding:24px 30px 12px; }}
    .subtitle {{ font-size:20px; font-weight:500; margin-bottom:12px; line-height:1.25; }}
    .date {{ font-size:18px; font-weight:700; margin-bottom:8px; }}
    .personal {{ font-size:13px; color:#6f6f6f; margin-bottom:10px; font-weight:500; }}
    .divider {{ border-top:2px dashed #d4d4d4; margin:0 24px; }}
    .qr-card {{ position:relative; border:2px solid #e2e2e2; border-top:none; border-radius:0 0 12px 12px; margin-top:-2px; padding:34px 24px 30px; text-align:center; background:#fff; }}
    .qr-card:before {{ left:-22px; top:-22px; border-right:none; }}
    .qr-card:after {{ right:-22px; top:-22px; border-left:none; }}
    .ticket-type {{ font-size:17px; font-weight:700; margin-bottom:26px; }}
    .qr-img {{ width:280px; height:280px; object-fit:contain; display:block; margin:0 auto 14px; image-rendering:pixelated; }}
    .name {{ font-size:18px; font-weight:700; margin-top:6px; word-break:break-word; }}
    .footer {{ text-align:center; padding:22px 24px 8px; }}
    .footer img {{ width:135px; margin:0 auto; display:block; max-height:69px; object-fit:contain; }}
    .mini-logo {{ font-size:24px; font-weight:800; color:#15152a; }}
    .love {{ margin-top:16px; font-size:16px; color:#15152a; font-weight:700; }}
</style>
<div class='page'>
  <div class='ticket'>
    {hero_html}
    <div class='body'>
      <div class='card'>
        <div class='header-info'>
          <div class='subtitle'>
            <a href='{MAPS_URL}' target='_blank' rel='noopener noreferrer'>Pousada da Juventude de Ovar</a>
          </div>
          <div class='date'>{data_evento}</div>
          <div class='personal'>Bilhete pessoal e intransferivel</div>
        </div>
      </div>
      <div class='divider'></div>
      <div class='qr-card'>
        <div class='ticket-type'>{tipo}</div>
        <img class='qr-img' src='data:image/png;base64,{qr_b64}' alt='QR Code do ingresso'>
        <div class='name'>{nome}</div>
      </div>
      <div class='footer'>
        {logo_html}
      </div>
    </div>
  </div>
</div>
"""

st.title('Gerador de Ingresso')
st.caption('Personalize o ingresso e baixe em HTML.')

col1, col2 = st.columns([1, 1.3], gap='large')
with col1:
    st.subheader('Dados atuais')
    st.write(f'**Nome:** {nome}')
    st.write(f'**Tipo:** {tipo}')
    st.markdown(f"**Local:** [Pousada da Juventude de Ovar]({MAPS_URL})")
    st.write(f'**Data:** {data_evento}')
    st.write('**Observação:** Bilhete individual, pessoal e intransferível')
    st.info('O QR code usa o próprio nome digitado. Se os arquivos assets/capa_enf.png ou assets/logo_quinta.png não existirem, o app usa um fallback visual.')

with col2:
    st.subheader('Pré-visualização')
    st.components.v1.html(html, height=930, scrolling=False)

st.download_button(
    'Baixar HTML do ingresso',
    data=html,
    file_name='Encontro_nacional_de_forrozeiros.html',
    mime='text/html'
)