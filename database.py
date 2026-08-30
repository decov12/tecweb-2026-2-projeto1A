import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''
    favorito: bool = False


class Database:
    def __init__(self, nome):
        self.conn = sqlite3.connect(nome + '.db')
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT NOT NULL,
                favorito INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()

    

    def get_all(self):
        cursor = self.conn.execute("SELECT id, title, content, favorito FROM note ORDER BY favorito DESC, id ASC")
        lista=[]
        for linha in cursor:
            lista.append(Note(id=linha[0], title=linha[1], content=linha[2], favorito=bool(linha[3])))
        return lista
    
    def add(self, note):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO note (title, content) VALUES (?, ?)', (note.title, note.content))
        self.conn.commit()

    def update(self, entry):
        cursor = self.conn.cursor()
        cursor.execute('UPDATE note SET title = ?, content = ? WHERE id = ?', (entry.title, entry.content, entry.id))
        self.conn.commit()

    def delete(self, note_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM note WHERE id = ?', (note_id,))
        self.conn.commit()

    def get(self, note_id):
        cursor = self.conn.execute("SELECT id, title, content, favorito FROM note WHERE id = " + str(note_id))
        linha = cursor.fetchone()
        if linha is None:
            return None
        return Note(id=linha[0], title=linha[1], content=linha[2], favorito=bool(linha[3]))

    def toggle_favorito(self, note_id):
        nota = self.get(note_id)
        novo_valor = 0 if nota.favorito else 1
        cursor = self.conn.cursor()
        cursor.execute("UPDATE note SET favorito = ? WHERE id = ?", (novo_valor, note_id))
        self.conn.commit()

