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
    * **Ejemplo:** `x^2 - sin(3*x)`
    """)

# --- BLOQUE 1: ENTRADA ---
u_input = st.text_input("Ingresa la función a derivar:", value="x^2 - sin(3*x)")

x = sp.symbols('x')

try:
    input_proc = u_input.replace("^", "**").replace("e**", "exp")
    h = sp.sympify(input_proc)
    
    st.info("#### 👁️ Vista Previa:")
    st.latex(f"f(x) = {sp.latex(h)}")
    st.markdown("---")

    # --- PASO 1: IDENTIFICAR ESTRUCTURA (SUMA O RESTA) ---
    terminos = sp.Add.make_args(h)
    
    st.write(f"### 🔍 Paso 1: Análisis de estructura")
    
    # Determinar si es suma, resta o ambas
    tiene_positivos = any(t.as_coeff_Mul()[0] > 0 for t in terminos)
    tiene_negativos = any(t.as_coeff_Mul()[0] < 0 for t in terminos)
    
    if tiene_positivos and tiene_negativos:
        st.write("La función presenta **sumas y restas**. Aplicamos la regla de linealidad:")
        st.latex(r"\frac{d}{dx}[f(x) \pm g(x)] = \frac{d}{dx}f(x) \pm \frac{d}{dx}g(x)")
    elif tiene_negativos:
        st.write("La estructura principal es una **resta**. Aplicamos la regla:")
        st.latex(r"\frac{d}{dx}[f(x) - g(x)] = \frac{d}{dx}f(x) - \frac{d}{dx}g(x)")
    else:
        st.write("La estructura principal es una **suma**. Aplicamos la regla:")
        st.latex(r"\frac{d}{dx}[f(x) + g(x)] = \frac{d}{dx}f(x) + \frac{d}{dx}g(x)")

    # --- PASO 2: DESGLOSE POR TÉRMINO ---
    resultados_parciales = []

    for i, t in enumerate(terminos):
        # Extraer el signo y la expresión positiva para explicar la técnica
        coeff, expr_base = t.as_coeff_Mul()
        signo_texto = "Positivo (+)" if coeff > 0 else "Negativo (-)"
        t_abs = t if coeff > 0 else -t
        
        st.write(f"---")
        st.write(f"### 📝 Analizando Término {i+1} ({signo_texto}):")
        st.latex(f"{sp.latex(t)}")

        # --- A. DETECTAR COCIENTE ---
        num, den = sp.fraction(t_abs)
        if den != 1 and den.has(x):
            st.warning("**Técnica: Regla del Cociente**")
            st.latex(r"\frac{d}{dx}\left[\frac{u}{v}\right] = \frac{u'v - uv'}{v^2}")
            u, v = num, den
            du, dv = sp.diff(u, x), sp.diff(v, x)
            
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Identificar:**")
                st.latex(f"u = {sp.latex(u)}, v = {sp.latex(v)}")
            with c2:
                st.write("**Derivar:**")
                st.latex(f"u' = {sp.latex(du)}, v' = {sp.latex(dv)}")
            
            der_paso = (du*v - u*dv)/(v**2)

        # --- B. DETECTAR PRODUCTO ---
        elif t_abs.is_Mul and len([a for a in t_abs.args if arg.has(x) for arg in [a]]) > 1:
            st.warning("**Técnica: Regla del Producto**")
            st.latex(r"\frac{d}{dx}[u \cdot v] = u'v + uv'")
            
            factores = [a for a in t_abs.args if a.has(x)]
            constante = t_abs.as_coefficient(sp.Mul(*factores))
            u, v = factores[0], sp.Mul(*factores[1:])
            du, dv = sp.diff(u, x), sp.diff(v, x)

            c1, c2 = st.columns(2)
            with c1:
                st.write("**Identificar:**")
                st.latex(f"u = {sp.latex(u)}, v = {sp.latex(v)}")
            with c2:
                st.write("**Derivar:**")
                st.latex(f"u' = {sp.latex(du)}, v' = {sp.latex(dv)}")
            
            der_paso = (du*v + u*dv) * constante

        # --- C. FORMAS GENERALIZADAS ---
        elif any(t_abs.has(getattr(sp, f)) for f in ["sin", "cos", "exp"]):
            if t_abs.has(sp.sin):
                st.info("**Técnica: Forma General del Seno**")
                st.latex(r"\frac{d}{dx}[\sin(ax)] = a \cdot \cos(ax)")
            elif t_abs.has(sp.cos):
                st.info("**Técnica: Forma General del Coseno**")
                st.latex(r"\frac{d}{dx}[\cos(ax)] = -a \cdot \sin(ax)")
            elif t_abs.has(sp.exp):
                st.info("**Técnica: Forma General Exponencial**")
                st.latex(r"\frac{d}{dx}[e^{ax}] = a \cdot e^{ax}")

            # Extraer 'a'
            f_interna = list(t_abs.atoms(sp.Function))[0] if t_abs.atoms(sp.Function) else list(t_abs.atoms(sp.exp))[0]
            a = sp.diff(f_interna.args[0], x)
            st.write(f"Donde el coeficiente interno es $a = {sp.latex(a)}$")
            der_paso = sp.diff(t_abs, x)

        # --- D. POTENCIA ---
        else:
            st.info("**Técnica: Regla de la Potencia**")
            st.latex(r"\frac{d}{dx}[x^n] = n \cdot x^{n-1}")
            der_paso = sp.diff(t_abs, x)

        # Mostrar resultado del término manteniendo el signo
        st.write("**Resultado de este término:**")
        if coeff < 0:
            st.latex(f"- ({sp.latex(der_paso)})")
        else:
            st.latex(f"{sp.latex(der_paso)}")
            
        resultados_parciales.append(sp.diff(t, x))

    # --- RESULTADO FINAL ---
    st.markdown("---")
    st.success("### ✅ Paso Final: Resultado Ensamblado")
    res_final = sum(resultados_parciales)
    
    # Construcción visual de la suma/resta final
    st.write("Uniendo los términos según sus signos originales:")
    st.latex(f"f'(x) = {sp.latex(res_final)}")
    
    st.write("**Resultado Simplificado:**")
    st.latex(f"f'(x) = {sp.latex(sp.simplify(res_final))}")

except Exception as e:
    st.error(f"Error: Asegúrate de usar '*' para multiplicar (ej: 5*x).")
