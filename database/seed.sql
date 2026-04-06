INSERT INTO task_lists (title, description) VALUES
('Revisar documentacion del proyecto', 'Leer y analizar los requisitos del sistema'),
('Configurar entorno de desarrollo', 'Instalar dependencias y configurar variables de entorno'),
('Implementar modulo de tareas', 'Desarrollar CRUD completo de tareas');

INSERT INTO subtasks (task_list_id, title, is_completed) VALUES
(1, 'Leer el enunciado del examen', 1),
(1, 'Identificar requisitos funcionales', 1),
(1, 'Documentar arquitectura', 0),
(1, 'Revisar criterios de evaluacion', 0),
(2, 'Instalar Python y Flask', 1),
(2, 'Configurar base de datos SQLite', 1),
(2, 'Crear archivo .env', 0),
(3, 'Crear modelo de datos', 1),
(3, 'Implementar repositorio', 0),
(3, 'Crear servicio con validaciones', 0),
(3, 'Desarrollar endpoints REST', 0);
