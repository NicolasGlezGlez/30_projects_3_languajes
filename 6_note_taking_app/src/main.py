from pymongo import MongoClient
import bcrypt
import datetime

# Conexión con MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["note_taking_app"]


# Funciones para Usuarios:
def add_user(username, password):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        "username": username,
        "password": hashed_pw,
    }
    db.usuarios.insert_one(user)

def get_user(username):
    user = db.usuarios.find_one({"username": username})
    return user

def check_password(username, password):
    user = get_user(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        return True
    return False

# Funciones para Notas:

def add_note(user_id, title, content):
    note = {
        "userID": user_id,
        "title": title,
        "content": content,
        "created_at": datetime.datetime.now(),
        "updated_at": datetime.datetime.now(),
        "archived": False
    }
    db.notas.insert_one(note)

def get_notes(user_id):
    return list(db.notas.find({"userID": user_id}))


def test_user_functions():
    # Añadir un usuario
    add_user("testUser", "testPassword")
    
    # Comprobar que el usuario existe y que la contraseña es correcta
    assert get_user("testUser") is not None, "Error: El usuario no fue añadido correctamente."
    assert check_password("testUser", "testPassword"), "Error: La contraseña no es correcta."

def test_note_functions():
    # Usar el usuario creado anteriormente para las pruebas
    user = get_user("testUser")
    user_id = user["_id"]

    # Añadir una nota
    add_note(user_id, "Test Title", "Test Content")
    
    # Comprobar que la nota fue añadida
    notes = get_notes(user_id)
    assert len(notes) > 0, "Error: La nota no fue añadida correctamente."
    assert notes[0]["title"] == "Test Title", "Error: El título de la nota no es correcto."
    assert notes[0]["content"] == "Test Content", "Error: El contenido de la nota no es correcto."

# Ejecutar las funciones de prueba:

test_user_functions()
test_note_functions()

print("¡Todas las pruebas se han ejecutado con éxito!")
