from urllib.parse import unquote_plus
from utils import load_data, save_note, load_template, build_response

NOTE_TEMPLATE = load_template('components/note.html')


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
        save_note(params['titulo'], params['detalhes'])

        # Redireciona para a mesma página com uma nova requisição GET
        return build_response(code=303, reason='See Other', headers='Location: /')

    # Cria uma lista de <li>'s para cada anotação
    notes_li = []
    for dados in load_data('notes.json'):
        notes_li.append(NOTE_TEMPLATE.format(title=dados['titulo'], details=dados['detalhes']))

    notes = '\n'.join(notes_li)

    body = load_template('index.html').format(notes=notes)
    response = build_response(body=body)
    return response