
from fastapi import FastAPI
import uvicorn
from helpers import funcs 
from helpers.northbound import NorthboundAPI

if __name__ == "__main__":
    app = FastAPI()

    components = {'Project': {'type': 'object', 'properties': {'id': {'type': 'string', 'example': 'project-1234'}, 'name': {'type': 'string', 'example': 'Nuevo Proyecto'}, 'description': {'type': 'string', 'example': 'Descripción detallada del proyecto'}, 'startDate': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}, 'endDate': {'type': 'string', 'format': 'date', 'example': '2024-12-31'}, 'status': {'type': 'string', 'enum': ['active', 'completed', 'on_hold'], 'example': 'active'}}}, 'NewProject': {'type': 'object', 'required': ['name', 'startDate', 'endDate'], 'properties': {'name': {'type': 'string', 'example': 'Nuevo Proyecto'}, 'description': {'type': 'string', 'example': 'Descripción detallada del proyecto'}, 'startDate': {'type': 'string', 'format': 'date', 'example': '2024-01-01'}, 'endDate': {'type': 'string', 'format': 'date', 'example': '2024-12-31'}, 'status': {'type': 'string', 'enum': ['active', 'completed', 'on_hold'], 'example': 'active'}}}, 'Task': {'type': 'object', 'properties': {'id': {'type': 'string', 'example': 'task-5678'}, 'title': {'type': 'string', 'example': 'Implementar API'}, 'description': {'type': 'string', 'example': 'Desarrollar el endpoint para obtener lista de proyectos'}, 'assignedTo': {'type': 'string', 'example': 'user-1234'}, 'dueDate': {'type': 'string', 'format': 'date', 'example': '2024-06-30'}, 'status': {'type': 'string', 'enum': ['pending', 'in_progress', 'completed'], 'example': 'pending'}}}, 'NewTask': {'type': 'object', 'required': ['title', 'projectId'], 'properties': {'title': {'type': 'string', 'example': 'Implementar API'}, 'description': {'type': 'string', 'example': 'Desarrollar el endpoint para obtener lista de proyectos'}, 'projectId': {'type': 'string', 'example': 'project-1234'}, 'assignedTo': {'type': 'string', 'example': 'user-1234'}, 'dueDate': {'type': 'string', 'format': 'date', 'example': '2024-06-30'}}}}

    dynamic_models = {
        model_name: funcs.create_pydantic_model(model_name, model_schema)
        for model_name, model_schema in components.items()
    }

    funcs.register_dynamic_models(app, dynamic_models)
    stored_routes = ['/projects', '/projects', '/projects/{projectId}', '/tasks', '/users/{userId}/assignments']
    methods = ['get', 'post', 'get', 'post', 'get']
    parameters = [[{'in': 'query', 'name': 'page', 'schema': {'type': 'integer', 'default': 1}, 'description': 'Página de resultados'}, {'in': 'query', 'name': 'limit', 'schema': {'type': 'integer', 'default': 10}, 'description': 'Número de resultados por página'}], [], [{'in': 'path', 'name': 'projectId', 'required': True, 'schema': {'type': 'string'}, 'description': 'ID del proyecto'}], [], [{'in': 'path', 'name': 'userId', 'required': True, 'schema': {'type': 'string'}, 'description': 'ID del usuario'}]]
    responses = [{'200': {'description': 'Lista de proyectos', 'content': {'application/json': {'schema': {'type': 'array', 'items': {'$ref': '#/components/schemas/Project'}}}}}, '401': {'$ref': '#/components/responses/Unauthorized'}, '500': {'$ref': '#/components/responses/InternalServerError'}}, {'201': {'description': 'Proyecto creado correctamente', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Project'}}}}, '400': {'$ref': '#/components/responses/BadRequest'}, '401': {'$ref': '#/components/responses/Unauthorized'}}, {'200': {'description': 'Detalles del proyecto', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Project'}}}}, '404': {'$ref': '#/components/responses/NotFound'}, '401': {'$ref': '#/components/responses/Unauthorized'}}, {'201': {'description': 'Tarea creada', 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/Task'}}}}, '400': {'$ref': '#/components/responses/BadRequest'}, '401': {'$ref': '#/components/responses/Unauthorized'}}, {'200': {'description': 'Lista de tareas asignadas al usuario', 'content': {'application/json': {'schema': {'type': 'array', 'items': {'$ref': '#/components/schemas/TaskAssignment'}}}}}, '404': {'$ref': '#/components/responses/NotFound'}, '401': {'$ref': '#/components/responses/Unauthorized'}}]
    request_bodies = [None, {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/NewProject'}}}}, None, {'required': True, 'content': {'application/json': {'schema': {'$ref': '#/components/schemas/NewTask'}}}}, None]
    summaries = ['Obtener lista de proyectos', 'Crear un nuevo proyecto', 'Obtener detalles de un proyecto', 'Crear una nueva tarea', 'Obtener tareas asignadas a un usuario']
    descriptions = ['Devuelve una lista paginada de todos los proyectos', 'Crea un nuevo proyecto con los datos especificados', 'Devuelve los detalles de un proyecto específico por ID', 'Asigna una nueva tarea a un proyecto existente', 'Lista todas las tareas asignadas a un usuario en particular']
    tags = [['Projects'], ['Projects'], ['Projects'], ['Tasks'], ['Users']]
    operation_ids = ['getProjects', 'createProject', 'getProject', 'createTask', 'getUserAssignments']

    api = NorthboundAPI(stored_routes, methods, parameters, responses, request_bodies, summaries, descriptions, tags, operation_ids, dynamic_models)
    api.generate_northbound_api(app)
    uvicorn.run(app, host="0.0.0.0", port=3000)
