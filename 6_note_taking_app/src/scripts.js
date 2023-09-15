function login() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Crear el objeto con las credenciales
    var credentials = {
        username: username,
        password: password
    };

    console.log("Credentials: ", credentials)

    // Hacer una petición POST al endpoint de login
    fetch('http://localhost:5000/users/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            // Si el login es exitoso, oculta el formulario de login y muestra el formulario de nota
            document.getElementById('loginForm').style.display = 'none';
            document.getElementById('notaForm').style.display = 'block';
            document.getElementById('searchForm').style.display = 'block';
            document.getElementById('logoutButton').style.display = 'block';
            
            localStorage.setItem('loggedInUser', username);
            var userToShow = document.getElementById('userToShow');
            userToShow.textContent = "Bienvenido usuario: " + username;
            fetchUserNotes(username);
        } else {
            // Si hay un error, muestra un mensaje
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ha ocurrido un error. Inténtalo de nuevo.');
    });
}

function register() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // Crear el objeto con las credenciales
    var credentials = {
        username: username,
        password: password
    };

    // Hacer una petición POST al endpoint de login
    fetch('http://localhost:5000/users/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            loggedUserId = data.user_id;
            alert("Usuario registrado con éxito");
            username = document.getElementById('username').value = '';
            password = document.getElementById('password').value = '';
        } else {
            // Si hay un error, muestra un mensaje
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Ha ocurrido un error. Inténtalo de nuevo.');
    });
}

function agregarNota() {
    var titulo = document.getElementById('tituloNota').value;
    var contenido = document.getElementById('contenidoNota').value;
    var username = localStorage.getItem('loggedInUser');

    if(titulo && contenido) {
        var listaNotas = document.getElementById('listaNotas');
        var notaDiv = document.createElement('div');
        notaDiv.className = 'nota';

        var notaTitulo = document.createElement('h2');
        notaTitulo.textContent = titulo;
        notaDiv.appendChild(notaTitulo);

        var notaContenido = document.createElement('p');
        notaContenido.textContent = contenido;
        notaDiv.appendChild(notaContenido);

        listaNotas.appendChild(notaDiv);

        const noteData = {
            title: titulo,
            content: contenido,
            user_id: username
        };
        console.log("Notes: ", noteData)

        fetch('http://localhost:5000/notes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(noteData) 
        })  
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                console.log("Success: ", data);
                loggedUserId = data.user_id; // Guardamos el ID del usuario
                // Otras acciones que quieras realizar luego del registro exitoso
            } else {
                console.error(data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });

        // Limpiar campos
        document.getElementById('tituloNota').value = '';
        document.getElementById('contenidoNota').value = '';
    } else {
        alert('Por favor, rellena todos los campos.');
    }
}

function fetchUserNotes(username) {
    fetch('http://localhost:5000/notes/' + username)
    .then(response => response.json())
    .then(notes => {
        // Aquí, "notes" es una lista de todas las notas del usuario
        // Debes agregar la lógica para mostrar estas notas en tu frontend
        console.log("Notes: ", notes);
        displayUserNotes(notes);
    })
    .catch(error => {
        console.error('Error fetching notes:', error);
    });
}

function displayUserNotes(notes) {
    const notesList = document.getElementById('listaNotas');
    notesList.innerHTML = '';  // Limpiamos cualquier nota anterior

    notes.forEach(note => {
        const noteDiv = document.createElement('div');
        noteDiv.className = 'note-item'; 

        const noteTitle = document.createElement('h2');
        noteTitle.textContent = note.title;
        noteDiv.appendChild(noteTitle);

        const noteContent = document.createElement('p');
        noteContent.textContent = note.content;
        noteDiv.appendChild(noteContent);

        // Añadimos un botón de edición
        const editButton = document.createElement('button');
        editButton.textContent = 'Editar';
        editButton.onclick = () => showEditForm(note._id.$oid, note.title, note.content);
        noteDiv.appendChild(editButton);
        
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Eliminar';
        deleteButton.onclick = () => deleteNoteById(note._id.$oid);
        noteDiv.appendChild(deleteButton);

        const archiveButton = document.createElement('button');
        // Suponiendo que tienes un campo 'archived' en tu objeto de nota
        if(note.archived) {
            archiveButton.textContent = 'Desarchivar';
        } else {
            archiveButton.textContent = 'Archivar';
        }

        archiveButton.onclick = () => toggleArchive(note._id.$oid, note.archived);
        noteDiv.appendChild(archiveButton);

        notesList.appendChild(noteDiv);
    });
}

function toggleArchive(noteId, currentlyArchived) {
    if (currentlyArchived) {
        unarchiveNoteById(noteId);
    } else {
        archiveNoteById(noteId);
    }
}

function searchNotes() {
    const username = localStorage.getItem('loggedInUser');
    const keyword = document.getElementById('searchKeyword').value;

    if (keyword.trim() === '') {
        // Si el campo de búsqueda está vacío, obtiene las notas del usuario.
        fetchUserNotes(username);
    } else {
        console.log("Keyword: ", keyword);
        fetch(`http://localhost:5000/notes/search/${username}/${keyword}`)
        .then(response => response.json())
        .then(data => {
            // Aquí, muestra las notas que coincidan con la búsqueda en la sección listaNotas.
            // Puedes usar la misma lógica que usaste para mostrar las notas del usuario, pero con los resultados de esta búsqueda.
            console.log(data)
            displayUserNotes(data);
        })
        .catch(error => {
            console.error('Error searching notes:', error);
            alert('Error buscando notas. Inténtalo de nuevo.');
        });
    }
}

function editarNota() {
    const noteId = document.getElementById('editNoteId').value;

    const newTitle = document.getElementById('editTituloNota').value;
    const newContent = document.getElementById('editContenidoNota').value;

    fetch(`http://localhost:5000/notes/${noteId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            title: newTitle,
            content: newContent
        })
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            // Refrescar las notas o hacer lo que quieras aquí
            alert(data.success);
            const username = localStorage.getItem('loggedInUser');
            fetchUserNotes(username); // Refresca las notas después de editar
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error editando la nota:', error);
        alert('Error editando la nota. Inténtalo de nuevo.');
    });
}

function showEditForm(noteId, currentTitle, currentContent) {
    document.getElementById('editNotaForm').style.display = 'block';
    document.getElementById('editNoteId').value = noteId;
    document.getElementById('editTituloNota').value = currentTitle;
    document.getElementById('editContenidoNota').value = currentContent;
}

function deleteNoteById(noteId) {
    document.getElementById('editNoteId').value = noteId;

    fetch(`http://localhost:5000/notes/${noteId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            // Refrescar las notas o hacer lo que quieras aquí
            alert(data.success);
            const username = localStorage.getItem('loggedInUser');
            fetchUserNotes(username); // Refresca las notas después de editar
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error eliminando la nota:', error);
        alert('Error eliminando la nota. Inténtalo de nuevo.');
    });
}

function archiveNoteById(noteId) {
    fetch(`http://localhost:5000/notes/${noteId}/archive`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        if(data.success) {
            alert(data.success);

            // Encuentra el botón correspondiente y actualízalo
            const noteDiv = document.querySelector(`.note[data-noteid="${noteId}"]`);
            const archiveBtn = noteDiv.querySelector('button');
            archiveBtn.textContent = 'Desarchivar';
        } else {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error archivando la nota:', error);
        alert('Error archivando la nota. Inténtalo de nuevo.');
    });
}

function unarchiveNoteById(noteId) {
    // Lógica similar a la función anterior pero llamando al endpoint de desarchivar
}

function logout() {
    // Elimina el nombre de usuario del localStorage
    localStorage.removeItem("loggedInUser");

    // Oculta las secciones que no deben ser visibles después de cerrar sesión
    document.getElementById("userToShow").style.display = "none";
    document.getElementById("searchForm").style.display = "none";
    document.getElementById("notaForm").style.display = "none";
    document.getElementById("editNotaForm").style.display = "none";
    document.getElementById("listaNotas").innerHTML = ''; // Limpia las notas

    // Muestra el formulario de inicio de sesión
    document.getElementById("loginForm").style.display = "block";

    window.location.reload();
}

