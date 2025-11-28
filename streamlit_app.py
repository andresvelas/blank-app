import streamlit as st
import random
import math

st.title("Juego Monty Hall Interactivo y Probabilístico (10 puertas)")
st.write("""
Bienvenida/o al juego de Monty Hall con **10 puertas**.  
Detrás de **9 puertas hay una cabra** y detrás de **1 el premio**.  
Vamos a explorar **probabilidades paso a paso**, incluyendo probabilidades
condicionadas antes y después de que Monty abra puertas.
""")

# ---------- Estado ----------
if 'estado' not in st.session_state:
    st.session_state.estado = 'inicio'
    st.session_state.puertas = []
    st.session_state.eleccion = None
    st.session_state.puertas_abiertas = []
    st.session_state.otra_puerta = None

# Función auxiliar para dibujar puertas
def dibujar_puertas(n=10, abiertas=None, eleccion=None, otra_puerta=None, revelar=False, puertas_real=None):
    if abiertas is None:
        abiertas = []
    cols = st.columns(n)
    for i in range(n):
        puerta_num = i + 1
        texto = f"🚪 {puerta_num}"

        # Puerta abierta
        if i in abiertas:
            if revelar and puertas_real is not None:
                texto += "\n🎁" if puertas_real[i] == 1 else "\n🐐"
            else:
                texto += "\n(abierta)"

        # Marcar elección y puerta alternativa
        if eleccion is not None and i == eleccion:
            texto = "⭐ " + texto
        if otra_puerta is not None and i == otra_puerta:
            texto = "👉 " + texto

        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    border: 2px solid #555;
                    border-radius: 6px;
                    padding: 6px;
                    text-align: center;
                    white-space: pre-line;
                ">
                {texto}
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------- Inicio: elegir puerta ----------
if st.session_state.estado == 'inicio':
    st.write("Todas las puertas están cerradas. Elige una:")
    dibujar_puertas(10)
    puerta = st.number_input("Puerta elegida (1–10):", 1, 10, 1)
    if st.button("Confirmar elección"):
        st.session_state.eleccion = puerta - 1
        st.session_state.puertas = [0]*9 + [1]
        random.shuffle(st.session_state.puertas)
        st.session_state.estado = 'pregunta_prob1'

# ---------- Probabilidad de tu puerta ----------
if st.session_state.estado == 'pregunta_prob1':
    st.write(f"Elegiste la puerta {st.session_state.eleccion+1}.")
    dibujar_puertas(10, eleccion=st.session_state.eleccion)

    st.number_input(
        "¿Probabilidad de que el premio esté en tu puerta (antes de abrir)?",
        min_value=0.0, max_value=1.0, step=0.01, key="prob1"
    )

    if st.button("Siguiente"):
        st.session_state.estado = 'prob_puertas_9'

# ---------- Probabilidad de CADA una de las 9 puertas restantes ----------
if st.session_state.estado == 'prob_puertas_9':
    st.write("""
    Ahora piensa en las **9 puertas que NO elegiste**.

    Condiciona a que *sabes* que el premio está dentro de esas 9 puertas.
    ¿Cuál es la probabilidad de cada una de esas puertas?
    """)

    st.write("Visualización (⭐ = tu puerta):")
    dibujar_puertas(10, eleccion=st.session_state.eleccion)

    st.number_input(
        "¿Probabilidad de cada una de las 9 puertas (si sabes que el premio está en esas 9)?",
        min_value=0.0, max_value=1.0, step=0.01, key="prob_9"
    )

    if st.button("Monty abre 8 puertas sin premio"):
        # Monty abre 8 de las 9 puertas que no elegiste y que seguro tienen cabra
        indices_posibles = [
            i for i in range(10)
            if i != st.session_state.eleccion and st.session_state.puertas[i] == 0
        ]
        st.session_state.puertas_abiertas = random.sample(indices_posibles, 8)

        # La única que queda cerrada
        st.session_state.otra_puerta = [
            i for i in range(10)
            if i != st.session_state.eleccion and i not in st.session_state.puertas_abiertas
        ][0]

        st.session_state.estado = "prob_8_abiertas"

# ---------- Probabilidad de cada una de las 8 puertas abiertas ----------
if st.session_state.estado == 'prob_8_abiertas':
    st.write("""
    Monty ha abierto 8 puertas de las 9 que no elegiste y todas tienen cabra.
    Ahora condiciona de nuevo:

    *"Sabiendo que el premio estaba entre las 9 puertas que no elegiste,  
    ¿cuál es ahora la probabilidad de cada UNA de las 8 puertas abiertas?"*
    """)

    dibujar_puertas(
        10,
        abiertas=st.session_state.puertas_abiertas,
        eleccion=st.session_state.eleccion,
        otra_puerta=st.session_state.otra_puerta
    )

    st.number_input(
        "Probabilidad de CADA una de las 8 puertas abiertas:",
        min_value=0.0, max_value=1.0, step=0.01, key="prob_8"
    )

    if st.button("Continuar a probabilidad condicional de las 2 puertas cerradas"):
        st.session_state.estado = "pregunta_prob_condicional"

# ---------- Probabilidad condicional entre las 2 puertas cerradas ----------
if st.session_state.estado == 'pregunta_prob_condicional':
    st.write("""
    Solo quedan 2 puertas cerradas:
    - ⭐ tu puerta  
    - 👉 la única puerta no abierta entre las 9 restantes

    Si sabes que *el premio está entre estas 2*, reparte la probabilidad.
    """)

    dibujar_puertas(
        10,
        abiertas=st.session_state.puertas_abiertas,
        eleccion=st.session_state.eleccion,
        otra_puerta=st.session_state.otra_puerta
    )

    st.number_input(
        "¿Probabilidad de tu puerta (de las 2)?",
        min_value=0.0, max_value=1.0, step=0.01, key="prob_cond_2"
    )

    if st.button("Ver explicación matemática"):
        st.session_state.estado = "resultado_exp"

# ---------- Explicación completa ----------
if st.session_state.estado == 'resultado_exp':
    st.write("### 📘 Explicación matemática final")
    st.write("Las probabilidades reales son:")
    st.latex(r"P(\text{tu puerta}) = \frac{1}{10}")
    st.latex(r"P(\text{otra puerta}) = \frac{9}{10}")

    st.write("Puedes decidir si quieres cambiar:")
    st.session_state.estado = 'decision'

# ---------- Decisión final ----------
if st.session_state.estado == 'decision':
    cambiar = st.radio(
        f"¿Quieres cambiar a la puerta {st.session_state.otra_puerta+1}?",
        ("No", "Sí")
    )

    if st.button("Mostrar resultado final"):
        if cambiar == "Sí":
            st.session_state.eleccion = st.session_state.otra_puerta

        dibujar_puertas(
            10,
            abiertas=list(range(10)),
            revelar=True,
            eleccion=st.session_state.eleccion,
            puertas_real=st.session_state.puertas
        )

        if st.session_state.puertas[st.session_state.eleccion] == 1:
            st.success("🎉 ¡Ganaste el premio!")
        else:
            st.error("🐐 ¡Cabrón! (solo era una cabra...)")

        st.session_state.estado = "reinicio"

# ---------- Reinicio ----------
if st.session_state.estado == "reinicio":
    if st.button("Jugar de nuevo"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
