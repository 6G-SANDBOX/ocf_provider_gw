from fastapi import FastAPI, Depends, HTTPException, Security, Request
from fastapi.security import HTTPBearer
from jose import jwt
from OpenSSL import crypto
import requests

class NorthboundAPI:
    def __init__(self, stored_routes, methods, parameters, responses, request_bodies, summaries, descriptions, tags, operation_ids, dynamic_models):
        self.stored_routes = stored_routes
        self.methods = methods
        self.parameters = parameters
        self.responses = responses
        self.request_bodies = request_bodies
        self.summaries = summaries
        self.descriptions = descriptions
        self.tags = tags
        self.operation_ids = operation_ids
        self.dynamic_models = dynamic_models
        self.PUBLIC_KEY = self.config_jwt()

    def config_jwt(self):
        try:
            with open(f"./provider_gw/provider_information/echeva_0/capif_cert_server.pem", "rb") as cert_file:
                cert = cert_file.read()

            crt_obj = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            pub_key_object = crt_obj.get_pubkey()
            pub_key_string = crypto.dump_publickey(crypto.FILETYPE_PEM, pub_key_object).decode("utf-8")
            return pub_key_string
        except Exception as e:
            print("Error in JWT configuration:", e)
            raise

    def decode_token(self, token: str = Security(HTTPBearer())):
        try:
            decoded = jwt.decode(token.credentials, self.PUBLIC_KEY, algorithms=["RS256"])
            return decoded
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")

    def create_route_handler(self, route, params, decode_token, method):
        southbound_paths = {'/projects': [{'southbound_path': '/v1/resources', 'method': 'GET'}, {'southbound_path': '/v1/resources', 'method': 'POST'}], '/projects/{projectId}': [{'southbound_path': '/v1/resources/{resource_id}', 'method': 'GET'}], '/tasks': [{'southbound_path': '/v1/resources/tasks', 'method': 'POST'}], '/users/{userId}/assignments': [{'southbound_path': '/v1/resources/users/{user_id}/information', 'method': 'GET'}]}
        params_dict = {'projectId': 'resource_id', 'userId': 'user_id'}

        possible_mappings = southbound_paths.get(route, [])
        southbound_mapping = next(
            (mapping for mapping in possible_mappings if mapping["method"].lower() == method.lower()),
            None
        )

        if not southbound_mapping:
            raise ValueError(f"No southbound path defined for route {route} with method {method}")

        southbound_url_template = southbound_mapping["southbound_path"]

        async def route_handler(
            request: Request,
            token=Depends(decode_token)
        ):
            try:
                path_params = request.path_params

                mapped_path_params = {params_dict.get(key, key): value for key, value in path_params.items()}

                payload = await request.json() if method.upper() in ["POST", "PUT", "PATCH"] else None
                try:
                    southbound_url = southbound_url_template.format(**mapped_path_params)
                except KeyError as e:
                    raise HTTPException(status_code=400, detail=f"Missing path parameter: {e}")

                headers = {key: value for key, value in request.headers.items() if key.lower() != "host"}

                headers["Authorization"] = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTczMjcwMjc3NH0.zaev1Pplm9QNx-C0Wr_YJ9nToAEa-giJMjXeaVp3weQ"

                if not headers["Authorization"]:
                    raise HTTPException(status_code=500, detail="JWT token not configured for southbound authentication")

                print(f"Forwarding {method.upper()} request to {southbound_url} with payload: {payload}")

                response = requests.request(
                    method=method.upper(),
                    url=f"http://0.0.0.0:8000{southbound_url}",
                    headers=headers,
                    json=payload,
                    timeout=10
                )
                response.raise_for_status()

                return response.json()

            except requests.exceptions.Timeout:
                raise HTTPException(status_code=504, detail="Southbound server timeout")
            except requests.exceptions.ConnectionError:
                raise HTTPException(status_code=502, detail="Southbound server not reachable")
            except requests.RequestException as e:
                raise HTTPException(status_code=502, detail=f"Error forwarding request: {str(e)}")

        return route_handler


    def generate_northbound_api(self, app: FastAPI):
        for n in range(len(self.stored_routes)):
            method = self.methods[n].lower()
            route = self.stored_routes[n]
            params = self.parameters[n]
            response_model = None
            if "200" in self.responses[n]:
                schema_ref = self.responses[n]["200"].get("content", {}).get("application/json", {}).get("schema", {}).get("$ref")
                if schema_ref:
                    model_name = schema_ref.split("/")[-1]
                    response_model = self.dynamic_models.get(model_name)

            summary = self.summaries[n]
            description = self.descriptions[n]
            tags = self.tags[n]
            operation_id = self.operation_ids[n]

            route_handler = self.create_route_handler(route, params, self.decode_token, method)

            app.add_api_route(
                path=route,
                endpoint=route_handler,
                methods=[method.upper()],
                response_model=response_model,
                summary=summary,
                description=description,
                tags=tags,
                operation_id=operation_id,
                responses=self.responses[n],
            )