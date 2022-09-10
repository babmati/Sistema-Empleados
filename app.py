import pymysql
import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from datetime import datetime
import os
from flask import send_from_directory

import re






app= Flask(__name__)
app.secret_key = "Byron'smind"

# esta conexion a la base no funciono 
"""////////////////Primer Codigo
mysql = MySQL()
app.config['MySQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3306
app.config['MySQL_USER'] = 'root'
app.config['MySQL_PASSWORD'] ='nico123'
app.config['MySQL_DB'] = 'sistema'
mysql.init_app(app)
conn= mysql.connect()s
//////////////////////////////////////////"""





 #segundo codigo , este conexion a la base si funciono 
try:

    conexion = mysql.connector.connect(
        host='localhost',
        port =3306,
        user='root', 
        passwd='nico123', 
        database='sistema'
    )


finally:
    print("conexion abierta no cierre")


CARPETA = os.path.join('uploads')
app.config['CARPETA']= CARPETA


@app.route("/uploads/<nombrefoto>")
def uploads(nombrefoto):

    return send_from_directory(app.config['CARPETA'], nombrefoto)



@app.route('/')
def index():

  #  """  Primer Codigo///////////////////
    cur = conexion.cursor()
    cur.execute("SELECT * FROM empleados")
   #conexion.commit()
    empleados = cur.fetchall()

    
    print(empleados)
   
#aca se estan enviando los atravez del render template 
    return render_template('empleados/index.html', empleados = empleados)


# Esto le da la direccion al folder o al nombre del form de html en este caso metodo POST
@app.route('/add_contact', methods=['POST']) 
def add_contact():


  if request.method == 'POST':
   #id= request.form['NUll']
   nombre= request.form['nombre']
   correo= request.form['correo']
   foto= request.form['foto']
   cur = conexion.cursor()
   cur.execute('INSERT INTO empleados ( nombre, correo, foto) VALUES ( %s ,%s , %s)',
   ( nombre, correo, foto))
   conexion.commit()

   return render_template('empleados/create.html')
   




# Codigo de borrar usuarios 
@app.route('/destroy/<int:id>')
def destroy(id):

    cur = conexion.cursor()
     # Este codigo debe borrar la foto pero no esta funcionando por path of the file 
    cur.execute("SELECT foto FROM empleados WHERE id=%s",[id])
    fila= cur.fetchall()
    if fila[0][0]!='':
     os.remove(os.path.join(CARPETA,fila[0][0]))
     
    cur.execute('DELETE FROM empleados WHERE id=%s', [id])
    conexion.commit()
    return redirect('/')




# Codigo de editar usuarios/ selecciona la informacion del usuario q quiero editar y la imprime 
@app.route('/edit/<int:id>')
def edit(id):
    cur = conexion.cursor()
    cur.execute("SELECT * FROM empleados WHERE id=%s", [id])
    empleados = cur.fetchall()
    conexion.commit()

    return render_template('empleados/edit.html', empleados =empleados)






@app.route('/update', methods=['POST'])
def update():

  if request.method == 'POST':

   nombre= request.form['txtNombre']
   correo= request.form['txtCorreo']
   foto= request.files['txtFoto']
   id= request.form['txtID']  
   
   cur = conexion.cursor()
   cur.execute("""UPDATE  empleados  SET nombre =%s, correo =%s WHERE id =%s""",(nombre, correo, id))
   
   
   now= datetime.now()
   tiempo= now.strftime("%Y%H%M%S")

   

   if foto.filename != '':
    nuevoNombreFoto= tiempo+foto.filename
    foto.save("uploads/"+ nuevoNombreFoto)

    cur.execute("SELECT foto FROM empleados WHERE id=%s",[id])
    fila= cur.fetchall()


    #os.remove(os.path.join(app.config['CARPETA'],fila[0][0]))
   #este codigo entra a la carpeta y borra la foto original pero esta dando error de path
    cur.execute("UPDATE empleados SET foto=%s WHERE id=%s",(nuevoNombreFoto,id))
 

   
   conexion.commit()
   return redirect('/')





#nuevo form del archivo create.html
@app.route("/create")
def create():

    return render_template('empleados/create.html')





@app.route('//store', methods=['POST'])
def storage():

   nombre= request.form['txtNombre']
   correo= request.form['txtCorreo']
   foto= request.files['txtFoto']

   if nombre =='' or correo=='':
    flash('Recuerda llenar los datos del empleado')
    return redirect(url_for('create'))
  


   now = datetime.now()
   tiempo = now.strftime("%Y%H%M%S")

   if foto.filename != '':

    nuevoNombreFoto = tiempo+foto.filename
    foto.save("uploads/"+nuevoNombreFoto)

    cur = conexion.cursor()
    cur.execute('INSERT INTO empleados ( nombre, correo, foto) VALUES ( %s ,%s , %s)',
    ( nombre, correo, nuevoNombreFoto)) ###aca esta el error de si carga o no la foto
    conexion.commit()
    
   if foto.filename == '':
        cur = conexion.cursor()
        cur.execute('INSERT INTO empleados ( nombre, correo, foto) VALUES ( %s ,%s , %s)',
        ( nombre, correo, foto.filename)) ###aca esta el error de si carga o no la foto
        conexion.commit()

   
   return redirect('/')




   """Codido del login"""""""""""""""""""""""""""""""""""""""""""""""""""""""""

# @app.route('/login')
# def login():


#     return render_template('empleados/login.html')


# @app.route('/verificar', methods=['GET' , 'POST'])
# def verificar():

#  usuario = request.form['txt.Usuario']
#  contraseña = request.form['txt.Contraseña']

#  cur = conexion.cursor()
#  cur.execute('SELECT  * FROM login WHERE usuario =%s', (usuario))
#  row = cur.fetchall()

# if usuario ==row[0] and password==row[1]
  





if __name__=='__main__':
    app.run(debug=True)
 

