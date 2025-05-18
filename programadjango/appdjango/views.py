import base64
import io
import re
from PIL import Image # type: ignore
from urllib import request
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth.hashers import check_password
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .forms import LoginFormulario, RegistroFormulario
from .models import Animales, Lugar
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
import numpy as np
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import logout

modeloReptiles = load_model(r"C:\Users\Jose\Desktop\TFG\Django\programadjango\appdjango\modelos\modeloReptiles.keras")
clases_modelo_reptiles = ['Culebra', 'Lagarto', 'Rana', 'Tortuga']
modeloDomestico = load_model(r"C:\Users\Jose\Desktop\TFG\Django\programadjango\appdjango\modelos\modeloDomestico.keras")
clases_modelo_domesticos = ['Bisonte', 'Burro', 'Caballo', 'Cabra', 'Cerdo', 'Cisne', 'Conejo', 'Gallina', 'Gato', 'Oveja', 'Pavo', 'Perro', 'Vaca']
modeloAves = load_model(r"C:\Users\Jose\Desktop\TFG\Django\programadjango\appdjango\modelos\modeloAve.keras")
clases_modelo_aves = ['Aguila', 'Buitre', 'Cigüeña', 'Ganso', 'Grulla', 'Halcon', 'Lechuza']
modeloSalvaje = load_model(r"C:\Users\Jose\Desktop\TFG\Django\programadjango\appdjango\modelos\modeloSalvaje.keras")
clases_modelo_salvajes = ['Ardilla', 'Ciervo', 'Jabali', 'Liebre', 'Lince', 'Lobo', 'Marmota', 'Nutria', 'Oso', 'Tejon', 'Zorro']

#vista usada para el login de nuestra pagina web
def vistaLogin(request):
    if request.method == "POST":
        formulario = LoginFormulario(request.POST)
        if formulario.is_valid(): # si el formulario es valido, recogemos los datos en variables
            correo = formulario.cleaned_data['correo']
            contrasena = formulario.cleaned_data['contrasena']

            user = User.objects.filter(email=correo).first()

            if user is None or not check_password(contrasena, user.password):
                messages.error(request, "Credenciales inválidas.")
            else:
                login(request, user)  # Logeamos el usuario
                return redirect('inicio')  # Redirigir a la página de inicio

        else:
            messages.error(request, "Formulario no válido.")
    
    else:
        formulario = LoginFormulario()

    return render(request, "appdjango/login.html", {"form": formulario})

#vista para el registro de nuestra pagina web
def vistaRegistro(request):
    if request.method == "POST":
        formulario = RegistroFormulario(request.POST)
        if formulario.is_valid():
            #cogemos los datos que ha insertado el usuario a la hora de registrarse y lo guardamos en variables
            nombre = formulario.cleaned_data['nombre']
            correo = formulario.cleaned_data['correo']
            contrasena = formulario.cleaned_data['contrasena']
            
            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', contrasena): #verificamos si la contraseña cumple con los requisitos
                formulario.add_error('contrasena', 'La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número.')
                return render(request, "appdjango/registro.html", {"form": formulario})
            else:    
                if User.objects.filter(email=correo).exists(): #verificamos que el correo no esté registrado ya en la base de datos
                    formulario.add_error('correo', 'Este correo ya está registrado.')
                    return render(request, "appdjango/registro.html", {"form": formulario})
                else:
                    if User.objects.filter(username=nombre).exists(): #verificamos que el nombre no esté registrado ya en la base de datos
                        formulario.add_error('nombre', 'Este nombre ya está registrado.')
                        return render(request, "appdjango/registro.html", {"form": formulario})
                    else:
                        #si el usuario no existe, encriptamos la contraseña y creamos un nuevo usuario insertandolo en la base de datos
                        contrasena_encriptada = make_password(contrasena)
                        nuevo_usuario = User(username=nombre, email = correo, password = contrasena_encriptada)
                        nuevo_usuario.save()
                        #una vez insertado, mandamos al usuario a logearse
                        return redirect('login')
            
    else: 
        formulario = RegistroFormulario()
    return render(request, "appdjango/registro.html", {"form": formulario})

#vista para la pagina de inicio (despues del login)
def vistaInicio(request):
    return render(request, 'appdjango/inicio.html')


 #vista para el historial de reconocimientos de animales
def vistaReconocimientos(request):
    user = request.user

    # Obtener todos los animales almacenados en la base de datos 
    animales = Animales.objects.filter(usuario = user)

    return render(request, 'appdjango/reconocimiento.html', {'animales': animales})

#vista para los ajustes de la pagina web
def vistaAjustes(request):
    return render(request, 'appdjango/ajustes.html', {'usuario': request.user, 'email': request.user.email, 'contrasena': request.user.password} )

#funcion para eliminar la cuenta del usuario que ha iniciado sesion
def eliminarCuenta(request): 
    if request.user.is_authenticated:  # Verifica si el usuario está autenticado
        user = request.user
        user.delete()  # Elimina el usuario de la base de datos
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error", "message": "No estás autenticado"})
    
#funcion para cambiar la contraseña del usuario que ha iniciado sesion
def cambiar_contrasena(request):
    if request.method == "POST":
        data = json.loads(request.body)
        actual = data.get("actual") #obtenemos el valor de la contraseña actual y la nueva
        nueva = data.get("nueva")

        usuario = request.user
        if not usuario.check_password(actual): #comprobamos que la contraseña actual sea correcta
            return JsonResponse({"success": False, "error": "La contraseña actual es incorrecta"}, status=400)

        usuario.set_password(nueva) #introducimos la contraseña nueva al usuario
        usuario.save() # guardamos los cambios
        update_session_auth_hash(request, usuario)  # Evita que el usuario cierre sesión

        return JsonResponse({"success": True})

    return JsonResponse({"success": False, "error": "Método no permitido"}, status=405)

def deteccion_resultado(request):
    if request.method == 'POST':
        if 'archivo' in request.FILES:
            imagen = Image.open(request.FILES['archivo'])
        elif request.POST.get('fotobase64'):
            base64_str = request.POST.get('fotobase64').split(',')[1]
            image_data = base64.b64decode(base64_str)
            imagen = Image.open(io.BytesIO(image_data))
        else:
            return render(request, 'appdjango/resultado.html', {'error':'No se recibió ninguna imagen'})

        # Preprocesamiento
        imagen = imagen.resize((128, 128))
        imagen_array = img_to_array(imagen) / 128.0
        imagen_array = np.expand_dims(imagen_array, axis=0)

        # Evaluar modelo de reptiles
        pred_reptil = modeloReptiles.predict(imagen_array)
        prob_reptil = np.max(pred_reptil)
        clase_reptil = clases_modelo_reptiles[np.argmax(pred_reptil)]

        if prob_reptil >= 0.6:
            return render(request, 'appdjango/resultado.html', {
                'clase': clase_reptil,
                'probabilidad': round(prob_reptil * 100, 2)
            })

        # Evaluar modelo doméstico
        pred_domestico = modeloDomestico.predict(imagen_array)
        prob_domestico = np.max(pred_domestico)
        clase_domestico = clases_modelo_domesticos[np.argmax(pred_domestico)]

        if prob_domestico >= 0.6:
            return render(request, 'appdjango/resultado.html', {
                'clase': clase_domestico,
                'probabilidad': round(prob_domestico * 100, 2)
            })

        # Evaluar modelo aves
        pred_aves = modeloAves.predict(imagen_array)
        prob_aves = np.max(pred_aves)
        clase_ave = clases_modelo_aves[np.argmax(pred_aves)]

        if prob_aves >= 0.6:
            return render(request, 'appdjango/resultado.html', {
                'clase': clase_ave,
                'probabilidad': round(prob_aves * 100, 2)
            })

       # Evaluar modelo salvajes
        pred_salvajes = modeloSalvaje.predict(imagen_array)
        prob_salvaje = np.max(pred_salvajes)
        clase_salvaje = clases_modelo_salvajes[np.argmax(pred_salvajes)]

        if prob_salvaje >= 0.6:
            return render(request, 'appdjango/resultado.html', {
                'clase': clase_salvaje,
                'probabilidad': round(prob_salvaje * 100, 2)
            })
            
    return render(request, 'appdjango/resultado.html', {'error': 'Método no válido'})

def obtener_coordenadas_exif(archivo_imagen):
    # Abrir la imagen para leer los datos EXIF
    imagen = Image.open(archivo_imagen)
    # Cogemos los metadatos EXIF
    exif_data = imagen._getexif()
    # Si existen metadatos EXIF
    if exif_data:
        # Obtenemos la coordenada GPS
        for tag, value in exif_data.items():
            # Encontrar la latitud y longitud en los metadatos EXIF (corresponde con la etiqueta 34853)
            if tag == 34853:  
                lat = value[2][0] / value[2][1]  # Grados latitud (2)
                lon = value[4][0] / value[4][1]  # Grados longitud (4)
                return lat, lon
    return None, None  # Si no se encuentra información EXIF, devolvemos nulo

def guardar_animal_BBDD(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                clase = data.get('clase')
                probabilidad = data.get('probabilidad')
                latitud = data.get('latitud')
                longitud = data.get('longitud')
            except json.JSONDecodeError:
                return JsonResponse({'success': False, 'error': 'Error en el formato JSON'}, status=400)
        else:
            clase = request.POST.get('clase')
            probabilidad = request.POST.get('probabilidad')
            latitud = request.POST.get('latitud')
            longitud = request.POST.get('longitud')

        if not latitud or not longitud:
            return JsonResponse({'success': False, 'error': 'Coordenadas faltantes'}, status=400)

        # Consulta si ya existe un lugar con las mismas coordenadas
        lugar_existente = Lugar.objects.filter(latitud=float(latitud), longitud=float(longitud)).first()

        if lugar_existente:
            lugar = lugar_existente  # Si existe, lo reutilizamos
        else:
            lugar = Lugar(latitud=float(latitud), longitud=float(longitud))  # Si no existe, lo creamos
            lugar.save()

        animal = Animales(usuario=request.user, nombreAnimal=clase, cantidad=1, lugarEncuentro=lugar)
        animal.save()

        return redirect('reconocimientos')

    return JsonResponse({'success': False, 'error': 'Método no válido'}, status=405)

def recuperar_contrasena(request):
    if request.method == 'POST':
        email = request.POST.get('email_recuperacion')
        
        asunto = 'Recuperación de contraseña'
        # Mensaje en texto plano (para clientes que no soportan HTML)
        mensaje = 'Haz clic en el siguiente enlace para cambiar tu contraseña:\n\n'
        mensaje += 'http://127.0.0.1:8000/cambio_contrasena/'

        # Mensaje en formato HTML
        mensaje_html = '''
            <html>
                <body>
                    <p>Haz clic en el siguiente enlace para cambiar tu contraseña:</p>
                    <a href="http://127.0.0.1:8000/cambio_contrasena/">Pincha aquí para cambiar tu contraseña</a>
                </body>
            </html>
        '''
        
        try:
            send_mail(
                asunto,
                mensaje,  # Mensaje en texto plano
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=mensaje_html  # Enviar el mensaje como HTML
            )
            request.session['email_usuario'] = email
            request.session.modified = True
            messages.success(request, 'Se ha enviado un enlace a tu correo.')
        except Exception as e:
            messages.error(request, f'Error al enviar el correo: {str(e)}')

        return redirect('login')  # Redirigir al login 

    return redirect('login')

def cambio_contrasena(request):
    return render(request, 'appdjango/cambioContraseña.html')

def reestablecer_contrasena(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email') or request.GET.get('email') or request.session.get('email_usuario')

        if not email:
            messages.error(request, 'No se encontró el correo del usuario.')
            return redirect('recuperar_contrasena')

        if password1 != password2:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('reestablecer_contrasena')
        
        if len(password1) < 8:
            messages.error(request, 'La contraseña debe tener al menos 8 caracteres.')
            return redirect('reestablecer_contrasena')

        if not re.search(r'[A-Z]', password1):
            messages.error(request, 'La contraseña debe contener al menos una letra mayúscula.')
            return redirect('reestablecer_contrasena')

        if not re.search(r'[a-z]', password1):
            messages.error(request, 'La contraseña debe contener al menos una letra minúscula.')
            return redirect('reestablecer_contrasena')

        if not re.search(r'\d', password1):
            messages.error(request, 'La contraseña debe contener al menos un número.')
            return redirect('reestablecer_contrasena')

        try:
            usuario = User.objects.get(email=email)
            usuario.set_password(password1)
            usuario.save()
            logout(request)
            messages.success(request, 'Contraseña actualizada correctamente.')
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return redirect('recuperar_contrasena')

    email = request.GET.get('email') or request.session.get('email_usuario')
    return render(request, 'appdjango/cambioContraseña.html', {'email': email})




