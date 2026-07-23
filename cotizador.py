import streamlit as st
import os

# Configuración de página
st.set_page_config(page_title="Outland Logistics - Cotizador", page_icon="📦", layout="wide")

# Estilos CSS - Modo Oscuro Ejecutivo Outland Logistics
st.markdown("""
<style>
/* Fondo principal negro profundo */
.stApp {
    background-color: #121212 !important;
    color: #FFFFFF !important;
}

/* Sidebar en tono gris oscuro contrastante */
[data-testid="stSidebar"] {
    background-color: #1E1E1E !important;
}

/* Títulos y encabezados en blanco puro y tipografía limpia */
h1, h2, h3, h4, h5, h6, label, p, span {
    color: #FFFFFF !important;
    font-family: 'Segoe UI', Roboto, Helvetica, sans-serif !important;
}

/* Subtítulos de ayuda / capturas en gris claro */
.stCaption {
    color: #B0B0B0 !important;
}

/* Botón Principal en Naranja Oficial Outland */
.stButton>button {
    background-color: #F38218 !important;
    color: #FFFFFF !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    height: 3.2em !important;
    width: 100% !important;
    box-shadow: 0px 4px 10px rgba(243, 130, 24, 0.3);
}
.stButton>button:hover {
    background-color: #FF9429 !important;
    color: #FFFFFF !important;
    box-shadow: 0px 6px 15px rgba(243, 130, 24, 0.5);
}

/* Ajuste de cajas de texto e inputs para modo oscuro */
input {
    background-color: #2A2A2A !important;
    color: #FFFFFF !important;
    border-radius: 6px !important;
}

/* Tarjetas de Métricas / Resultados */
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    color: #F38218 !important;
    font-weight: bold !important;
}
[data-testid="stMetricLabel"] {
    color: #E0E0E0 !important;
}
</style>
""", unsafe_allow_html=True)

# Detección del logo oficial (Outland)
logo_file = None
for item in os.listdir("."):
    if item.lower().startswith("outland") and (item.lower().endswith(".png") or item.lower().endswith(".jpg") or item.lower().endswith(".jpeg")):
        logo_file = item
        break
if not logo_file:
    for item in os.listdir("."):
        if item.lower() == "outland":
            logo_file = item
            break

# Encabezado corporativo
col_logo, col_title = st.columns([1.5, 4])
with col_logo:
    if logo_file:
        st.image(logo_file, width=230)
    else:
        st.markdown("## 🌐 **OUTLAND**\n##### *LOGISTICS*")

with col_title:
    st.title("Cotizador de Cargas Aéreas y Marítimas (LCL)")
    st.caption("Herramienta Oficial de Cotización - Outland Logistics")

st.markdown("---")

# Menú lateral
st.sidebar.header("⚙️ Configuración del Envío")
tipo_transporte = st.sidebar.radio("Tipo de Transporte:", ["Marítimo LCL", "Aéreo"])
unidad_medida = st.sidebar.selectbox("Unidad de dimensión:", ["Milímetros (mm)", "Centímetros (cm)", "Metros (m)", "Pulgadas (in)"])
unidad_peso = st.sidebar.selectbox("Unidad de peso:", ["Kilogramos (kg)", "Libras (lb)"])

# Formulario de Carga
st.subheader("📏 Dimensiones y Peso de la Carga")
col1, col2, col3, col4 = st.columns(4)
with col1:
    largo = st.number_input("Largo", min_value=0.0, value=100.0 if "m" not in unidad_medida else 1.0, step=1.0)
with col2:
    ancho = st.number_input("Ancho", min_value=0.0, value=100.0 if "m" not in unidad_medida else 1.0, step=1.0)
with col3:
    alto = st.number_input("Alto", min_value=0.0, value=100.0 if "m" not in unidad_medida else 1.0, step=1.0)
with col4:
    bultos = st.number_input("Cantidad de bultos", min_value=1, value=1, step=1)

col5, col6 = st.columns(2)
with col5:
    peso_input = st.number_input(f"Peso Bruto Total ({unidad_peso.split()[-1]})", min_value=0.0, value=150.0 if "kg" in unidad_peso else 330.0, step=5.0)
with col6:
    if tipo_transporte == "Marítimo LCL":
        tarifa = st.number_input("Tarifa Flete (USD por m³ / W/M)", min_value=0.0, value=85.0, step=5.0)
    else:
        tarifa = st.number_input("Tarifa Flete (USD por kg cargable)", min_value=0.0, value=4.5, step=0.5)

# Cálculo al presionar el botón
if st.button("🧮 Calcular Cotización Outland"):
    # Conversión a metros
    if "Milímetros" in unidad_medida:
        l, a, h = largo / 1000.0, ancho / 1000.0, alto / 1000.0
    elif "Centímetros" in unidad_medida:
        l, a, h = largo / 100.0, ancho / 100.0, alto / 100.0
    elif "Metros" in unidad_medida:
        l, a, h = largo, ancho, alto
    else:  # Pulgadas
        l, a, h = largo * 0.0254, ancho * 0.0254, alto * 0.0254
    
    # Conversión a Kilogramos
    peso_bruto_kg = peso_input if "Kilogramos" in unidad_peso else peso_input * 0.453592
    
    m3_unitario = l * a * h
    m3_total = m3_unitario * bultos
    
    if tipo_transporte == "Marítimo LCL":
        peso_ton = peso_bruto_kg / 1000.0
        unidades_facturables = max(m3_total, peso_ton)
        costo_total = unidades_facturables * tarifa
        
        st.success("### 📊 Resumen de Cotización - Marítimo LCL")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Volumen Total", f"{m3_total:.3f} m³")
        m2.metric("Peso Bruto", f"{peso_bruto_kg:.1f} kg")
        m3.metric("Unidades W/M", f"{unidades_facturables:.3f}")
        m4.metric("💰 Costo Flete", f"${costo_total:,.2f} USD")
    else:
        peso_volumetrico_kg = m3_total * 166.667
        peso_tasable_kg = max(peso_bruto_kg, peso_volumetrico_kg)
        costo_total = peso_tasable_kg * tarifa
        
        st.success("### 📊 Resumen de Cotización - Carga Aérea")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Volumen Total", f"{m3_total:.3f} m³")
        m2.metric("Peso Volumétrico", f"{peso_volumetrico_kg:.2f} kg")
        m3.metric("Peso Cargable", f"{peso_tasable_kg:.2f} kg")
        m4.metric("💰 Costo Flete", f"${costo_total:,.2f} USD")