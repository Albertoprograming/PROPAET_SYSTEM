from flask import Flask, request, render_template, redirect, url_for
import psycopg2
from dotenv import load_dotenv
import os
from flask import send_from_directory


# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), "uploads")


# Función para conectar a PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )


@app.route("/", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        motivo = request.form["motivo"]
        fecha_inicio = request.form["fecha_inicio"]
        fecha_fin = request.form["fecha_fin"]
        monto = request.form["monto"]
        num_exp = request.form["num_exp"]
        telefono = request.form["telefono"]
        firma = request.form["firma"]
        archivo = request.files["archivo_pdf"]

        if archivo:
            filename = archivo.filename
            archivo_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            archivo.save(archivo_path)

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO registros (
                    nombre, motivo, fecha_inicio, fecha_fin, monto,
                    num_exp, telefono, firma, archivo_pdf
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
                (
                    nombre,
                    motivo,
                    fecha_inicio,
                    fecha_fin,
                    monto,
                    num_exp,
                    telefono,
                    firma,
                    filename,
                ),
            )
            conn.commit()
            cur.close()
            conn.close()

            return redirect(url_for("registro"))

    return render_template("registro.html")


@app.route("/historial")
def historial():
    archivos = os.listdir(app.config["UPLOAD_FOLDER"])
    archivos = [archivo for archivo in archivos if archivo.endswith(".pdf")]
    return render_template("historial.html", archivos=archivos)


@app.route("/ver_pdf/<nombre_archivo>")
def ver_pdf(nombre_archivo):
    return send_from_directory(app.config["UPLOAD_FOLDER"], nombre_archivo)


if __name__ == "__main__":
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    app.run(host="0.0.0.0", port=5000, debug=True)
