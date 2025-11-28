import streamlit as st
import random

st.title("Juego Monty Hall con 10 puertas")

st.write("Detrás de 9 puertas hay una cabra y detrás de 1 el premio.")

# Selección de puerta
puerta = st.number_input("Elige una puerta del 1 al 10:", min_value=1, max_value=10, step=1)

if st.button("Jugar"):
    # Crear las puertas: 0 = cabra, 1 = premio
    puertas = [0]*9 + [1]
    random.shuffle(puertas)
    
    eleccion = puerta - 1  # convertir a índice 0-9

    # Monty abre 8 puertas sin premio y distintas a la elegida
    indices_posibles = [i for i in range(10) if i != eleccion and puertas[i] == 0]
    puertas_abiertas = random.sample(indices_posibles, 8)
    st.write(f"Se abren las puertas { [i+1 for i in puertas_abiertas] } y todas tienen cabras.")

    # Determinar la única puerta cerrada restante que no es la elegida
    otra_puerta = [i for i in range(10) if i != eleccion and i not in puertas_abiertas][0]

    # Preguntar si desea cambiar
    cambiar = st.radio(
        f"Tu puerta actual es {eleccion+1}. Si cambias, irías a la puerta {otra_puerta+1}. ¿Deseas cambiar?",
        ('No', 'Sí')
    )

    if cambiar == 'Sí':
        eleccion = otra_puerta

    # Mostrar resultado
    if puertas[eleccion] == 1:
        st.success(f"¡Felicidades! Has ganado el premio en la puerta {eleccion+1}.")
    else:
        st.error(f"Lo siento, hay una cabra detrás de la puerta {eleccion+1}. Mejor suerte la próxima vez.")

