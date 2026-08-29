from pathlib import Path


def extract_route(http):
    resposta=''
    primeiro_t = http.find(' ')
    http = http[primeiro_t:]
    for c in http:
        if c != "H":
            resposta+=c
        else:
            break

    resposta=resposta.replace('/',"",1)
    resposta=resposta.strip()

    return resposta

def read_file(path: Path) -> bytes:
    with open(path,'rb') as f:
        conteudo=f.read()
    return conteudo

def load_template(filename):
    with open(f'templates/{filename}', 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def build_response(body='', code=200, reason='OK', headers=''):
    status_line = f'HTTP/1.1 {code} {reason}'
    if headers:
        response = f'{status_line}\n{headers}\n\n{body}'
    else:
        response = f'{status_line}\n\n{body}'
    return response.encode()