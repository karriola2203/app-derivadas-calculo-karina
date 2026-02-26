import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Cátedra Arriola: Cálculo de Derivadas", layout="wide")

# Estilo para mejorar la apariencia del editor
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        font-size: 24px;
        color: #1E3A8A;
        font-family: 'Consolas', monospace;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ Tutor de Derivación Detallada")
st.subheader("Facultad de Arquitectura | Profe Karina Arriola")

# --- SECCIÓN DEL EDITOR (ENTRADA) ---
st.write("### ✍️ Editor de Funciones")
u_input = st.text_input("Digita la función que deseas derivar:", "x**2 * sin(x)")

# Limpieza y preparación de la variable x
x = sp.symbols('x')

try:
    # Procesar la entrada del estudiante
    expr_clean = u_input.replace("^", "**")
    h = sp.sympify(expr_clean)
    
    # --- VISTA PREVIA (Para que el estudiante verifique lo que escribió) ---
    st.info("#### 👁️ Vista Previa de tu función:")
    st.latex(f"f(x) = {sp.latex(h)}")
    
    st.markdown("---")
    st.write("### 🔍 Desglose del Procedimiento Paso a Paso")

    # --- LÓGICA DE DERIVACIÓN (Basada en tu código original) ---
    
    # 1. CASO PRODUCTO
    if h.is_Mul and any(arg.has(x) for arg in h.args):
        args = [arg for arg in h.args if arg.has(x)]
        if len(args) > 1:
            f = args[0]
            g = sp.Mul(*args[1:])
            df = sp.diff(f, x)
            dg = sp.diff(g, x)
            
            st.info("**Regla Aplicada:** Regla del Producto")
            st.latex(r"[f(x) \cdot g(x)]' = f'(x)g(x) + f(x)g'(x)")
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Componentes Identificados:**")
                st.latex(f"f(x) = {sp.latex(f)}")
                st.latex(f"g(x) = {sp.latex(g)}")
            with col2:
                st.write("**Derivadas Individuales:**")
                st.latex(f"f'(x) = {sp.latex(df)}")
                st.latex(f"g'(x) = {sp.latex(dg)}")
            
            st.write("**Ensamblaje del resultado:**")
            st.latex(f"h'(x) = ({sp.latex(df)}) \cdot ({sp.latex(g)}) + ({sp.latex(f)}) \cdot ({sp.latex(dg)})")

    # 2. CASO COCIENTE
    elif h.is_Pow and h.exp.is_negative or sp.fraction(h)[1] != 1:
        num, den = sp.fraction(h)
        f, g = num, den
        df, dg = sp.diff(f, x), sp.diff(g, x)

        st.info("**Regla Aplicada:** Regla del Cociente")
        st.latex(r"\left[\frac{f(x)}{g(x)}\right]' = \frac{f'(x)g(x) - f(x)g'(x)}{[g(x)]^2}")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Componentes Identificados:**")
            st.latex(f"f(x) = {sp.latex(f)}")
            st.latex(f"g(x) = {sp.latex(g)}")
        with col2:
            st.write("**Derivadas Individuales:**")
            st.latex(f"f'(x) = {sp.latex(df)}")
            st.latex(f"g'(x) = {sp.latex(dg)}")

        st.write("**Ensamblaje del resultado:**")
        st.latex(f"h'(x) = \\frac{({sp.latex(df)})({sp.latex(g)}) - ({sp.latex(f)})({sp.latex(dg)})}{({sp.latex(g)})^2}")

    # 3. CASO FUNCIONES TRIGONOMÉTRICAS O EXPONENCIALES
    elif any(func in str(h) for func in ["sin", "cos", "exp", "log", "tan"]):
        # Obtener la función principal y su argumento
        main_func = h.func
        g = h.args[0]
        dg = sp.diff(g, x)
        
        if "exp" in str(h):
            st.info("**Regla Aplicada:** Exponencial")
            st.latex(r"[e^{g(x)}]' = e^{g(x)} \cdot g'(x)")
        elif "sin" in str(h):
            st.info("**Regla Aplicada:** Seno")
            st.latex(r"[\sin(g(x))]' = \cos(g(x)) \cdot g'(x)")
        elif "cos" in str(h):
            st.info("**Regla Aplicada:** Coseno")
            st.latex(r"[\cos(g(x))]' = -\sin(g(x)) \cdot g'(x)")
        
        st.write("**Identificación del Argumento Interno:**")
        st.latex(f"g(x) = {sp.latex(g)} \implies g'(x) = {sp.latex(dg)}")
        
        st.write("**Aplicando la Regla de la Cadena:**")
        st.latex(f"h'(x) = {sp.latex(sp.diff(h, x))}")

    # 4. REGLA POTENCIA / SUMA
    else:
        st.info("**Regla Aplicada:** Regla de la Potencia / Suma")
        st.write("Se deriva cada término de forma independiente:")
        st.latex(f"h'(x) = {sp.latex(sp.diff(h, x))}")

    # --- RESULTADO FINAL SIMPLIFICADO ---
    st.success("### ✅ Resultado Final Simplificado")
    st.latex(f"h'(x) = {sp.latex(sp.simplify(sp.diff(h, x)))}")

except Exception as e:
    st.error("⚠️ Error de sintaxis. Asegúrate de usar '*' para multiplicar (ej. 3*x) y '**' para potencias (ej. x**2).")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📖 Guía Rápida del Editor")
    st.write("Usa los siguientes comandos:")
    st.code("Producto: x**2 * sin(x)")
    st.code("División: (x+1) / (x-1)")
    st.code("Potencia: x**3")
    st.code("Trigonométricas: sin(x), cos(x), tan(x)")
    st.markdown("---")
    st.write("*Tutor desarrollado para la Facultad de Arquitectura.*")
