import flet as ft
from werkzeug.security import generate_password_hash, check_password_hash
from mongodb import save_user, find_user_by_email, authenticate_user
import jwt
import requests
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"  # Debes mantener esta clave en secreto y no exponerla
CURRENT_USER_TOKEN = None
tweets_list = None  # Declaración global


def create_jwt(data: dict):
    expiration = datetime.utcnow() + timedelta(hours=24)
    token = jwt.encode({"exp": expiration, **data}, SECRET_KEY, algorithm="HS256")
    return token


def main(page: ft.Page):
    page.title = "Routes Example"

    # Definir los campos de texto fuera de la función de callback
    login_username_field = ft.TextField(label="Usuario/Correo")
    login_password_field = ft.TextField(label="Contraseña", password=True)
    register_username_field = ft.TextField(label="Usuario")
    register_password_field = ft.TextField(label="Contraseña", password=True)
    register_repeat_password_field = ft.TextField(label="Repetir contraseña", password=True)
    register_email_field = ft.TextField(label="Correo electrónico")
    global tweets_list

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            # Icono o imagen
            app_icon = ft.Image(src="src/images/733635.png", width=100, height=100)

            # Descripción breve
            app_description = ft.Text(
                "Bienvenido a nuestra aplicación de Twitter. Aquí puedes compartir tus pensamientos y conectarte con otros.")

            # Menú (opcional, si tienes más opciones en el futuro)
            menu = ft.Row([
                ft.Text("Inicio"),
                # ft.Text("Otras opciones..."),
            ])

            # Botones de Login y Registro
            login_button = ft.ElevatedButton("Login", on_click=lambda _: page.go("/login"))
            register_button = ft.ElevatedButton("Registro", on_click=lambda _: page.go("/registre"))

            # Añadir todos los elementos a la vista
            home_view = ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    app_icon,
                    app_description,
                    menu,
                    ft.Row([login_button, register_button], spacing=20)  # Espaciado entre botones
                ]
            )
            page.views.append(home_view)
            page.update()

        # page.views.append(
        #     ft.View(
        #         "/",
        #         [
        #             ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
        #             ft.ElevatedButton("Login", on_click=lambda _: page.go("/login")),
        #             ft.ElevatedButton("Registro", on_click=lambda _: page.go("/registre")),
        #         ],
        #     )
        # )
        if page.route == "/login":
            page.views.append(
                ft.View(
                    "/login",
                    [
                        ft.AppBar(title=ft.Text("Login"), bgcolor=ft.colors.SURFACE_VARIANT),
                        login_username_field,
                        login_password_field,
                        ft.ElevatedButton("Entrar", on_click=lambda _: login(page, login_username_field.value,
                                                                             login_password_field.value)),
                    ],
                )
            )
        elif page.route == "/registre":
            page.views.append(
                ft.View(
                    "/registre",
                    [
                        ft.AppBar(title=ft.Text("Registro"), bgcolor=ft.colors.SURFACE_VARIANT),
                        register_username_field,
                        register_password_field,
                        register_repeat_password_field,
                        register_email_field,
                        ft.ElevatedButton("Registrarse", on_click=lambda _: register(page, register_username_field,
                                                                                     register_password_field,
                                                                                     register_repeat_password_field,
                                                                                     register_email_field)),
                    ],
                )
            )
        elif page.route == "/main":
            # Obtener tweets
            response = requests.get("http://localhost:8000/get_tweets/")
            try:
                tweets = response.json()
            except requests.exceptions.JSONDecodeError:
                print("Error decoding JSON from response.")
                tweets = []
            if tweets and isinstance(tweets, list):
                tweet_texts = [ft.Text(tweet["content"]) for tweet in tweets]
            else:
                tweet_texts = [ft.Text("No hay tweets disponibles.")]
            initialize_tweets_list()
            # Crear un campo de texto para escribir el tweet
            tweet_field = ft.TextField(label="Escribe tu tweet")

            # Crear un botón para publicar el tweet
            post_button = ft.ElevatedButton("Publicar", on_click=lambda _: post_tweet(tweet_field.value))

            # Crear una columna con los tweets como controles
            tweets_list = ft.Column(controls=tweet_texts)

            def spacing_slider_change(e):
                tweets_list.spacing = int(e.control.value)
                tweets_list.update()

            gap_slider = ft.Slider(
                min=0,
                max=100,
                divisions=10,
                value=0,
                label="{value}",
                width=500,
                on_change=spacing_slider_change,
            )

            # Añadir todos los elementos a la vista
            page.views.append(
                ft.View(
                    "/main",
                    [
                        ft.AppBar(title=ft.Text("TL"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.Column([ft.Text("Spacing between items"), gap_slider]),
                        tweets_list,
                        tweet_field,
                        post_button
                    ]
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


def post_tweet(content):
    if not CURRENT_USER_TOKEN:
        print("Error: No hay token disponible.")
        return
    print("Content: ", content)
    headers = {"Authorization": f"Bearer {CURRENT_USER_TOKEN}"}
    print("headers: ", headers)
    url = "http://localhost:8000/post_tweet/"
    response = requests.post(url, json={"content": content}, headers=headers)

    if response.status_code == 200:
        print("Tweet publicado con éxito.")
    else:
        print(f"Error al publicar el tweet. Código de estado: {response.status_code}. Mensaje: {response.text}")


def decode_jwt(token: str):
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return data
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token")
        return None


def login(page, username, password):
    global CURRENT_USER_TOKEN  # Indica que deseas usar la variable global
    user = authenticate_user(username, password)
    if user:
        CURRENT_USER_TOKEN = create_jwt({"_id": str(user["_id"])})
        page.go("/main")  # Cambia la ruta a "/main" después de un inicio de sesión exitoso
    else:
        print("Correo electrónico o contraseña incorrectos.")


def initialize_tweets_list():
    global tweets_list
    response = requests.get("http://localhost:8000/get_tweets/")
    try:
        tweets = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error decoding JSON from response.")
        tweets = []
    if tweets and isinstance(tweets, list):
        tweet_texts = [ft.Text(tweet["content"]) for tweet in tweets]
    else:
        tweet_texts = [ft.Text("No hay tweets disponibles.")]
    tweets_list = ft.Column(controls=tweet_texts)


def register(page, username_field, password_field, repeat_password_field, email_field):
    username = username_field.value
    password = password_field.value
    repeat_password = repeat_password_field.value
    email = email_field.value

    if find_user_by_email(email):
        print("El usuario ya existe")
        return
    else:
        print("El usuario no existe")
        pwd_verified = password == repeat_password

        if pwd_verified:
            hashed_password = generate_password_hash(password, method='scrypt')
            user_data = {
                "username": username,
                "email": email,
                "password": hashed_password,
            }
            print(save_user(user_data))

            username_field.value = ""
            password_field.value = ""
            repeat_password_field.value = ""
            email_field.value = ""

            # Redirigir al usuario al apartado de inicio de sesión
            page.go("/login")
        else:
            print("Las contraseñas no coinciden")
            return


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
