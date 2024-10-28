"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

df

st.write("Here's our first attempt at using data to create a table:")
st.write(pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
}))

st.write("Aleatorio con numpy:")
dataframe = np.random.randn(10, 20)
st.dataframe(dataframe)

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))


dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))
st.table(dataframe)

st.write("Draw a line chart:")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.line_chart(chart_data)


st.write("Plot a map:")

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [-31.5, -63.5],
    columns=['lat', 'lon'])

st.map(map_data)

st.write("widgets:")
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'el cuadrado es:', x * x)

# cuadra de dialogo
st.text_input("Ingresa tu nombre", key="name")

# llama a la variable
st.session_state.name
