"""Fortnite Tracker API (FastAPI) and local HTML page."""
from contextlib import asynccontextmanager
from pathlib import Path
import sqlite3

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, model_validator

from backend.database import connect, initialize

ROOT = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(application: FastAPI):
    initialize()
    yield


app = FastAPI(title='Fortnite Tracker API', description='Registro escolar de jugadores y estadísticas de Fortnite', lifespan=lifespan)
app.mount('/static', StaticFiles(directory=ROOT / 'public' / 'static'), name='static')


class JugadorEntrada(BaseModel):
    nombre: str = Field(min_length=2, max_length=30)
    plataforma: str
    temporada_id: int = Field(gt=0)
    partidas: int = Field(ge=0, le=1000000)
    victorias: int = Field(ge=0, le=1000000)
    eliminaciones: int = Field(ge=0, le=10000000)

    @model_validator(mode='after')
    def comprobar(self):
        self.nombre = self.nombre.strip()
        if len(self.nombre) < 2:
            raise ValueError('El nombre debe tener mínimo 2 caracteres.')
        if self.plataforma not in ('PC', 'PlayStation', 'Xbox', 'Nintendo Switch', 'Móvil'):
            raise ValueError('Plataforma no válida.')
        if self.victorias > self.partidas:
            raise ValueError('Las victorias no pueden superar las partidas.')
        return self


class TemporadaEntrada(BaseModel):
    nombre: str = Field(min_length=2, max_length=60)
    capitulo: str = Field(min_length=2, max_length=60)


def obtener_jugador(db, identificador: int):
    return db.execute('''SELECT j.*, t.nombre AS temporada, t.capitulo
        FROM jugadores j JOIN temporadas t ON t.id = j.temporada_id WHERE j.id = ?''', (identificador,)).fetchone()


def error_db(exc):
    raise HTTPException(status_code=400, detail='No se pudo guardar: comprueba los datos y sus relaciones.') from exc


@app.get('/', include_in_schema=False)
def inicio():
    return FileResponse(ROOT / 'public' / 'index.html')


@app.get('/api/temporadas')
def listar_temporadas():
    with connect() as db:
        return [dict(f) for f in db.execute('SELECT * FROM temporadas ORDER BY id')]


@app.post('/api/temporadas', status_code=201)
def crear_temporada(datos: TemporadaEntrada):
    with connect() as db:
        try:
            cursor = db.execute('INSERT INTO temporadas(nombre, capitulo) VALUES (?, ?)', (datos.nombre.strip(), datos.capitulo.strip()))
            return dict(db.execute('SELECT * FROM temporadas WHERE id=?', (cursor.lastrowid,)).fetchone())
        except sqlite3.IntegrityError as exc:
            error_db(exc)


@app.delete('/api/temporadas/{identificador}')
def eliminar_temporada(identificador: int):
    with connect() as db:
        try:
            cursor = db.execute('DELETE FROM temporadas WHERE id=?', (identificador,))
        except sqlite3.IntegrityError as exc:
            raise HTTPException(409, 'No se puede eliminar una temporada con jugadores asociados.') from exc
        if not cursor.rowcount:
            raise HTTPException(404, 'Temporada no encontrada.')
        return {'mensaje': 'Temporada eliminada.'}


@app.get('/api/jugadores')
def listar_jugadores(buscar: str = ''):
    with connect() as db:
        filas = db.execute('''SELECT j.*, t.nombre AS temporada, t.capitulo FROM jugadores j
            JOIN temporadas t ON t.id = j.temporada_id WHERE j.nombre LIKE ? ORDER BY j.id DESC''',
            (f'%{buscar}%',)).fetchall()
        return [dict(f) for f in filas]


@app.get('/api/jugadores/{identificador}')
def ver_jugador(identificador: int):
    with connect() as db:
        jugador = obtener_jugador(db, identificador)
        if not jugador:
            raise HTTPException(404, 'Jugador no encontrado.')
        return dict(jugador)


@app.post('/api/jugadores', status_code=201)
def crear_jugador(datos: JugadorEntrada):
    with connect() as db:
        try:
            cursor = db.execute('''INSERT INTO jugadores(nombre, plataforma, temporada_id, partidas, victorias, eliminaciones)
                VALUES (:nombre, :plataforma, :temporada_id, :partidas, :victorias, :eliminaciones)''', datos.model_dump())
            return dict(obtener_jugador(db, cursor.lastrowid))
        except sqlite3.IntegrityError as exc:
            error_db(exc)


@app.put('/api/jugadores/{identificador}')
def actualizar_jugador(identificador: int, datos: JugadorEntrada):
    with connect() as db:
        try:
            cursor = db.execute('''UPDATE jugadores SET nombre=:nombre, plataforma=:plataforma,
                temporada_id=:temporada_id, partidas=:partidas, victorias=:victorias,
                eliminaciones=:eliminaciones WHERE id=:id''', {**datos.model_dump(), 'id': identificador})
            if not cursor.rowcount:
                raise HTTPException(404, 'Jugador no encontrado.')
            return dict(obtener_jugador(db, identificador))
        except sqlite3.IntegrityError as exc:
            error_db(exc)


@app.delete('/api/jugadores/{identificador}')
def eliminar_jugador(identificador: int):
    with connect() as db:
        cursor = db.execute('DELETE FROM jugadores WHERE id=?', (identificador,))
        if not cursor.rowcount:
            raise HTTPException(404, 'Jugador no encontrado.')
        return {'mensaje': 'Jugador eliminado correctamente.'}
