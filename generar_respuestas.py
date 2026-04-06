from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

style = doc.styles['Normal']
style.font.name = 'Arial'
style.font.size = Pt(11)

# --- Portada ---
for _ in range(6):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('EXAMEN FINAL')
run.bold = True
run.font.size = Pt(20)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run('Ingenieria de Software II').font.size = Pt(14)

doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run('Enrique Lujan')

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run('Repositorio: github.com/tunek12421/project-exam-ingenieria-software')

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run('Rama: examen-enrique-lujan')

doc.add_page_break()

# ============================================================
# PARTE A - TEORIA
# ============================================================
doc.add_heading('A. Parte Teorica', level=1)

doc.add_heading('1. Diferencia entre arquitectura monolitica y por capas', level=2)
doc.add_paragraph(
    'En la monolitica todo el sistema esta en un solo bloque: presentacion, logica y datos juntos. '
    'Cualquier cambio obliga a redesplegar todo.'
)
doc.add_paragraph(
    'En la arquitectura por capas se separa en niveles independientes (presentacion, negocio, datos). '
    'Cada capa tiene su responsabilidad y solo se comunica con la capa de al lado. '
    'Esto hace que sea mas facil de mantener y de probar.'
)

doc.add_heading('2. Por que la refactorizacion no debe cambiar la funcionalidad', level=2)
doc.add_paragraph(
    'Porque la idea es mejorar como esta escrito el codigo por dentro, no lo que hace. '
    'Si cambias el comportamiento ya no es refactorizacion, es otra cosa. '
    'Las pruebas que ya existian tienen que seguir pasando igual antes y despues.'
)

doc.add_heading('3. Importancia de las pruebas automatizadas', level=2)
doc.add_paragraph(
    'Permiten detectar errores rapido y de forma repetible sin tener que probar a mano cada vez. '
    'Cuando haces cambios en el codigo, las pruebas te avisan si rompiste algo que antes funcionaba. '
    'Tambien sirven como documentacion de como debe comportarse el sistema.'
)

doc.add_page_break()

# ============================================================
# PARTE B - PRACTICA
# ============================================================
doc.add_heading('B. Parte Practica', level=1)

# --- Actividad 1 ---
doc.add_heading('Actividad 1 - Organizacion y control de versiones', level=2)

doc.add_paragraph('Stack usado:')
for item in ['Backend: Python 3 + Flask', 'Frontend: HTML/CSS/JS', 'BD: SQLite',
             'Tests: pytest', 'Docker + Docker Compose']:
    doc.add_paragraph(item, style='List Bullet')

doc.add_paragraph()
doc.add_paragraph('Estructura del proyecto:')
estructura = (
    'project-exam/\n'
    '  backend/src/ -> config, controllers, services, models, repositories\n'
    '  backend/tests/ -> pruebas unitarias\n'
    '  frontend/src/ -> components, pages, services, assets\n'
    '  database/ -> schema.sql, seed.sql\n'
    '  tests/integration/ -> pruebas de integracion\n'
    '  docs/architecture.md\n'
    '  Dockerfile, docker-compose.yml, README.md'
)
p = doc.add_paragraph()
run = p.add_run(estructura)
run.font.name = 'Consolas'
run.font.size = Pt(9)

doc.add_paragraph()
doc.add_paragraph('Commits realizados en la rama examen-enrique-lujan:')
commits = [
    'feat: estructura base con modelo, repositorio y configuracion de BD',
    'feat: implementacion de API REST y frontend',
    'test: pruebas unitarias e integracion + documentacion',
    'refactor: correccion de code smells',
    'feat: dockerizacion con Dockerfile y docker-compose',
    'docs: actualizacion del README',
    'feat: rediseno con listas de tareas, subtareas y progreso circular',
]
for i, c in enumerate(commits, 1):
    doc.add_paragraph(f'{i}. {c}')

# --- Actividad 2 ---
doc.add_heading('Actividad 2 - Arquitectura del sistema', level=2)

doc.add_paragraph(
    'El proyecto usa una arquitectura por capas. Cada parte tiene una responsabilidad clara:'
)
capas = [
    'Frontend (HTML/JS) -> lo que ve el usuario, consume la API',
    'Controllers -> reciben las peticiones HTTP y las pasan al servicio',
    'Services -> logica de negocio y validaciones',
    'Repositories -> consultas a la base de datos',
    'Models -> definen la estructura de los datos (TaskList, Subtask)',
]
for c in capas:
    doc.add_paragraph(c, style='List Bullet')

doc.add_paragraph()
doc.add_paragraph('Mejoras que se podrian hacer:')
mejoras = [
    'Usar un sistema de migraciones como Alembic en vez de schema.sql',
    'Agregar autenticacion con JWT',
    'Manejo centralizado de errores con un middleware',
    'Migrar el frontend a un framework como Vue o React',
]
for m in mejoras:
    doc.add_paragraph(m, style='List Bullet')

# --- Actividad 3 ---
doc.add_heading('Actividad 3 - Refactorizacion', level=2)

doc.add_paragraph('Problemas que encontre y como los corregi:')
doc.add_paragraph()

smells = [
    ('Conexiones a la BD no se cerraban si habia error',
     'Use context manager (with) para que siempre se cierre la conexion'),
    ('La misma query SQL repetida en 3 metodos',
     'La extraje a una constante _BASE_SELECT'),
    ('Import de datetime que no se usaba',
     'Lo elimine'),
    ('El numero 200 estaba puesto directo en el codigo',
     'Lo movi a una constante TITLE_MAX_LENGTH en config'),
    ('La misma validacion de "tarea no encontrada" en dos metodos',
     'Cree un metodo reutilizable _find_list_or_raise()'),
    ('No habia validacion en el frontend antes de enviar datos',
     'Agregue trim() y verificacion de campo vacio'),
    ('No habia aviso cuando algo salia bien',
     'Agregue notificaciones tipo toast'),
]

for problema, solucion in smells:
    p = doc.add_paragraph()
    run = p.add_run('Problema: ')
    run.bold = True
    p.add_run(problema)
    p = doc.add_paragraph()
    run = p.add_run('Solucion: ')
    run.bold = True
    p.add_run(solucion)
    doc.add_paragraph()

# --- Actividad 4 ---
doc.add_heading('Actividad 4 - Funcionalidad implementada', level=2)

doc.add_paragraph('El sistema permite:')
funciones = [
    'Crear listas de tareas con titulo y descripcion',
    'Agregar subtareas dentro de cada lista',
    'Marcar y desmarcar subtareas (toggle)',
    'Ver el porcentaje de avance con un circulo de progreso',
    'Expandir y colapsar las subtareas de cada lista',
    'Eliminar listas y subtareas',
    'Validacion de campos vacios en frontend y backend',
]
for f in funciones:
    doc.add_paragraph(f, style='List Bullet')

doc.add_paragraph()
doc.add_paragraph('Endpoints de la API:')
endpoints = [
    ('GET /api/task-lists', 'Obtener todas las listas con subtareas'),
    ('POST /api/task-lists', 'Crear una lista nueva'),
    ('DELETE /api/task-lists/<id>', 'Eliminar una lista'),
    ('POST /api/task-lists/<id>/subtasks', 'Agregar subtarea a una lista'),
    ('PATCH /api/subtasks/<id>/toggle', 'Marcar o desmarcar subtarea'),
    ('DELETE /api/subtasks/<id>', 'Eliminar una subtarea'),
]
for ep, desc in endpoints:
    p = doc.add_paragraph()
    run = p.add_run(ep)
    run.bold = True
    p.add_run(f' - {desc}')

# --- Actividad 5 ---
doc.add_heading('Actividad 5 - Pruebas', level=2)

doc.add_paragraph('Se crearon 21 pruebas automatizadas. Todas pasan.')
doc.add_paragraph()

doc.add_paragraph('Unitarias (15):')
unitarias = [
    'Crear lista con datos validos',
    'Titulo vacio lanza error',
    'Titulo con solo espacios lanza error',
    'Titulo muy largo lanza error',
    'Eliminar lista existente',
    'Eliminar lista inexistente lanza error',
    'Agregar subtarea a lista existente',
    'Agregar subtarea a lista inexistente lanza error',
    'Marcar subtarea como completada (toggle on)',
    'Desmarcar subtarea completada (toggle off)',
    'Toggle en subtarea inexistente lanza error',
    'Obtener todas las listas',
    'Progreso 0% sin subtareas',
    'Progreso 100% con todas completadas',
    'Progreso 25% con 1 de 4 completadas',
]
for t in unitarias:
    doc.add_paragraph(t, style='List Bullet')

doc.add_paragraph()
doc.add_paragraph('Integracion (6):')
integracion = [
    'Crear lista y verificar en listado',
    'Crear lista sin titulo da error 400',
    'Agregar subtareas y verificar progreso',
    'Toggle: marcar y desmarcar una subtarea',
    'Eliminar lista elimina sus subtareas (cascade)',
    'Eliminar lista inexistente da error 404',
]
for t in integracion:
    doc.add_paragraph(t, style='List Bullet')

doc.add_paragraph()
doc.add_paragraph('Evidencia de ejecucion:')
evidencia = (
    '$ python3 -m pytest -v\n'
    '21 passed in 0.39s\n'
    '\n'
    'Todas las pruebas unitarias y de integracion pasaron correctamente.'
)
p = doc.add_paragraph()
run = p.add_run(evidencia)
run.font.name = 'Consolas'
run.font.size = Pt(9)

# --- Guardar ---
output = '/home/tunek/Descargas/DOCUMENTACION/project-exam/Examen_Final_Respuestas.docx'
doc.save(output)
print(f'Documento generado: {output}')
