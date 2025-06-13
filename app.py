# Proyecto Flask para análisis económico (backend)
# Guarda este archivo como app.py

from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import os
import uuid

app = Flask(__name__)

# Función para calcular elasticidad
def calcular_elasticidad(porcentaje_cambio_cantidad, porcentaje_cambio_precio):
    try:
        return porcentaje_cambio_cantidad / porcentaje_cambio_precio
    except ZeroDivisionError:
        return float('inf')

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para análisis de demanda y oferta
@app.route('/demanda_oferta', methods=['POST'])
def demanda_oferta():
    precios = list(map(float, request.form['precios'].split(',')))
    demanda = list(map(float, request.form['demanda'].split(',')))
    oferta = list(map(float, request.form['oferta'].split(',')))

    plt.figure()
    plt.plot(precios, demanda, label='Demanda', marker='o')
    plt.plot(precios, oferta, label='Oferta', marker='x')
    plt.xlabel('Precio')
    plt.ylabel('Cantidad')
    plt.title('Curvas de Demanda y Oferta')
    plt.legend()
    plt.grid(True)

    nombre_imagen = f'static/{uuid.uuid4().hex}.png'
    plt.savefig(nombre_imagen)
    plt.close()

    resultado = ""
    if len(precios) >= 2:
        delta_qd = (demanda[1] - demanda[0]) / demanda[0] * 100
        delta_p = (precios[1] - precios[0]) / precios[0] * 100
        elasticidad = calcular_elasticidad(delta_qd, delta_p)

        resultado += f"Elasticidad precio de la demanda: {elasticidad:.2f}<br>"
        if abs(elasticidad) > 1:
            resultado += "La demanda es elástica, bajar precios puede aumentar ingresos."
        elif abs(elasticidad) < 1:
            resultado += "La demanda es inelástica, subir precios puede aumentar ingresos."
        else:
            resultado += "Elasticidad unitaria."
    else:
        resultado = "Se requieren al menos 2 puntos para calcular elasticidad."

    return render_template('resultado.html', resultado=resultado, imagen=nombre_imagen)

# Ruta para análisis macroeconómico
@app.route('/macroeconomia', methods=['POST'])
def macroeconomia():
    años = request.form['años'].split(',')
    pib = list(map(float, request.form['pib'].split(',')))
    inflacion = list(map(float, request.form['inflacion'].split(',')))
    desempleo = list(map(float, request.form['desempleo'].split(',')))

    plt.figure()
    plt.plot(años, pib, label='PIB')
    plt.plot(años, inflacion, label='Inflación')
    plt.plot(años, desempleo, label='Desempleo')
    plt.xlabel('Año')
    plt.title('Indicadores Macroeconómicos')
    plt.legend()
    plt.grid(True)

    nombre_imagen = f'static/{uuid.uuid4().hex}.png'
    plt.savefig(nombre_imagen)
    plt.close()

    resultado = ""
    for i in range(1, len(años)):
        crecimiento_pib = ((pib[i] - pib[i-1]) / pib[i-1]) * 100
        resultado += f"Crecimiento del PIB de {años[i-1]} a {años[i]}: {crecimiento_pib:.2f}%<br>"

    if inflacion[-1] > 10:
        resultado += "Alta inflación. Recomendación: política monetaria restrictiva.<br>"
    if desempleo[-1] > 8:
        resultado += "Alto desempleo. Recomendación: estímulos fiscales o empleo público.<br>"

    return render_template('resultado.html', resultado=resultado, imagen=nombre_imagen)

# Ejecutar la app
if __name__ == '__main__':
    import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

