from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId, json_util
from bson.errors import InvalidId
import json

app = Flask(__name__)
CORS(app)
client = MongoClient("mongodb://localhost:27017/")
db = client["note_taking_app"] 
users_collection = db["users"]
notes_collection = db["notes"]



def mongo_to_dict(obj):
    """ Convierte un objeto de MongoDB a un diccionario """
    return json.loads(json_util.dumps(obj))


@app.route('/users/register', methods=['POST'])
def register():
    data = request.get_json()  # obtener datos de la solicitud
    print("Data: ", data)

    # Suponiendo que tienes una función que verifica si el usuario existe:
    if find_user_by_username(data['username']):
        return jsonify({"error": "El usuario ya existe"}), 400

    user_id = save_user(data['username'], data['password'])
    if user_id:
        return jsonify({"success": "Usuario registrado con éxito", "user_id": str(user_id)}), 200
    else:
        return jsonify({"error": "Hubo un problema al registrar al usuario"}), 500


@app.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Datos recibidos:", data)

    user = find_user_by_username(data['username'])

    # Si no se encuentra el usuario o la contraseña es incorrecta
    if user is None or not check_password_hash(user['password'], data['password']):
        return jsonify({"error": "Nombre de usuario o contraseña incorrectos"}), 401

    # Si el inicio de sesión es correcto
    return jsonify({"success": "Inicio de sesión exitoso", "user": user['username']}), 200


@app.route('/users/profile', methods=['GET'])
def profile():
    # Aquí irá la lógica para obtener el perfil del usuario
    pass

@app.route('/users/profile', methods=['PUT'])
def update_profile():
    # Aquí irá la lógica para actualizar el perfil del usuario
    pass

@app.route('/notes/<username>', methods=['GET'])
def get_notes_by_user(username):
    try:
        notes = notes_collection.find({"username": username})
        notes_list = [mongo_to_dict(note) for note in notes]
        return jsonify(notes_list), 200
    except Exception as e:
        return jsonify({"error": f"Error fetching notes: {str(e)}"}), 500

    
@app.route('/notes', methods=['POST'])
def add_note():
    try:
        data = request.get_json()
        title = data['title']
        content = data['content']
        username = data['user_id']
        
        note = {
            "title": title,
            "content": content,
            "username": username,
            "archived": False,
        }
        
        notes_collection.insert_one(note)
        return jsonify({"success": "Nota añadida con éxito"}), 200
    
    except Exception as e:
        return jsonify({"error": f"Error al añadir la nota: {str(e)}"}), 400

@app.route('/notes/search/<username>/<keyword>', methods=['GET'])
def search_notes(username, keyword):
    try:
        if not keyword:
            # Si no hay palabra clave, retorna todas las notas del usuario
            found_notes = notes_collection.find({"username": username})
        else:
            regex = {"$regex": keyword, "$options": "i"}
            found_notes = notes_collection.find({
                "$and": [
                    {"username": username},  # <-- Aquí es donde se restrige la búsqueda al usuario que realiza la solicitud
                    {"$or": [
                        {"title": regex},
                        {"content": regex}
                    ]}
                ]
            })

        notes = list(found_notes)
        for note in notes:
            note['_id'] = str(note['_id'])
            
        return jsonify(notes), 200
    except Exception as e:
        return jsonify({"error": f"Error searching notes: {str(e)}"}), 500


@app.route('/notes/<id>', methods=['PUT'])
def edit_note(id):
    # Validamos si el ID tiene el formato correcto
    if not ObjectId.is_valid(id):
        return jsonify({"error": "ID proporcionado no es válido"}), 400
    
    try:
        data = request.get_json()
        title = data['title']
        content = data['content']

        result = notes_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"title": title, "content": content}}
        )

        if result.modified_count > 0:
            return jsonify({"success": "Nota actualizada con éxito"}), 200
        else:
            return jsonify({"error": "No se pudo actualizar la nota"}), 400

    except InvalidId:
        return jsonify({"error": "El ID proporcionado no es válido para MongoDB"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al editar la nota: {str(e)}"}), 500


@app.route('/notes/<id>', methods=['DELETE'])
def delete_note(id):
    if not ObjectId.is_valid(id):
        return jsonify({"error": "ID proporcionado no es válido"}), 400
    
    try:
        result = notes_collection.delete_one({"_id": ObjectId(id)})

        if result.deleted_count > 0:
            return jsonify({"success": "Nota eliminada con éxito"}), 200
        else:
            return jsonify({"error": "No se pudo eliminar la nota"}), 400

    except Exception as e:
        return jsonify({"error": f"Error al eliminar la nota: {str(e)}"}), 500


@app.route('/notes/<id>/archive', methods=['POST'])
def archive_note(id):
    try:
        result = notes_collection.update_one({"_id": ObjectId(id)}, {"$set": {"archived": True}})

        if result.modified_count > 0:
            return jsonify({"success": "Nota archivada con éxito"}), 200
        else:
            return jsonify({"error": "No se pudo archivar la nota"}), 400

    except Exception as e:
        return jsonify({"error": f"Error al archivar la nota: {str(e)}"}), 500

@app.route('/notes/<id>/unarchive', methods=['POST'])
def unarchive_note(id):
    try:
        result = notes_collection.update_one({"_id": ObjectId(id)}, {"$set": {"archived": False}})

        if result.modified_count > 0:
            return jsonify({"success": "Nota desarchivada con éxito"}), 200
        else:
            return jsonify({"error": "No se pudo desarchivar la nota"}), 400

    except Exception as e:
        return jsonify({"error": f"Error al desarchivar la nota: {str(e)}"}), 500



def find_user_by_username(username):
    # Consulta en MongoDB con clave consistente
    user = db.users.find_one({"username": username})
    return user

def save_user(username, password):
    """
    Guarda un nuevo usuario en la base de datos.

    :param username: Nombre de usuario.
    :param password: Contraseña sin cifrar.
    :return: ID del usuario creado o None si el nombre de usuario ya existe.
    """
    # Primero, verificamos si el nombre de usuario ya existe en la base de datos
    if users_collection.find_one({"username": username}):
        return None

    # Si el nombre de usuario no existe, lo ciframos y lo guardamos
    hashed_password = generate_password_hash(password, method='scrypt')
    user_data = {
        "username": username,
        "password": hashed_password,
    }
    user_id = users_collection.insert_one(user_data).inserted_id
    return user_id


if __name__ == '__main__':
    app.run(debug=True)
