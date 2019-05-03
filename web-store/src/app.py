from flask import Flask, render_template, redirect, url_for, request
import pymysql #biblioteca para cominicarnos con sql

conn = pymysql.connect('', 'root', 'root', 'cesdestore')
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/add')
def add():
    return render_template('add_product.html')

@app.route('/add_product', methods=['POST'])
def add_product():
    if request.method == "POST":
        producto = request.form['producto']
        valor = request.form['valor']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        cur = conn.cursor()
        cur.execute("INSERT INTO productos(producto,valor,categoria,descripcion)VALUE(%s,%s,%s,%s)",(producto, valor, categoria, descripcion))
        conn.commit()
        cur.close
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(port=4200,debug=True)