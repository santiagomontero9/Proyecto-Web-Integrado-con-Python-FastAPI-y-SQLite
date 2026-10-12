"""SQLite connection and first-run setup for Fortnite Tracker."""
import os
import shutil
import sqlite3
from contextlib import contextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED_DB = ROOT / 'fortnite.db'


def database_path() -> Path:
    configured = os.getenv('DATABASE_PATH')
    if configured:
        return Path(configured)
    if os.getenv('VERCEL'):
        return Path('/tmp/fortnite-tracker.db')
    return SEED_DB


@contextmanager
def connect():
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.getenv('VERCEL') and not path.exists() and SEED_DB.exists():
        shutil.copy2(SEED_DB, path)
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize():
    with connect() as db:
        db.executescript('''
        CREATE TABLE IF NOT EXISTS temporadas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            capitulo TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS jugadores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL CHECK(length(trim(nombre)) BETWEEN 2 AND 30),
            plataforma TEXT NOT NULL CHECK(plataforma IN ('PC','PlayStation','Xbox','Nintendo Switch','Móvil')),
            temporada_id INTEGER NOT NULL,
            partidas INTEGER NOT NULL DEFAULT 0 CHECK(partidas >= 0),
            victorias INTEGER NOT NULL DEFAULT 0 CHECK(victorias >= 0 AND victorias <= partidas),
            eliminaciones INTEGER NOT NULL DEFAULT 0 CHECK(eliminaciones >= 0),
            FOREIGN KEY (temporada_id) REFERENCES temporadas(id) ON DELETE RESTRICT
        );
        ''')
        if db.execute('SELECT COUNT(*) FROM temporadas').fetchone()[0] == 0:
            db.executemany('INSERT INTO temporadas(nombre, capitulo) VALUES (?, ?)', [
                ('Temporada de ejemplo A', 'Capítulo de ejemplo 1'),
                ('Temporada de ejemplo B', 'Capítulo de ejemplo 2'),
            ])
        if db.execute('SELECT COUNT(*) FROM jugadores').fetchone()[0] == 0:
            db.executemany('''INSERT INTO jugadores(nombre, plataforma, temporada_id, partidas, victorias, eliminaciones)
                VALUES (?, ?, ?, ?, ?, ?)''', [
                ('JugadorAlpha', 'PC', 1, 40, 8, 115),
                ('VictoryFox', 'PlayStation', 1, 30, 5, 81),
                ('StormRider', 'Xbox', 2, 18, 3, 42),
            ])
