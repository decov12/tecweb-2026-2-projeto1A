import sqlite3
from dataclasses import dataclass

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''


class Database:
    def __init__(self, nome):
        self.conn = sqlite3.connect(nome + '.db')
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS note (
                id INTEGER PRIMARY KEY,
                title TEXT,
                content TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add(self, note):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO note (title,content) VALUES (''' + "'" + str(note.title) + "'" + ',' + "'" + str(note.content) + "'" + ');' )
        self.conn.commit()

    def get_all(self):
        cursor = self.conn.execute("SELECT id, title, content FROM note")
        lista=[]
        for linha in cursor:
            id = linha[0]
            title = linha[1]
            content = linha[2]
            lista.append(Note(id=id,title=title, content=content))
        return lista
    
    def update(self, entry):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE note SET title = ''' + "'" + str(entry.title) + "', content = '" + str(entry.content) + "'" + ' WHERE id = ' + str(entry.id)
            )
        self.conn.commit()

    def delete(self,note_id):
        cursor = self.conn.cursor()
        cursor.execute('''DELETE FROM note WHERE id = ' ''' + str(note_id)+"'"
            )
        self.conn.commit()


