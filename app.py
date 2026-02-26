import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Tutor de Cálculo: Cátedra Arriola", layout="wide")

st.title("🏛️ Tutor de Derivación Detallada")
st.subheader("Facultad de Arquitectura | Profe Karina Arriola")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📖 Guía de Escritura")
    st.markdown("""
    * **Multiplicación:** `5*x`
    * **Potencia:** `x^2`
    * **División:** `(x+1)/x`
    * **Ejemplo:** `x^2 * sin(3*x) - cos(2*x) / x`
    """)

# --- BLOQUE 1: ENTRADA ---
u_input = st.text_input("Ingresa la función a derivar:", value="x^2 * sin(3*x) - 5*x")

x = sp.symbols('x')

try:
    input_proc = u_input.replace("^", "**").replace("e**", "exp")
    h = sp.sympify(input_proc)
    
    st.info("#### 👁️ Vista Previa:")
    st.latex(f"f(x) = {sp.latex(h)}")
    st.markdown("---")

    # --- PASO 1: IDENTIFICAR TÉRMINOS ---
    # Sympy separa automáticamente por sumas/restas
    terminos = sp.Add.make_args(h)
    num_terminos = len(terminos)
    
    st.write(f"### 🔍 Paso 1: Análisis de estructura")
    st.write(f"La función tiene **{num_terminos} término(s)**. Aplicamos la regla de la suma/resta:")
    
    # Mostrar la separación visual
    st.latex(f"\\frac{{d}}{{dx}}[f(x)] = " + " ".join([f"{'+' if i>0 and t.as_coeff_Mul()[0]>0 else ''} \\frac{{d}}{{dx}}({sp.latex(t)})" for i, t in enumerate(terminos)]))

    # --- PASO 2: DESGLOSE POR TÉRMINO ---
    resultados_parciales = []

    for i, t in enumerate(terminos):
        st.write(f"---")
        st.write(f"### 📝 Analizando Término {i+1}:")
        st.latex(f"f_{i+1}(x) = {sp.latex(t)}")

        # Extraer signo para explicar la técnica sobre el valor absoluto
        coeff, expr_base = t.as_coeff_Mul()
        signo = -1 if coeff < 0 else 1
        t_abs = t if signo == 1 else -t

        # --- A. DETECTAR COCIENTE ---
        num, den = sp.fraction(t_abs)
        if den != 1 and den.has(x):
            st.warning("**Técnica: Regla del Cociente**")
            st.latex(r"\frac{d}{dx}\left[\frac{u}{v}\right] = \frac{u'v - uv'}{v^2}")
            
            u, v = num, den
            du, dv = sp.diff(u, x), sp.diff(v, x)
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Identificar:**")
                st.latex(f"u = {sp.latex(u)}")
                st.latex(f"v = {sp.latex(v)}")
            with col2:
                st.write("**Derivar:**")
                st.latex(f"u' = {sp.latex(du)}")
                st.latex(f"v' = {sp.latex(dv)}")
            
            st.write("**Sustituir:**")
            res_t = (du*v - u*dv)/(v**2)
            st.latex(f"\\frac{{({sp.latex(du)})({sp.latex(v)}) - ({sp.latex(u)})({sp.latex(dv)})}}{{{sp.latex(v**2)}}}")

        # --- B. DETECTAR PRODUCTO ---
        elif t_abs.is_Mul and len([a for a in t_abs.args if a.has(x)]) > 1:
            st.warning("**Técnica: Regla del Producto**")
            st.latex(r"\frac{d}{dx}[u \cdot v] = u'v + uv'")
            
            factores = [a for a in t_abs.args if a.has(x)]
            constante = t_abs.as_coefficient(sp.Mul(*factores))
            
            u, v = factores[0], sp.Mul(*factores[1:])
            du, dv = sp.diff(u, x), sp.diff(v, x)

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Identificar:**")
                st.latex(f"u = {sp.latex(u)}")
                st.latex(f"v = {sp.latex(v)}")
            with col2:
                st.write("**Derivar:**")
                st.latex(f"u' = {sp.latex(du)}")
                st.latex(f"v' = {sp.latex(dv)}")

            st.write("**Sustituir:**")
            if constante != 1:
                st.latex(f"{sp.latex(constante)} \\cdot [({sp.latex(du)})({sp.latex(v)}) + ({sp.latex(u)})({sp.latex(dv)})]")
            else:
                st.latex(f"({sp.latex(du)})({sp.latex(v)}) + ({sp.latex(u)})({sp.latex(dv)})")

        # --- C. FORMAS GENERALIZADAS (SIN, COS, EXP) ---
        elif any(t_abs.has(getattr(sp, f)) for f in ["sin", "cos", "exp"]):
            # Identificar función y argumento
            f_interna = list(t_abs.atoms(sp.Function))[0] if t_abs.atoms(sp.Function) else list(t_abs.atoms(sp.exp))[0]
            arg = f_interna.args[0]
            a = sp.diff(arg, x)
            
            if t_abs.has(sp.sin):
                st.info("**Técnica: Forma General del Seno**")
                st.latex(r"\frac{d}{dx}[\sin(ax)] = a \cdot \cos(ax)")
            elif t_abs.has(sp.cos):
                st.info("**Técnica: Forma General del Coseno**")
                st.latex(r"\frac{d}{dx}[\cos(ax)] = -a \cdot \sin(ax)")
            elif t_abs.has(sp.exp):
                st.info("**Técnica: Forma General Exponencial**")
                st.latex(r"\frac{d}{dx}[e^{ax}] = a \cdot e^{ax}")

            st.write(f"Aquí $a = {sp.latex(a)}$.")
            st.write("**Resultado:**")
            st.latex(f"{sp.latex(sp.diff(t_abs, x))}")

        # --- D. POTENCIA ---
        else:
            st.info("**Técnica: Regla de la Potencia**")
            st.latex(r"\frac{d}{dx}[x^n] = n \cdot x^{n-1}")
            st.latex(f"\\implies {sp.latex(sp.diff(t_abs, x))}")

        # Almacenar resultado respetando el signo original
        resultados_parciales.append(sp.diff(t, x))

    # --- RESULTADO FINAL ---
    st.markdown("---")
    st.success("### ✅ Paso Final: Ensamblaje y Simplificación")
    res_final = sum(resultados_parciales)
    st.write("Sumando los resultados de cada término:")
    st.latex(f"f'(x) = {sp.latex(res_final)}")
    
    st.write("Simplificando algebraicamente:")
    st.latex(f"f'(x) = {sp.latex(sp.simplify(res_final))}")

except Exception as e:
    st.error(f"Error en la expresión. Asegúrate de usar '*' para multiplicar.")
