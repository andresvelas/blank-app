import streamlit as st
import random
import math

st.title("Juego Monty Hall Interactivo y Probabilístico (10 puertas)")
st.write("""
Bienvenida/o al juego de Monty Hall con **10 puertas**.  
Detrás de **9 puertas hay una cabra** y detrás de **1 el premio**.  
Vamos a explorar **probabilidades paso a paso** con apoyo visual y ecuaciones.
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
        color = "white"

        # Puerta abierta/cerrada
        if i in abiertas:
            # Si se revela el contenido
            if revelar and puertas_real is not None:
                if puertas_real[i] == 1:
                    texto = f"🚪 {puerta_num}\n🎁"
                else:
                    texto = f"🚪 {puerta_num}\n🐐"
            else:
                texto = f"🚪 {puerta_num}\n(abierta)"

        # Resaltar elección y otra puerta
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
                    background-color: {color};
                    white-space: pre-line;
                    font-size: 14px;
                ">
                {texto}
                </div>
                """,
                unsafe_allow_html=True
            )

# ---------- Paso 1: Elegir puerta ----------
if st.session_state.estado == 'inicio':
    st.write("Primero elige una puerta. Todas están cerradas:")
    dibujar_puertas(n=10)
    puerta = st.number_input("Elige una puerta del 1 al 10:", min_value=1, max_value=10, step=1)
    if st.button("Confirmar elección"):
        st.session_state.eleccion = puerta - 1
        # Crear puertas: 1 premio, 9 cabras
        st.session_state.puertas = [0]*9 + [1]
        random.shuffle(st.session_state.puertas)
        st.session_state.estado = 'pregunta_prob1'

# ---------- Paso 2: Probabilidad puerta elegida ----------
if st.session_state.estado == 'pregunta_prob1':
    st.write(f"Elegiste la puerta {st.session_state.eleccion+1}. Así se ve tu elección resaltada:")
    dibujar_puertas(n=10, eleccion=st.session_state.eleccion)
    prob_elegida = st.number_input(
        "¿Cuál crees que es la probabilidad de que el premio esté en tu puerta elegida?",
        min_value=0.0, max_value=1.0, step=0.01, key='prob1'
    )
    if st.button("Siguiente paso"):
        st.session_state.estado = 'pregunta_prob2'

# ---------- Paso 3: Probabilidad puertas restantes ----------
if st.session_state.estado == 'pregunta_prob2':
    st.write("Tu puerta está marcada con ⭐. Las otras 9 están cerradas:")
    dibujar_puertas(n=10, eleccion=st.session_state.eleccion)
    prob_restantes = st.number_input(
        "¿Cuál crees que es la probabilidad de que el premio esté en las **otras 9 puertas**?",
        min_value=0.0, max_value=1.0, step=0.01, key='prob2'
    )
    if st.button("Abrir 8 puertas sin premio"):
        # Monty abre 8 puertas con cabras que no son tu elección
        indices_posibles = [
            i for i in range(10)
            if i != st.session_state.eleccion and st.session_state.puertas[i] == 0
        ]
        st.session_state.puertas_abiertas = random.sample(indices_posibles, 8)
        # Determinar la única puerta cerrada restante (no elegida)
        st.session_state.otra_puerta = [
            i for i in range(10)
            if i != st.session_state.eleccion and i not in st.session_state.puertas_abiertas
        ][0]
        st.session_state.estado = 'pregunta_prob_condicional'

# ---------- Paso 4: Probabilidad condicional con ecuaciones ----------
if st.session_state.estado == 'pregunta_prob_condicional':
    st.write("Monty abre 8 puertas con cabras (marcadas como abiertas):")
    dibujar_puertas(
        n=10,
        abiertas=st.session_state.puertas_abiertas,
        eleccion=st.session_state.eleccion,
        otra_puerta=st.session_state.otra_puerta
    )

    st.write(f"Se abren las puertas { [i+1 for i in st.session_state.puertas_abiertas] } y todas tienen cabras.")
    st.write("Ahora solo quedan 2 puertas cerradas: tu elección inicial (⭐) y la otra puerta (👉).")

    prob_condicional = st.number_input(
        "Imagina que sabes que el premio está en una de las 2 puertas cerradas. "
        "¿Qué probabilidad le asignas a cada una?",
        min_value=0.0, max_value=1.0, step=0.01, key='prob_cond'
    )

    if st.button("Revelar resultado y explicación matemática"):
        st.write("✅ Explicación con probabilidad condicional (versión 10 puertas):")

        st.latex(r"P(\text{premio en tu puerta al inicio}) = \frac{1}{10}")
        st.latex(r"P(\text{premio en alguna de las otras 9}) = \frac{9}{10}")

        st.write("""
        Monty abre 8 puertas de las otras 9, todas con cabras, y deja solo **1 puerta cerrada** que no elegiste.  
        Esto no cambia la probabilidad inicial de tu puerta, pero concentra toda la probabilidad de las 9 puertas
        en esa única puerta que Monty dejó cerrada.
        """)

        st.latex(r"""
        P(\text{premio en tu puerta} \mid \text{información de Monty}) = \frac{1}{10}
        """)
        st.latex(r"""
        P(\text{premio en la otra puerta} \mid \text{información de Monty}) = \frac{9}{10}
        """)

        st.write("Si condicionamos solo a que el premio esté en una de las 2 puertas cerradas, entonces:")
        st.latex(r"""
        P(\text{tu puerta} \mid \text{premio en una de las 2}) 
        = \frac{\tfrac{1}{10}}{\tfrac{1}{10} + \tfrac{9}{10}} = \frac{1}{10}
        """)
        st.latex(r"""
        P(\text{otra puerta} \mid \text{premio en una de las 2}) 
        = \frac{\tfrac{9}{10}}{\tfrac{1}{10} + \tfrac{9}{10}} = \frac{9}{10}
        """)

        st.write("En otras palabras: cambiar de puerta multiplica por 9 tus probabilidades de ganar.")
        st.session_state.estado = 'resultado'

# ---------- Paso 5: Mostrar resultado y opción de cambiar ----------
if st.session_state.estado == 'resultado':
    st.write("Puertas justo antes de tu decisión final:")
    dibujar_puertas(
        n=10,
        abiertas=st.session_state.puertas_abiertas,
        eleccion=st.session_state.eleccion,
        otra_puerta=st.session_state.otra_puerta
    )

    cambiar = st.radio(
        f"Tu puerta actual es {st.session_state.eleccion+1} (⭐). "
        f"La otra puerta cerrada es {st.session_state.otra_puerta+1} (👉). ¿Deseas cambiar?",
        ('No', 'Sí')
    )
    if st.button("Mostrar resultado final"):
        if cambiar == 'Sí':
            st.session_state.eleccion = st.session_state.otra_puerta

        st.write("Estado final de todas las puertas (se revela el contenido):")
        dibujar_puertas(
            n=10,
            abiertas=list(range(10)),   # todas abiertas visualmente
            eleccion=st.session_state.eleccion,
            otra_puerta=None,
            revelar=True,
            puertas_real=st.session_state.puertas
        )

        if st.session_state.puertas[st.session_state.eleccion] == 1:
            st.success(f"🎉 ¡Felicidades! Has ganado el premio en la puerta {st.session_state.eleccion+1}.")
        else:
            st.error(f"🐐 Lo siento, hay una cabra detrás de la puerta {st.session_state.eleccion+1}.")
        st.session_state.estado = 'reinicio'

# ---------- Paso 6: Reinicio ----------
if st.session_state.estado == 'reinicio':
    if st.button("Volver a jugar"):
        st.session_state.estado = 'inicio'
        st.session_state.puertas = []
        st.session_state.eleccion = None
        st.session_state.puertas_abiertas = []
        st.session_state.otra_puerta = None
