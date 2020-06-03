
#importamos archivos que utilizaremos 
from flask import Flask, render_template, request, redirect, url_for, flash # importamos la libreria (frenwork) de Flask para utilizar sus propiedades
from flask_mysqldb import MySQL
app = Flask(__name__) # obtenemos un abjeto 

#Datos para inicar el objeto con mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'personas'
#pasamos los datos de secion y listo 
mysql = MySQL(app)

#la yave de seguridad
app.secret_key = 'mysecretkey'


#ruta principal la cual abrira mi archivo al cargarse
@app.route('/')
def Index(): #creamos una funcion 
	cursor = mysql.connection.cursor() #almasenamos el objeto de conexion
	cursor.execute('SELECT * FROM contactos') #utilizamos el execut para realizar una consulta ala BD
	datos = cursor.fetchall() #almasenamos los datos de la consulta fetchall es para no quedar atrapado por algun error inesperado
	if datos:
		return render_template('index.html', contactos = datos) #render template nos ayuda a cargar una pagina
	#y poder pasar datos en este caso le doy mi diccionario de datos
	else:
		flash('NO HAY DATOS PARA MOSTRAR')
		return render_template('index.html', contactos = datos)


@app.route('/buscar_dato', methods=['POST'])
def buscando_dato(): #creamos una funcion
	if request.method == 'POST':
		id_recibido = request.form['id'] 
		cursor = mysql.connection.cursor() #almasenamos el objeto de conexion
		#cursor.execute('SELECT FROM contactos WHERE \'nombre\' LIKE \'{0}\''.format(nombre_recibido)) #utilizamos el execut para realizar una consulta ala BD
		cursor.execute('SELECT * FROM contactos WHERE id = {0}'.format(id_recibido))
		datos = cursor.fetchall() #almasenamos los datos de la consulta fetchall es para no quedar atrapado por algun error inesperado
		
		if datos:
			flash('ID encontrado')
			return render_template('index.html', contactos = datos)
		else:
			flash('El ID no se encontro')
			return redirect(url_for('Index'))
		 #render template nos ayuda a cargar una pagina
	#y poder pasar datos en este caso le doy mi diccionario de datos

#creamos una nueva ruta que resivira algo con el metodo post
@app.route('/agregar_contacto', methods=['POST']) 
def agregar_contacto(): 
	if request.method == 'POST': #verificamos que venga por el metodo POST
		nombre_recibido = request.form['nombre'] #recuperamos los datos del html y los guardamos en una variable
		telefono_recibido = request.form['telefono']
		correo_recibido = request.form['correo']
		TC = telefono_recibido.isdigit() #metodo que nos ayuda si la cadena contiene puras letras 
		NC = nombre_recibido.isspace() #metodo que nos ayuda a sabir si la cadena contiene solo espasios
		CV = False
		if "@" in correo_recibido:
			CV = True


		if(TC == True and NC == False and CV == True): #validamos los datos
			cursor = mysql.connection.cursor()  #almasenamos el objeto de conexion
			#realizamos la consulta y despues la executamos 
			cursor.execute('INSERT INTO contactos (nombre, telefono, correo) VALUES(%s, %s, %s)',(nombre_recibido, telefono_recibido, correo_recibido))
			mysql.connection.commit()
			flash('Contacto agregado correctamente') #sirve para mandar mensajes y mostrarlos en pantalla
			return redirect(url_for('Index'))
		else:
			flash("DATO NO GUARDADO")
			return redirect(url_for('Index'))

#ruta y funcion para editar un contacto
@app.route('/editar_contacto/<id>')
def editar_contacto(id):
	cursor = mysql.connection.cursor()
	cursor.execute('SELECT * FROM contactos WHERE id = {0}'.format(id))
	dato = cursor.fetchall()
	return render_template('editarContacto.html', susdatos = dato[0])


#ruta y funcion para actualizar un contacto
@app.route('/actualizar_contacto/<id>', methods = ['POST'])
def actualiza_contacto(id):
	if request.method == 'POST':
		nombre_recibido = request.form['nombre']
		telefono_recibido = request.form['telefono']
		correo_recibido = request.form['correo']
		TC = telefono_recibido.isdigit()
		NC = nombre_recibido.isspace()
		CV = False
		if "@" in correo_recibido:
			CV = True
			
		if(TC == True and NC == False and CV == True):
			cursor = mysql.connection.cursor()
			cursor.execute("""UPDATE contactos SET nombre = %s, telefono = %s, correo = %s
			 WHERE id = %s""", (nombre_recibido, telefono_recibido, correo_recibido, id))
			mysql.connection.commit()
			flash("Contacto actualizado correctamente")
			return redirect(url_for('Index'))
		else:
			flash("Los datos no fueron actualizados, vuelve a intentar pero esta ves escribelos correctamente")
			return redirect(url_for('Index'))

#ruta y funcion para eliminar un contacto
@app.route('/eliminar_contacto/<string:id>')
def eliminar_contacto(id):
		cursor = mysql.connection.cursor()
		cursor.execute('DELETE FROM contactos WHERE id = {0}'.format(id))
		mysql.connection.commit()
		flash('Contacto eliminado')
		return redirect(url_for('Index'))


#verificamos que estamos en el principal 
if __name__ == '__main__':
	app.run(port = 3000, debug = True)  #debug nos ayuda a actualizar mientras el programa este en execucion
#le asignamos el puerto donde estara nuestra pagina