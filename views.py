from urllib.parse import unquote_plus
from utils import  load_template, build_response
from database import Database, Note

NOTE_TEMPLATE = load_template('components/note.html')
db = Database('notes')

def index(request):
    if request.startswith('POST'):
        request = request.replace('\r', '')
        partes = request.split('\n\n')
        corpo = partes[1]
        params = {}
        for chave_valor in corpo.split('&'):
            if not chave_valor:
                continue
            chave, valor = chave_valor.split('=', 1)
            params[unquote_plus(chave)] = unquote_plus(valor)

        # Adiciona a nova anotação ao arquivo notes.json
        db.add(Note(title=params['titulo'], content=params['detalhes'])) 

        # Redireciona para a mesma página com uma nova requisição GET
        return build_response(code=303, reason='See Other', headers='Location: /')

    # Cria uma lista de <li>'s para cada anotação
    notes_li = []
    for nota in db.get_all():
        notes_li.append(NOTE_TEMPLATE.format(id=nota.id, title=nota.title, details=nota.content))

    notes = '\n'.join(notes_li)

    body = load_template('index.html').format(notes=notes)
    response = build_response(body=body)
    return response

def confirmar_exclusao(note_id):
    nota = None
    for n in db.get_all():
        if n.id == note_id:
            nota = n
            break

    body = load_template('confirmar_exclusao.html').format(
        id=nota.id, title=nota.title, content=nota.content
    )
    return build_response(body=body)

def excluir_nota(note_id):
    db.delete(note_id)
    return build_response(code=303, reason='See Other', headers='Location: /')

def editar_nota(note_id):
    nota = db.get(note_id)
    body = load_template('editar_nota.html').format(
        id=nota.id, title=nota.title, content=nota.content
    )
    return build_response(body=body)


def salvar_edicao(note_id, request):
    request = request.replace('\r', '')
    partes = request.split('\n\n')
    corpo = partes[1]
    params = {}
    for chave_valor in corpo.split('&'):
        if not chave_valor:
            continue
        chave, valor = chave_valor.split('=', 1)
        params[unquote_plus(chave)] = unquote_plus(valor)

    db.update(Note(id=note_id, title=params['titulo'], content=params['detalhes']))

    return build_response(code=303, reason='See Other', headers='Location: /')