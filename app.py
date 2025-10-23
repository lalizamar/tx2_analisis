# -*- coding: utf-8 -*-
# NLP • TextBlob + googletrans — Arcoíris de Emociones 🌈
# Requisitos: streamlit, textblob, googletrans==4.0.0-rc1 (o la que uses)

import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# ─────────────────────────────────────────────────────────
# Config general
st.set_page_config(page_title="🌈 EmotiText — Arcoíris de Sentimientos", page_icon="🌈", layout="centered")
translator = Translator()

# ─────────────────────────────────────────────────────────
# Temas arcoíris (selector)
PALETTES = {
    "Arcoíris Sueño 🌈": {
        "bg": "linear-gradient(180deg, #fff7fb 0%, #fffbe6 30%, #e9fff8 60%, #f0e9ff 100%)",
        "card": "rgba(255,255,255,0.92)",
        "accent": "#ff7ac8",
        "accent2": "#a78bfa",
        "text": "#111",
        "chip": "#ffe6f4",
    },
    "Dulce Lavanda 💜": {
        "bg": "linear-gradient(180deg, #fefcff 0%, #efe9ff 100%)",
        "card": "rgba(255,255,255,0.92)",
        "accent": "#8a6bff",
        "accent2": "#d8ceff",
        "text": "#111",
        "chip": "#efe6ff",
    },
    "Menta Peach 🍑": {
        "bg": "linear-gradient(180deg, #f7fff9 0%, #ffeede 100%)",
        "card": "rgba(255,255,255,0.92)",
        "accent": "#2fbf71",
        "accent2": "#b8f2cf",
        "text": "#111",
        "chip": "#e9fff0",
    },
}

with st.sidebar:
    st.markdown("## 🎨 Tema")
    theme = st.selectbox("Elige tu paleta", list(PALETTES.keys()), index=0)
    P = PALETTES[theme]

# ─────────────────────────────────────────────────────────
# CSS cute + arcoíris
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
  background: {P['bg']} !important;
}}
[data-testid="stSidebarContent"] {{
  background: {P['card']}; border: 2px solid {P['accent2']};
  border-radius: 16px; padding: .8rem;
}}
h1,h2,h3,label,p,span,div {{ color:{P['text']} !important; }}
.card {{
  background:{P['card']}; border:2px solid {P['accent2']}; border-radius:22px;
  padding:1rem 1.1rem; box-shadow:0 12px 30px rgba(0,0,0,.06); backdrop-filter: blur(6px);
}}
.chip {{
  display:inline-flex; align-items:center; gap:.4rem; padding:.35rem .7rem; border-radius:999px;
  background:{P['chip']}; border:1.5px solid {P['accent2']}; color:{P['text']}; font-weight:700; font-size:.8rem;
  margin-right:.25rem;
}}
div.stButton>button {{
  background:{P['accent']}; color:#fff; border:none; border-radius:16px; padding:.6rem 1rem; font-weight:800;
  box-shadow:0 8px 16px rgba(0,0,0,.08); transition:transform .06s ease, filter .2s ease;
}}
div.stButton>button:hover {{ transform: translateY(-1px); filter: brightness(1.06); }}
.stTextArea textarea, .stTextInput input, .stSelectbox [data-baseweb="select"]>div {{
  border-radius:14px !important; border:2px solid {P['accent2']} !important;
}}
.gauge {{
  width:100%; height:14px; border-radius:999px; background:#eee; overflow:hidden; border:2px solid {P['accent2']};
}}
.bar {{
  height:100%; transition:width .4s ease;
  background: linear-gradient(90deg,#ff6b6b,#ffd166,#6ee7b7,#60a5fa,#a78bfa);
}}
.banner {{
  display:flex; gap:12px; align-items:center;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# Encabezado creativo
st.markdown(f"""
<div class="card banner">
  <div style="font-size:34px">🌈</div>
  <div>
    <h1 style="margin:0">EmotiText — Arcoíris de Sentimientos</h1>
    <div class="chip">💬 Análisis</div>
    <div class="chip">😊/😔 Emociones</div>
    <div class="chip">🧭 Polaridad</div>
    <div class="chip">🌫️ Subjetividad</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.write("Escribe una frase y te diré **qué emoción domina**, con colores y consejitos acordes. "
         "Analizamos con **TextBlob** (en inglés), así que traducimos de forma automática si escribes en español.")

# Sidebar con explicación (del profe, remaquetado)
with st.sidebar:
    st.markdown("## 📘 Polaridad y Subjetividad")
    st.write(
        "**Polaridad:** de -1 (muy negativo) a 1 (muy positivo), 0 = neutral.\n\n"
        "**Subjetividad:** de 0 (objetivo) a 1 (muy subjetivo)."
    )

# ─────────────────────────────────────────────────────────
# Funciones utilitarias
def analyze_text(text, src_lang="auto"):
    """
    Traduce a inglés si hace falta, analiza con TextBlob y devuelve:
    polarity, subjectivity, lang_detected, text_en, text_out
    """
    if not text.strip():
        return None

    # Detecta idioma y traduce a EN para TextBlob
    try:
        det = translator.detect(text) if src_lang == "auto" else None
        source = det.lang if det else src_lang
        if source != "en":
            trans = translator.translate(text, src=source, dest="en")
            text_en = trans.text
        else:
            text_en = text
    except Exception:
        # Si falla la traducción, intenta directo
        source = "auto"
        text_en = text

    blob = TextBlob(text_en)
    pol = round(blob.sentiment.polarity, 3)
    subj = round(blob.sentiment.subjectivity, 3)
    return {"polarity": pol, "subjectivity": subj, "lang": source, "text_en": text_en}

def emotion_from_polarity(p):
    # Map simple a emoción + color + emoji
    if p >= 0.6:   return "Felicidad intensa", "😍", "#6ee7b7"
    if p >= 0.25:  return "Felicidad / Calma", "😊", "#a7f3d0"
    if p > -0.25:  return "Neutral / Equilibrio", "😐", "#fef08a"
    if p > -0.6:   return "Tristeza / Enfado leve", "😕", "#fbcfe8"
    return "Rabia / Tristeza profunda", "😭", "#fecaca"

def advice_for_emotion(name):
    tips = {
        "Felicidad intensa": "¡Sigue así! Comparte esa buena vibra con alguien más hoy ✨.",
        "Felicidad / Calma": "Se siente bien. Quizá una mini meta o gratitud de 1 minuto 💖.",
        "Neutral / Equilibrio": "¿Qué le falta a tu día para subir +1? Un té, una canción, un paseo ☕🎶.",
        "Tristeza / Enfado leve": "Respira 4-4-4, escribe 3 cosas que te apoyan ahora mismo 💌.",
        "Rabia / Tristeza profunda": "Haz una pausa amable contigo. Busca apoyo o descansa un poco 🫶.",
    }
    return tips.get(name, "")

# ─────────────────────────────────────────────────────────
# Sección 1: Analizar Polaridad y Subjetividad (como el profe)
with st.expander("🔎 Analizar Polaridad y Subjetividad en un texto", expanded=True):
    text1 = st.text_area("Escribe tu frase aquí:", placeholder="Hoy me siento…")
    if text1:
        res = analyze_text(text1, src_lang="auto")
        if res:
            pol, subj = res["polarity"], res["subjectivity"]
            emo, emo_ico, emo_color = emotion_from_polarity(pol)

            # Indicadores
            st.write(f"**Polaridad:** {pol}  |  **Subjetividad:** {subj}")
            st.markdown('<div class="gauge"><div class="bar" style="width:{:.0f}%;"></div></div>'.format((pol+1)*50), unsafe_allow_html=True)
            st.write(f"**Emoción dominante:** {emo_ico} {emo}")

            # Consejo reactivo
            st.markdown(f"<div class='card' style='border-left:10px solid {emo_color}'><b>Consejo:</b> {advice_for_emotion(emo)}</div>", unsafe_allow_html=True)

            # Pequeña celebración/efecto
            if pol >= 0.6:
                st.balloons()
            elif pol <= -0.6:
                st.snow()

# ─────────────────────────────────────────────────────────
# Sección 2: Corrección en inglés (como el profe)
with st.expander("✍️ Corrección en inglés"):
    text2 = st.text_area("Escribe en inglés para corregir:", key="correct_en", placeholder="I has a dreem to be better…")
    if text2:
        blob2 = TextBlob(text2)
        st.write("**Corrección sugerida:**")
        st.write(blob2.correct())

# ─────────────────────────────────────────────────────────
# Bonus: pequeño traductor emoción ➜ inglés para probar TextBlob rápido
with st.expander("🌍 Mini-traductor (ES ➜ EN) para experimentar"):
    txt = st.text_input("Frase en español:", placeholder="Me siento increíblemente feliz hoy, gracias.")
    if txt:
        try:
            tt = translator.translate(txt, src="es", dest="en").text
            st.write("**Inglés:** ", tt)
        except Exception:
            st.warning("No se pudo traducir ahora mismo.")
