from flask import Flask, render_template, redirect, url_for, request
import pymysql #biblioteca para cominicarnos con sql

conn = pymysql.connect('', 'root', 'root', 'cesdestore')
app = Flask(__name__)

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos")
    productos = cur.fetchall()
    print(productos)
    return render_template('index.html',data = productos)

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


@app.route('/update/<id>')
def update(id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos WHERE id={0}".format(id))
    productos= cur.fetchall()

    return render_template('update_product.html',productos = productos[0])

@app.route('/update_product/<id>', methods=['POST'])
def update_product(id):
    # el name en los inputs debe coincidir con el nombre de los campos en la tabla de la base de datos
    if request.method == 'POST':
        producto = request.form['producto']
        valor = request.form['valor']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        cur = conn.cursor()
        cur.execute("""
            UPDATE productos
            SET producto = '{0}',
                valor = '{1}',
                categoria = '{2}',
                descripcion = '{3}'
            WHERE id = {4}
        """.format(producto, valor, categoria, descripcion,id))

    return redirect(url_for('index'))




@app.route('/delete/<id>')
def delete(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM productos WHERE id={0}".format(id))
    conn.commit()
    cur.close()
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(port=4200,debug=True)