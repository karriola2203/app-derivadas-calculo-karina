import streamlit as st
import sympy as sp

# Configuración de la página
st.set_page_config(page_title="Tutor de Cálculo: Cátedra Arriola", layout="wide")

st.title("🏛️ Tutor de Derivación Detallada")
st.subheader("Arquitectura | UPC")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("📖 Guía de Escritura")
    st.markdown("""
    * **Multiplicación:** `5*x`
    * **Potencia:** `x^2`
    * **División:** `(x+1)/x`
    * **Resta:** `x^2 - 5*x`
    """)

# --- BLOQUE 1: ENTRADA ---
u_input = st.text_input("Ingresa la función a derivar:", value="x^2 - sin(3*x)")

x = sp.symbols('x')

try:
    # Pre-procesamiento
    input_proc = u_input.replace("^", "**").replace("e**", "exp")
    h = sp.sympify(input_proc)
    
    st.info("#### 👁️ Vista Previa del Alumno:")
    st.latex(f"f(x) = {sp.latex(h)}")
    st.markdown("---")

    # --- PASO 1: IDENTIFICAR TÉRMINOS Y OPERADORES ---
    # Separamos los términos
    raw_terminos = sp.Add.make_args(h)
    
    # Creamos una lista de términos positivos y sus signos correspondientes
    lista_analisis = []
    for t in raw_terminos:
        coeff, expr = t.as_coeff_Mul()
        if coeff < 0:
            lista_analisis.append({"expr": -t, "signo": "-"})
        else:
            lista_analisis.append({"expr": t, "signo": "+"})

    st.write(f"### 🔍 Paso 1: Identificación de Operaciones")
    st.write(f"La función tiene **{len(lista_analisis)} términos**.")
    
    # Mostrar la regla de Suma/Resta pura
    formula_visual = "f'(x) = "
    for i, item in enumerate(lista_analisis):
        operador = item['signo'] if i > 0 else ("-" if item['signo'] == "-" else "")
        formula_visual += f" {operador} \\frac{{d}}{{dx}}({sp.latex(item['expr'])})"
    
    st.latex(formula_visual)
    
    st.write("---")

    # --- PASO 2: DESGLOSE TÉRMINO POR TÉRMINO (SIEMPRE POSITIVOS) ---
    derivadas_finales = []

    for i, item in enumerate(lista_analisis):
        t_pos = item['expr']
        sig = item['signo']
        
        st.write(f"### 📝 Derivando Término {i+1}:")
        st.latex(f"u_{i+1} = {sp.latex(t_pos)}")

        # --- CLASIFICACIÓN TÉCNICA ---
        # 1. COCIENTE
        num, den = sp.fraction(t_pos)
        if den != 1 and den.has(x):
            st.warning("**Técnica: Regla del Cociente**")
            st.latex(r"\frac{d}{dx}\left[\frac{u}{v}\right] = \frac{u'v - uv'}{v^2}")
            
            u, v = num, den
            du, dv = sp.diff(u, x), sp.diff(v, x)
            
            c1, col2 = st.columns(2)
            with c1:
                st.write("**Componentes:**")
                st.latex(f"u = {sp.latex(u)}, v = {sp.latex(v)}")
            with col2:
                st.write("**Derivadas:**")
                st.latex(f"u' = {sp.latex(du)}, v' = {sp.latex(dv)}")
            
            der_calculada = (du*v - u*dv)/(v**2)

        # 2. PRODUCTO
        elif t_pos.is_Mul and len([a for a in t_pos.args if a.has(x)]) > 1:
            st.warning("**Técnica: Regla del Producto**")
            st.latex(r"\frac{d}{dx}[u \cdot v] = u'v + uv'")
            
            factores = [a for a in t_pos.args if a.has(x)]
            constante = t_pos.as_coefficient(sp.Mul(*factores))
            u, v = factores[0], sp.Mul(*factores[1:])
            du, dv = sp.diff(u, x), sp.diff(v, x)

            c1, col2 = st.columns(2)
            with c1:
                st.write("**Componentes:**")
                st.latex(f"u = {sp.latex(u)}, v = {sp.latex(v)}")
            with col2:
                st.write("**Derivadas:**")
                st.latex(f"u' = {sp.latex(du)}, v' = {sp.latex(dv)}")
            
            der_calculada = (du*v + u*dv) * constante

        # 3. FORMAS GENERALIZADAS
        elif any(t_pos.has(getattr(sp, f)) for f in ["sin", "cos", "exp"]):
            if t_pos.has(sp.sin):
                st.info("**Técnica: Forma General del Seno**")
                st.latex(r"\frac{d}{dx}[\sin(ax)] = a \cdot \cos(ax)")
                
            elif t_pos.has(sp.cos):
                st.info("**Técnica: Forma General del Coseno**")
                st.latex(r"\frac{d}{dx}[\cos(ax)] = -a \cdot \sin(ax)")
            elif t_pos.has(sp.exp):
                st.info("**Técnica: Forma General Exponencial**")
                st.latex(r"\frac{d}{dx}[e^{ax}] = a \cdot e^{ax}")
                

            f_interna = list(t_pos.atoms(sp.Function))[0] if t_pos.atoms(sp.Function) else list(t_pos.atoms(sp.exp))[0]
            a = sp.diff(f_interna.args[0], x)
            st.write(f"Donde el coeficiente interno es $a = {sp.latex(a)}$")
            der_calculada = sp.diff(t_pos, x)

        # 4. POTENCIA
        else:
            st.info("**Técnica: Regla de la Potencia**")
            st.latex(r"\frac{d}{dx}[x^n] = n \cdot x^{n-1}")
            
            der_calculada = sp.diff(t_pos, x)

        st.write(f"Resultado de derivar el término {i+1}:")
        st.latex(f"{sp.latex(der_calculada)}")
        
        # Guardamos la derivada multiplicada por su signo original para el ensamble
        derivadas_finales.append(der_calculada if sig == "+" else -der_calculada)
        st.write("---")

    # --- PASO 3: ENSAMBLAJE FINAL ---
    st.success("### ✅ Paso Final: Ensamblaje según Suma/Resta")
    st.write("Unimos los resultados respetando los signos de la función original:")
    
    res_final = sum(derivadas_finales)
    st.latex(f"f'(x) = {sp.latex(res_final)}")
    
    st.write("**Resultado Simplificado Final:**")
    st.latex(f"f'(x) = {sp.latex(sp.simplify(res_final))}")

except Exception as e:
    st.error("Error en la lectura de la función. Revisa que uses '*' para multiplicar.")  
