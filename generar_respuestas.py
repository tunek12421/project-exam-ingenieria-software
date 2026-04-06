from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

style = doc.styles['Normal']
font = style.font
font.name = 'Arial'
font.size = Pt(11)

# === PORTADA ===
for _ in range(4):
    doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('EXAMEN FINAL')
run.bold = True
run.font.size = Pt(22)

subtitle = doc.add_paragraph()
subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = subtitle.add_run('Ingenieria de Software II')
run.font.size = Pt(16)
run.font.color.rgb = RGBColor(80, 80, 80)

doc.add_paragraph()

info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
info.add_run('Sistema de Gestion de Tareas').font.size = Pt(14)

doc.add_paragraph()
info2 = doc.add_paragraph()
info2.alignment = WD_ALIGN_PARAGRAPH.CENTER
info2.add_run('Repositorio: https://github.com/tunek12421/project-exam-ingenieria-software').font.size = Pt(10)

info3 = doc.add_paragraph()
info3.alignment = WD_ALIGN_PARAGRAPH.CENTER
info3.add_run('Rama: examen-final').font.size = Pt(10)

doc.add_page_break()

# === PARTE A: TEORIA ===
doc.add_heading('A. Parte Teorica (10 puntos)', level=1)

doc.add_heading('1. Diferencia entre arquitectura monolitica y arquitectura por capas', level=2)
doc.add_paragraph(
    'La arquitectura monolitica agrupa toda la logica del sistema (presentacion, negocio y datos) '
    'en un solo bloque desplegable, sin separacion clara de responsabilidades. Cualquier cambio '
    'requiere recompilar y redesplegar todo el sistema.'
)
doc.add_paragraph(
    'La arquitectura por capas divide el sistema en capas independientes (presentacion, logica de '
    'negocio, acceso a datos), donde cada capa tiene una responsabilidad especifica y se comunica '
    'solo con las capas adyacentes. Esto mejora la mantenibilidad, testabilidad y permite modificar '
    'una capa sin afectar directamente a las demas.'
)

doc.add_heading('2. Por que la refactorizacion no debe cambiar la funcionalidad del software', level=2)
doc.add_paragraph(
    'Porque el objetivo de la refactorizacion es mejorar la estructura interna del codigo (legibilidad, '
    'mantenibilidad, eliminacion de duplicados) sin alterar el comportamiento observable del sistema. '
    'Si se cambia la funcionalidad, ya no es refactorizacion sino una modificacion funcional, y se pierde '
    'la garantia de que el sistema sigue funcionando correctamente. Las pruebas existentes deben seguir '
    'pasando antes y despues de la refactorizacion, sirviendo como red de seguridad.'
)

doc.add_heading('3. Importancia de las pruebas automatizadas en un proyecto de software', level=2)
doc.add_paragraph(
    'Las pruebas automatizadas permiten detectar errores de forma temprana y repetible, sin intervencion '
    'manual. Garantizan que los cambios en el codigo (refactorizaciones, nuevas funcionalidades) no rompan '
    'la funcionalidad existente (pruebas de regresion). Reducen costos a largo plazo, aumentan la confianza '
    'en el codigo, facilitan la integracion continua (CI/CD) y sirven como documentacion viva del '
    'comportamiento esperado del sistema.'
)

doc.add_page_break()

# === PARTE B: PRACTICA ===
doc.add_heading('B. Parte Practica (90 puntos)', level=1)

# Actividad 1
doc.add_heading('Actividad 1: Organizacion inicial del proyecto y control de versiones', level=2)
doc.add_paragraph('Tecnologias utilizadas:')
bullets = [
    'Backend: Python 3 con Flask',
    'Frontend: HTML5, CSS3, JavaScript vanilla',
    'Base de datos: SQLite',
    'Pruebas: unittest + pytest',
    'Contenedores: Docker + Docker Compose',
]
for b in bullets:
    doc.add_paragraph(b, style='List Bullet')

doc.add_paragraph()
doc.add_paragraph('Estructura del proyecto:')
structure = """project-exam/
├── backend/
│   ├── src/
│   │   ├── config/         # Configuracion de BD + constantes
│   │   ├── controllers/    # Endpoints REST (Flask Blueprints)
│   │   ├── services/       # Logica de negocio y validaciones
│   │   ├── models/         # Modelo de datos Task
│   │   └── repositories/   # Acceso a datos (queries SQL)
│   └── tests/              # Pruebas unitarias
├── frontend/
│   ├── src/
│   │   ├── components/     # Componentes (task_card)
│   │   ├── pages/          # Logica de paginas (main)
│   │   ├── services/       # Cliente API (api_service)
│   │   └── assets/         # Estilos CSS
│   └── index.html
├── database/
│   ├── schema.sql          # Esquema de la BD
│   └── seed.sql            # Datos iniciales
├── docs/
│   └── architecture.md
├── tests/integration/      # Pruebas de integracion
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── .dockerignore
└── README.md"""

p = doc.add_paragraph()
run = p.add_run(structure)
run.font.name = 'Consolas'
run.font.size = Pt(8)

doc.add_paragraph()
doc.add_paragraph('Historial de commits en rama examen-final:')
commits = [
    'feat: estructura base del proyecto con modelo, repositorio y configuracion de BD',
    'feat: implementacion de API REST y frontend para gestion de tareas',
    'test: pruebas unitarias e integracion + documentacion arquitectonica',
    'refactor: correccion de code smells y mejora de calidad de codigo',
    'feat: dockerizacion del proyecto con Dockerfile y docker-compose',
]
for i, c in enumerate(commits, 1):
    doc.add_paragraph(f'{i}. {c}')

# Actividad 2
doc.add_heading('Actividad 2: Identificacion de estructura y arquitectura del sistema', level=2)

doc.add_heading('Tipo de arquitectura', level=3)
doc.add_paragraph(
    'El proyecto implementa una arquitectura por capas (Layered Architecture) con separacion '
    'clara de responsabilidades:'
)
capas = [
    'Capa de presentacion (Frontend): Interfaz HTML/CSS/JS que consume la API REST.',
    'Capa de controladores: Recibe peticiones HTTP, delega al servicio correspondiente.',
    'Capa de servicios (Logica de negocio): Validaciones y reglas de negocio.',
    'Capa de repositorios (Acceso a datos): Encapsula consultas SQL.',
    'Capa de modelos: Define las entidades del dominio.',
]
for c in capas:
    doc.add_paragraph(c, style='List Bullet')

doc.add_heading('Modulos identificados', level=3)
modulos = [
    ('config/database.py', 'Conexion SQLite con context manager + constantes'),
    ('models/task_model.py', 'Modelo Task con serializacion y deserializacion'),
    ('repositories/task_repository.py', 'CRUD a nivel de base de datos'),
    ('services/task_service.py', 'Validaciones y logica de negocio'),
    ('controllers/task_controller.py', 'Endpoints REST de la API'),
    ('frontend/src/services/', 'Cliente HTTP para consumir la API'),
    ('frontend/src/components/', 'Componentes visuales reutilizables'),
]
table = doc.add_table(rows=1, cols=2)
table.style = 'Table Grid'
hdr = table.rows[0].cells
hdr[0].text = 'Modulo'
hdr[1].text = 'Responsabilidad'
for mod, resp in modulos:
    row = table.add_row().cells
    row[0].text = mod
    row[1].text = resp

doc.add_heading('Mejoras arquitectonicas propuestas', level=3)
mejoras = [
    'Inyeccion de dependencias formal con contenedor DI.',
    'Sistema de migraciones (Alembic) en lugar de schema.sql directo.',
    'Middleware centralizado de manejo de errores en Flask.',
    'Autenticacion con JWT para proteger endpoints.',
    'Migrar frontend a framework (Vue/React) para mejor escalabilidad.',
]
for m in mejoras:
    doc.add_paragraph(m, style='List Bullet')

# Actividad 3
doc.add_heading('Actividad 3: Refactorizacion de codigo', level=2)
doc.add_paragraph('Code smells identificados y corregidos:')

smells = [
    ('Resource Leak (CRITICO)', 'Conexiones a BD sin try/finally',
     'Se implemento context manager con @contextmanager para garantizar cierre seguro de conexiones.'),
    ('Codigo SQL duplicado', 'Misma query SELECT repetida en 3 metodos del repositorio',
     'Se extrajo a constante de clase _BASE_SELECT (principio DRY).'),
    ('Import sin usar', 'from datetime import datetime en task_model.py',
     'Se elimino el import no utilizado.'),
    ('Magic number', 'Valor 200 hardcodeado para longitud maxima de titulo',
     'Se centralizo en constante TITLE_MAX_LENGTH en config/database.py.'),
    ('Codigo duplicado en servicio', 'Misma validacion de tarea existente en complete_task y delete_task',
     'Se extrajo a metodo privado _find_task_or_raise().'),
    ('Sin validacion frontend', 'Datos enviados sin validar al API',
     'Se agrego trim() y validacion de titulo vacio antes de enviar.'),
    ('Sin feedback UX', 'Solo alertas de error, sin confirmacion visual de exito',
     'Se implemento sistema de notificaciones toast con animacion CSS.'),
]

table2 = doc.add_table(rows=1, cols=3)
table2.style = 'Table Grid'
hdr2 = table2.rows[0].cells
hdr2[0].text = 'Code Smell'
hdr2[1].text = 'Problema'
hdr2[2].text = 'Solucion aplicada'
for smell, prob, sol in smells:
    row = table2.add_row().cells
    row[0].text = smell
    row[1].text = prob
    row[2].text = sol

# Actividad 4
doc.add_heading('Actividad 4: Implementacion de mejora funcional', level=2)
doc.add_paragraph('Funcionalidades implementadas en el sistema:')
funcionalidades = [
    'Registrar nueva tarea con titulo y descripcion.',
    'Listar todas las tareas ordenadas por fecha.',
    'Filtrar tareas pendientes (no completadas).',
    'Marcar una tarea como completada.',
    'Eliminar una tarea con confirmacion.',
    'Validacion de datos vacios (backend y frontend).',
    'Notificaciones visuales de exito.',
]
for f in funcionalidades:
    doc.add_paragraph(f, style='List Bullet')

doc.add_paragraph()
doc.add_paragraph('Endpoints de la API REST:')
endpoints = [
    ('GET', '/api/tasks', 'Listar todas las tareas'),
    ('GET', '/api/tasks?filter=pending', 'Listar tareas pendientes'),
    ('POST', '/api/tasks', 'Crear nueva tarea'),
    ('PATCH', '/api/tasks/<id>/complete', 'Marcar como completada'),
    ('DELETE', '/api/tasks/<id>', 'Eliminar tarea'),
]
table3 = doc.add_table(rows=1, cols=3)
table3.style = 'Table Grid'
hdr3 = table3.rows[0].cells
hdr3[0].text = 'Metodo'
hdr3[1].text = 'Endpoint'
hdr3[2].text = 'Descripcion'
for met, ep, desc in endpoints:
    row = table3.add_row().cells
    row[0].text = met
    row[1].text = ep
    row[2].text = desc

# Actividad 5
doc.add_heading('Actividad 5: Pruebas de software', level=2)
doc.add_paragraph('Se crearon 12 pruebas automatizadas (8 unitarias + 4 de integracion):')

doc.add_heading('Pruebas unitarias (backend/tests/test_task_service.py)', level=3)
unit_tests = [
    'test_create_task_with_valid_data - Verifica creacion correcta con datos validos.',
    'test_create_task_with_empty_title_raises_error - Titulo vacio lanza ValidationError.',
    'test_create_task_with_whitespace_title_raises_error - Titulo con solo espacios es rechazado.',
    'test_create_task_with_long_title_raises_error - Titulo mayor a 200 caracteres es rechazado.',
    'test_complete_task_success - Completar tarea existente funciona correctamente.',
    'test_complete_nonexistent_task_raises_error - Completar tarea inexistente lanza error.',
    'test_delete_nonexistent_task_raises_error - Eliminar tarea inexistente lanza error.',
    'test_get_all_tasks - Obtener todas las tareas retorna lista correcta.',
]
for t in unit_tests:
    doc.add_paragraph(t, style='List Bullet')

doc.add_heading('Pruebas de integracion (tests/integration/test_api_integration.py)', level=3)
int_tests = [
    'test_create_and_list_tasks - Flujo completo: crear tarea y verificar en listado.',
    'test_create_task_without_title_returns_400 - Crear sin titulo retorna error 400.',
    'test_complete_task_flow - Crear y luego completar una tarea.',
    'test_delete_nonexistent_task_returns_404 - Eliminar inexistente retorna 404.',
]
for t in int_tests:
    doc.add_paragraph(t, style='List Bullet')

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Resultado de ejecucion: 12 passed in 0.19s')
run.bold = True
run.font.color.rgb = RGBColor(0, 128, 0)

doc.add_paragraph()
evidencia = """$ python3 -m pytest -v
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-7.4.4

backend/tests/test_task_service.py::TestTaskService::test_complete_nonexistent_task_raises_error PASSED [  8%]
backend/tests/test_task_service.py::TestTaskService::test_complete_task_success PASSED [ 16%]
backend/tests/test_task_service.py::TestTaskService::test_create_task_with_empty_title_raises_error PASSED [ 25%]
backend/tests/test_task_service.py::TestTaskService::test_create_task_with_long_title_raises_error PASSED [ 33%]
backend/tests/test_task_service.py::TestTaskService::test_create_task_with_valid_data PASSED [ 41%]
backend/tests/test_task_service.py::TestTaskService::test_create_task_with_whitespace_title_raises_error PASSED [ 50%]
backend/tests/test_task_service.py::TestTaskService::test_delete_nonexistent_task_raises_error PASSED [ 58%]
backend/tests/test_task_service.py::TestTaskService::test_get_all_tasks PASSED [ 66%]
tests/integration/test_api_integration.py::TestTaskAPIIntegration::test_complete_task_flow PASSED [ 75%]
tests/integration/test_api_integration.py::TestTaskAPIIntegration::test_create_and_list_tasks PASSED [ 83%]
tests/integration/test_api_integration.py::TestTaskAPIIntegration::test_create_task_without_title_returns_400 PASSED [ 91%]
tests/integration/test_api_integration.py::TestTaskAPIIntegration::test_delete_nonexistent_task_returns_404 PASSED [100%]

============================== 12 passed in 0.19s =============================="""

p2 = doc.add_paragraph()
run2 = p2.add_run(evidencia)
run2.font.name = 'Consolas'
run2.font.size = Pt(7)

output_path = '/home/tunek/Descargas/DOCUMENTACION/project-exam/Examen_Final_Respuestas.docx'
doc.save(output_path)
print(f'Documento generado: {output_path}')
