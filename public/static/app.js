const $ = (selector) => document.querySelector(selector);
let jugadores = [];
let temporadas = [];
let mensajeTimer;

function aviso(texto) {
  const caja = $('#mensaje');
  caja.textContent = texto;
  caja.classList.add('visible');
  clearTimeout(mensajeTimer);
  mensajeTimer = setTimeout(() => caja.classList.remove('visible'), 3800);
}

async function api(ruta, opciones = {}) {
  let respuesta;
  try { respuesta = await fetch(ruta, {headers: {'Content-Type': 'application/json'}, ...opciones}); }
  catch { throw new Error('No se pudo conectar con el servidor.'); }
  const cuerpo = await respuesta.json().catch(() => ({}));
  if (!respuesta.ok) {
    const detalle = cuerpo.detail;
    throw new Error(typeof detalle === 'string' ? detalle : 'Revisá los datos ingresados.');
  }
  return cuerpo;
}

function nodo(tag, texto, clase) {
  const elemento = document.createElement(tag);
  elemento.textContent = String(texto);
  if (clase) elemento.className = clase;
  return elemento;
}

async function cargar() {
  try {
    [jugadores, temporadas] = await Promise.all([api('/api/jugadores'), api('/api/temporadas')]);
    dibujarJugadores();
    dibujarTemporadas();
  } catch (e) { aviso(e.message); $('#lista').replaceChildren(nodo('tr', 'Error al cargar.')); }
}

function dibujarJugadores() {
  const filtro = $('#buscar').value.toLowerCase();
  const lista = $('#lista');
  lista.replaceChildren();
  const visibles = jugadores.filter(j => j.nombre.toLowerCase().includes(filtro));
  if (!visibles.length) {
    const fila = document.createElement('tr');
    const celda = nodo('td', 'No hay jugadores para mostrar.');
    celda.colSpan = 7; fila.append(celda); lista.append(fila);
  }
  visibles.forEach(j => {
    const fila = document.createElement('tr');
    [j.nombre, j.plataforma, j.temporada, j.partidas, j.victorias, j.eliminaciones].forEach(valor => fila.append(nodo('td', valor)));
    const opciones = document.createElement('td');
    const editar = nodo('button', 'Editar', 'action');
    editar.type = 'button'; editar.addEventListener('click', () => abrirModal(j));
    const eliminar = nodo('button', 'Eliminar', 'action danger');
    eliminar.type = 'button'; eliminar.addEventListener('click', () => borrarJugador(j));
    opciones.append(editar, eliminar); fila.append(opciones); lista.append(fila);
  });
  $('#total-jugadores').textContent = jugadores.length;
  $('#total-partidas').textContent = jugadores.reduce((s,j) => s + j.partidas, 0);
  $('#total-victorias').textContent = jugadores.reduce((s,j) => s + j.victorias, 0);
  $('#total-eliminaciones').textContent = jugadores.reduce((s,j) => s + j.eliminaciones, 0);
}

function dibujarTemporadas() {
  const lista = $('#lista-temporadas');
  lista.replaceChildren();
  temporadas.forEach(t => {
    const li = document.createElement('li');
    const info = document.createElement('div');
    info.append(nodo('strong', t.nombre), document.createElement('br'), nodo('small', t.capitulo));
    const borrar = nodo('button', 'Eliminar', 'action danger');
    borrar.type = 'button';
    borrar.addEventListener('click', async () => {
      if (!confirm(`¿Eliminar la temporada "${t.nombre}"?`)) return;
      try { await api(`/api/temporadas/${t.id}`, {method:'DELETE'}); aviso('Temporada eliminada.'); await cargar(); }
      catch(e){aviso(e.message);}
    });
    li.append(info,borrar); lista.append(li);
  });
}

function abrirModal(j = null) {
  const formulario = $('#form-jugador');
  formulario.reset();
  $('#modal-titulo').textContent = j ? 'Editar jugador' : 'Nuevo jugador';
  const selector = formulario.elements.temporada_id;
  selector.replaceChildren();
  temporadas.forEach(t => { const opcion = new Option(`${t.nombre} (${t.capitulo})`, t.id); selector.add(opcion); });
  if (!temporadas.length) { aviso('Primero agregá una temporada.'); return; }
  formulario.elements.id.value = j?.id ?? '';
  if (j) {
    ['nombre','plataforma','temporada_id','partidas','victorias','eliminaciones'].forEach(clave => {formulario.elements[clave].value = j[clave];});
  }
  $('#modal').showModal();
}

async function borrarJugador(j) {
  if (!confirm(`¿Eliminar a ${j.nombre}?`)) return;
  try { await api(`/api/jugadores/${j.id}`, {method:'DELETE'}); aviso('Jugador eliminado.'); await cargar(); }
  catch (e) { aviso(e.message); }
}

$('#buscar').addEventListener('input', dibujarJugadores);
$('#nuevo').addEventListener('click', () => abrirModal());
$('#cerrar').addEventListener('click', () => $('#modal').close());
$('#cancelar').addEventListener('click', () => $('#modal').close());
$('#form-jugador').addEventListener('submit', async (evento) => {
  evento.preventDefault();
  const f = evento.currentTarget.elements;
  const id = f.id.value;
  const datos = {nombre:f.nombre.value, plataforma:f.plataforma.value, temporada_id:Number(f.temporada_id.value), partidas:Number(f.partidas.value), victorias:Number(f.victorias.value), eliminaciones:Number(f.eliminaciones.value)};
  if (datos.victorias > datos.partidas) {aviso('Las victorias no pueden superar las partidas.'); return;}
  try {
    await api(id ? `/api/jugadores/${id}` : '/api/jugadores', {method:id ? 'PUT' : 'POST', body:JSON.stringify(datos)});
    $('#modal').close(); aviso(id ? 'Jugador actualizado.' : 'Jugador agregado.'); await cargar();
  } catch(e) {aviso(e.message);}
});
$('#form-temporada').addEventListener('submit', async evento => {
  evento.preventDefault(); const form = evento.currentTarget;
  const datos = {nombre: form.elements.nombre.value, capitulo: form.elements.capitulo.value};
  try {await api('/api/temporadas', {method:'POST',body:JSON.stringify(datos)}); form.reset(); aviso('Temporada agregada.'); await cargar();}
  catch(e){aviso(e.message);}
});
cargar();
