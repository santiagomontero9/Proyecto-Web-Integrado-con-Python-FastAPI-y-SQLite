"""Execute: python -m unittest discover -s tests -v"""
import os
import tempfile
import unittest
from fastapi.testclient import TestClient


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        os.environ['DATABASE_PATH'] = os.path.join(self.temp.name, 'test.db')
        from app import app
        self.client_context = TestClient(app)
        self.client = self.client_context.__enter__()

    def tearDown(self):
        self.client_context.__exit__(None, None, None)
        self.temp.cleanup()
        os.environ.pop('DATABASE_PATH', None)

    def test_crud_jugadores(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        temporadas = self.client.get('/api/temporadas').json()
        self.assertGreaterEqual(len(temporadas), 1)
        info = {'nombre': 'PruebaJugador', 'plataforma': 'PC', 'temporada_id': temporadas[0]['id'], 'partidas': 10, 'victorias': 2, 'eliminaciones': 15}
        r = self.client.post('/api/jugadores', json=info)
        self.assertEqual(r.status_code, 201, r.text)
        identificador = r.json()['id']
        self.assertEqual(self.client.get(f'/api/jugadores/{identificador}').json()['nombre'], 'PruebaJugador')
        self.assertTrue(any(x['id'] == identificador for x in self.client.get('/api/jugadores').json()))
        r = self.client.put(f'/api/jugadores/{identificador}', json={**info, 'victorias': 5})
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()['victorias'], 5)
        self.assertEqual(self.client.delete(f'/api/jugadores/{identificador}').status_code, 200)
        self.assertEqual(self.client.get(f'/api/jugadores/{identificador}').status_code, 404)

    def test_validation_and_foreign_keys(self):
        info = {'nombre': 'Usuario', 'plataforma': 'PC', 'temporada_id': 1, 'partidas': 1, 'victorias': 2, 'eliminaciones': 0}
        self.assertEqual(self.client.post('/api/jugadores', json=info).status_code, 422)
        info['victorias'] = 1
        info['temporada_id'] = 123456
        self.assertEqual(self.client.post('/api/jugadores', json=info).status_code, 400)
        self.assertEqual(self.client.delete('/api/temporadas/1').status_code, 409)
        self.assertEqual(self.client.delete('/api/jugadores/999999').status_code, 404)

    def test_season_creation(self):
        response = self.client.post('/api/temporadas', json={'nombre': 'Extra', 'capitulo': 'Capítulo 5'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.delete('/api/temporadas/' + str(response.json()['id'])).status_code, 200)

if __name__ == '__main__':
    unittest.main()
