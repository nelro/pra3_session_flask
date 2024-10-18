from flask import Flask, jsonify, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'nelro_123'

# Lista para almacenar a los usuarios registrados (nombre de usuario y contraseña)
# solo lo almacenaremos en una  lista para fines de ejemplo tener encuenta jejejej
usuarios = []  

@app.route('/')
def index():
    return redirect(url_for('iniciar_sesion'))

#  Ruta para la página de inicio de sesión para poder dirigirnios
@app.route('/iniciar_sesion', methods=['GET', 'POST'])
def iniciar_sesion():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contrasena = request.form['contrasena']
        
        # Verificaremos si el usuario existe enl a lista de usuarios registrados
        for usuario in usuarios:
            if usuario['nombre_usuario'] == nombre_usuario and usuario['contrasena'] == contrasena:
                session['nombre_usuario'] = nombre_usuario

                #cuando todo se cumple se retorna un valor(erro si ponemos a retornar un html
                # ya que estamos usando una alerta para envair mensaje)
                return jsonify({'status': 'success', 'message': 'Usuario autenticado correctamente.'})
        #enviamos un mensaje  de error caundo no hay el suaurio
        return jsonify({'status': 'error', 'message': 'usuario o contraseña son incorrectas, intenta nuevamente.'})
    return render_template('iniciar_sesion.html')

#registraremso el  usuario 
@app.route('/registrarse', methods=['GET', 'POST'])
def registrarse():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contrasena = request.form['contrasena']
        
        # Guardar el usuario en la lista
        usuarios.append({'nombre_usuario': nombre_usuario, 'contrasena': contrasena})
        # tener cuidado com usamos  el return json para enviar un mensaje de exito
        # como estamos usando Sweet Alert 2 es  muy complicado encontrar el error tener cuidado
        return jsonify({'status': 'success', 'message': 'Usuario registrado exitosamente. Ahora puedes iniciar sesión.'})
   
    return render_template('registrarse.html')

# ruata para abrir la pagina donde esta la bienvenuida
@app.route('/bienvenida')
def bienvenida():
    if 'nombre_usuario' in session:
        return render_template('bienvenida.html', nombre_usuario=session['nombre_usuario'])
    return redirect(url_for('iniciar_sesion'))

#con esto enlazamos al boton de cerar  sesion para terminar la sesion
@app.route('/cerrar_sesion')
def cerrar_sesion():
    #aquei  se elimina la sesion es decir eliminamos el nombre del usuario 
    session.pop('nombre_usuario', None)
    return redirect(url_for('iniciar_sesion'))

if __name__ == '__main__':
    app.run(debug=True)
