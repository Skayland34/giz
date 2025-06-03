
from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import plotly.express as px
import plotly.io as pio
import sqlite3

app = Flask(__name__)
app.secret_key = 'clave-secreta'  # Necesario para usar sesiones y flash

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['contraseña']

        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE usuario = ? AND contraseña = ?', (usuario, clave))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['usuario'] = usuario
            return redirect(url_for('pagina_principal'))  # para pasar a la pagina principal 
        else:
            flash('Usuario o contraseña incorrectos.')

    return render_template('registro.html')  # para iniciar sesión revisar nombre del template

@app.route('/register', methods=['POST'])
def register():
    nombre = request.form['nombre_completo']
    tipo_doc = request.form['tipo_documento']
    num_doc = request.form['numero_documento']
    correo = request.form['correo']
    celular = request.form['celular']
    usuario = request.form['usuario']
    contraseña = request.form['contraseña']

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO usuarios (nombre_completo, tipo_documento, numero_documento, correo, celular, usuario, contraseña)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, tipo_doc, num_doc, correo, celular, usuario, contraseña))
    conn.commit()
    conn.close()

    flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.')
    return redirect(url_for('login'))

@app.route('/principal')
def pagina_principal():
    if 'usuario' not in session:
        flash('Debes iniciar sesión primero.')
        return redirect(url_for('login'))


    # Cargar y procesar datos
    data = pd.read_excel("indicador31.xlsx")
    data.columns = data.columns.str.strip()

    fig1 = px.bar(data, 
                 x="Región(es) en la que se implementa",
                 title="Cantidad de iniciativas por región",
                 labels={"x": "Región", "count": "Cantidad"},
                 color="Región(es) en la que se implementa")

    fig2 = px.pie(data, 
                 names="Estado del proceso", 
                 title="Distribución de los estados del proceso")

    conteo_sostenibilidad = data["¿La iniciativa tiene una forma de hacer seguimiento o estrategia de sostenibilidad?"].value_counts().reset_index()
    conteo_sostenibilidad.columns = ["Tiene_sostenibilidad", "Cantidad"]
    fig3 = px.bar(conteo_sostenibilidad,
                 x="Tiene_sostenibilidad",
                 y="Cantidad",
                 text_auto=True,
                 title="Estrategia de sostenibilidad en iniciativas",
                 labels={"Tiene_sostenibilidad": "¿Tiene sostenibilidad?", "Cantidad": "Cantidad"})

    data.rename(columns={
        "Participantes directos (OSIGD)": "Participantes",
        "Región(es) en la que se implementa": "Region",
        "Periodo de implementación": "Periodo",
        "Población objetivo de la iniciativa": "Estrato"
    }, inplace=True)

    region_participantes = data.groupby("Region")["Participantes"].sum().reset_index()
    fig4 = px.bar(region_participantes,
                  x="Participantes",
                  y="Region",
                  text_auto=True,
                  title="Total de Participantes OSIGD por Región",
                  text="Participantes",
                  labels={"Participantes": "N° de Participantes"},
                  template="plotly_white")
    fig4.update_traces(textposition="outside")

    cruce_region_poblacion = data.groupby(["Region", "Estrato"])["Participantes"].sum().reset_index()
    fig5 = px.bar(cruce_region_poblacion,
                  x="Region",
                  y="Participantes",
                  color="Estrato",
                  text_auto=True,
                  barmode="group",
                  title="Participantes por Región y Población Objetivo",
                  labels={"Participantes": "N° de Participantes"},
                  template="plotly_white")

    data["Poblacion_objetivo"] = pd.factorize(data["Estrato"])[0]
    fig6 = px.scatter_3d(data,
                        x="Poblacion_objetivo",
                        y="Participantes",
                        z="Periodo",
                        color="Region",
                        hover_name="Estrato",
                        title="Participantes por Población Objetivo",
                        labels={"Participantes": "N° de Participantes"},
                        template="plotly_dark")

    totalizados = data.groupby(["Region","Estrato"])["Participantes directos (mujeres)"].sum().reset_index()
    top = totalizados.sort_values("Estrato", ascending=False).head(10)
    top["Trazabilidad"] = "Escala"
    fig7 = px.line_3d(top, 
                     x="Region", 
                     y="Participantes directos (mujeres)",
                     z="Estrato",
                     color="Trazabilidad",
                     color_discrete_sequence=["Green"])

    graphs = {
        "graph1": pio.to_html(fig1, full_html=False),
        "graph2": pio.to_html(fig2, full_html=False),
        "graph3": pio.to_html(fig3, full_html=False),
        "graph4": pio.to_html(fig4, full_html=False),
        "graph5": pio.to_html(fig5, full_html=False),
        "graph6": pio.to_html(fig6, full_html=False),
        "graph7": pio.to_html(fig7, full_html=False)
    }

    return render_template("principal.html", **graphs)


if __name__ == '__main__':
    app.run(debug=True)
