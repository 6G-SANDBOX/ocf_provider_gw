# AEF_GW (API Exposer Function Gateway)

AEF_GW is a component designed to facilitate the integration of legacy systems with the **Common API Framework (CAPIF)**. It streamlines the process, enabling legacy systems to interact with CAPIF, ensuring compatibility and simplifying the adoption of modern APIs.

AEF_GW leverages the [Opencapif_sdk](https://github.com/Telefonica/pesp_capif_sdk/tree/develop) for running the component.

## Understanding AEF_GW

AEF_GW acts as a bridge between legacy systems and CAPIF, translating and exposing APIs from legacy systems in a way that allows them to interact with the CAPIF environment. It handles communication both with legacy systems (southbound) and with CAPIF (northbound), ensuring secure, flexible, and reliable API interaction.

![aef_gw_schema](./docs/aef_gw_schema.png)

## Getting Started

### Requirements

To use AEF_GW, a registered user account within the target CAPIF instance is required. 

**Contact the administrator to obtain the required predefined credentials (CAPIF username and password).**

In addition, ensure the following dependencies are installed:

- Python 3.12+
- `pipenv` or `virtualenv` for managing dependencies

### Installation


1. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. Install aef_gw:
   ```bash
   pip install aef_gw
   ```

---

## Configuration

AEF_GW requires configuration files for both **northbound** (communication with CAPIF) and **southbound** (communication with legacy systems) integrations.

### Northbound Configuration

The northbound configuration is stored in a YAML file (`northbound.yaml`). 

The YAML northbound configuration includes:

- **ip**: The IP address that will be exposed.
- **port**: The port that will be exposed.
- **opencapif_sdk_configuration**: Configuration for the OpenCapif SDK.
- **openapi**: Configuration for the OpenAPI specification.

#### Opencapif SDK Configuration

These are the fields of the `opencapif_sdk_configuration` 

- `capif_host`: The domain name of the CAPIF host.
- `register_host`: The domain name of the register host.
- `capif_https_port`: The CAPIF host port number.
- `capif_register_port`: The register host port number.
- `capif_username`: The CAPIF username.
- `capif_password`: The CAPIF password.
- `debug_mode`: A boolean value to enable or disable SDK logs (e.g., `True` or `False`).

In the provider field only one field is required:

- `provider`: Fields for certificate generation, with `csr_country_name` requiring a two-letter country code.

Here is an example of `provider`:

```yaml
provider:
    cert_generation:
        csr_common_name: "name"
        csr_organizational_unit: "team"
        csr_organization: "ACME"
        csr_locality: "Texas"
        csr_state_or_province_name: "Artic"
        csr_country_name: "ES"
        csr_email_address: "yeti@gmail.com"
```

#### OpenAPI Configuration

The `openapi` field in the `northbound.yaml` file must follow the [OpenAPI Specification](https://spec.openapis.org/oas/v3.0.3). This configuration defines the structure of the API that will be exposed to CAPIF.

The `openapi` field must contain a valid OpenAPI object, as defined in the specification. Below is an example of a minimal OpenAPI configuration:

**Important:** Ensure that the OpenAPI configuration complies with the [OpenAPI Specification](https://spec.openapis.org/oas/v3.0.3). Tools like [Swagger Editor](https://editor.swagger.io/) or [Redocly OpenAPI Lint](https://redocly.com/tools/cli/openapi-lint/) can help validate your OpenAPI files.


Below is an example of the complete configuration structure for northbound:

```yaml
northbound:
  ip: 0.0.0.0
  port: 3000
  opencapif_sdk_configuration:
    capif_host: "capif-prev.mobilesandbox.cloud"
    register_host: "registercapif-prev.mobilesandbox.cloud"
    capif_https_port: "36212"
    capif_register_port: "36211"
    capif_username: "echeva_0"
    capif_password: "echevapass"
    debug_mode: "True"
    provider:
      cert_generation:
        csr_common_name: "name"
        csr_organizational_unit: "team"
        csr_organization: "ACME"
        csr_locality: "Texas"
        csr_state_or_province_name: "Artic"
        csr_country_name: "ES"
        csr_email_address: "yeti@gmail.com"
  openapi:
    openapi: 3.0.0
    info:
      title: Simple API
      description: This is a simple example of an API using OpenAPI 3.0
      version: 1.0.0
    servers:
      - url: http://localhost:8080
        description: Local server
    paths:
      /greet:
        get:
          summary: Greet the user
          description: Returns a greeting message.
          responses:
            '200':
              description: Successful response
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                        example: "Hello, world!"
      /greet/{name}:
        get:
          summary: Personalized greeting
          description: Returns a personalized greeting message.
          parameters:
            - name: name
              in: path
              required: true
              description: The name of the person to greet.
              schema:
                type: string
          responses:
            '200':
              description: Successful response
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
                        example: "Hello, John!"
    components:
      schemas:
        GreetingResponse:
          type: object
          properties:
            message:
              type: string
              example: "Hello!"
```

### Southbound Configuration

The southbound configuration is stored in a YAML file (`southbound.yaml`). 

The YAML southbound configuration includes:

- **ip**: The IP address to be exposed.
- **port**: The port to be exposed.
- **type**: The type of endpoint exposed in the southbound interface.
- **authentication_method**: In this version of AEF_GW, only HTTP Basic Authentication is supported.
- **credentials**: The credentials required for authentication in the southbound interface. 
- **paths**: The mapping between northbound and southbound paths, including the method type and parameter correlations, if applicable.

Below is an example of the complete configuration structure for southbound:
```yaml
southbound:
  ip: 0.0.0.0
  port: 8000
  type: REST
  authentication_method: "HTTP Basic Authentication"
  credentials:
    username: "admin"
    password: "password123"
  paths:
    - northbound_path: "/greet"
      southbound_path: "/meet"
      method: GET
    - northbound_path: "/greet/{name}"
      southbound_path: "/meet/{person}"
      method: GET
      parameters:
        - name: person
```


## Usage

1. Populate the configuration files:
   - Place the `northbound.yaml` file in a directory.
   - Place the `southbound.yaml` file in the same directory.

There are 3 possible commands to use Aef_gw
- Start the gateway for the first time:
   ```bash
   cd ./directory/with/configuration/files
   aef_gw start
   ```
- Run the gateway once you have started for the first time the Aef_gw:
  ```bash
  cd ./directory/with/configuration/files
  aef_gw run
  ```
- Remove the aef_gw interface:
  ```bash
  cd ./directory/with/configuration/files
  aef_gw remove
  ```

---

## Development

### Adding a New Endpoint

To add a new endpoint, modify the OpenAPI configuration `northbound.yaml` and define the corresponding route in the `southbound.yaml` file. Then execute 

  ```bash
   cd ./directory/with/configuration/files
   aef_gw start
  ```


---

## Contributing

We welcome contributions to improve AEF_GW. To contribute:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes and open a pull request.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For support or inquiries, please contact [support@example.com](mailto:support@example.com).
