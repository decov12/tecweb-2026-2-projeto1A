import socket
from pathlib import Path
from utils import extract_route, read_file, build_response, load_template
from views import index, excluir_nota, confirmar_exclusao, editar_nota, salvar_edicao, favoritar_nota
CUR_DIR = Path(__file__).parent
SERVER_HOST = 'localhost'
SERVER_PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen()

print(f'Servidor escutando em (ctrl+click): http://{SERVER_HOST}:{SERVER_PORT}')

while True:
    client_connection, client_address = server_socket.accept()

    request = client_connection.recv(1024).decode()
    print('*'*100)
    print(request)

    route = extract_route(request)

    filepath = CUR_DIR / route
    if filepath.is_file():
        response = build_response() + read_file(filepath)
    elif route == '':
        response = index(request)
    elif route.endswith('/confirmar') and route.startswith('delete/'):
        note_id = int(route.split('/')[1])
        response = excluir_nota(note_id)

    elif route.startswith('delete/'):
        note_id = int(route.split('/')[1]) 
        response = confirmar_exclusao(note_id)

    elif route.startswith('edit/'):
        note_id = int(route.split('/')[1])
        if request.startswith('POST'):
            response = salvar_edicao(note_id, request)
        else:
            response = editar_nota(note_id)

    elif route.startswith('favoritar/'):
        note_id = int(route.split('/')[1])
        response = favoritar_nota(note_id)

    else:
        body = load_template('404.html')
        response = build_response(body=body, code=404, reason='Not Found')

    client_connection.sendall(response)
    client_connection.close()
server_socket.close()