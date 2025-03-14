# PROVIDER_GW (API Exposer Function Gateway)
[![PyPI version](https://img.shields.io/pypi/v/provider-gw.svg)](https://pypi.org/project/provider-gw/) ![Python](https://img.shields.io/badge/python-v3.12+-blue.svg) 


PROVIDER_GW is a gateway component designed to bridge legacy systems with the **Common API Framework (CAPIF)**. It simplifies the integration process, enabling legacy systems to interact seamlessly with CAPIF and adopt modern APIs without extensive modifications.

The component leverages the [Opencapif_sdk](https://labs.etsi.org/rep/ocf/sdk) to manage the interactions between systems and CAPIF effectively.

---

## Overview of PROVIDER_GW

PROVIDER_GW acts as an intermediary, translating and exposing APIs from legacy systems in a format compatible with CAPIF. It manages communication between the **Southbound interface** (legacy systems) and the **Northbound interface** (CAPIF), ensuring secure, reliable, and flexible API interaction.

![PROVIDER_GW Schema](./docs/provider_gw_schema.png)

---

## Getting Started

### Prerequisites

To use PROVIDER_GW, you need:
1. A registered user account in the CAPIF instance.
   - Contact your CAPIF administrator to obtain the necessary credentials (CAPIF username and password).
2. The following software dependencies:
   - Python 3.12+
   - `pipenv` or `virtualenv` for managing Python environments.

### Installation Steps

1. **Set up a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

2. **Install PROVIDER_GW:**
   ```bash
   pip install provider_gw
   ```

---

## Configuration

PROVIDER_GW requires two YAML configuration files:
1. **Northbound (`northbound.yaml`)**: Defines interaction with CAPIF. [**EXAMPLE**](./example_files/northbound.yaml)
2. **Southbound (`southbound.yaml`)**: Specifies communication with legacy systems. [**EXAMPLE**](./example_files/southbound.yaml)

### 1. Northbound Configuration

The `northbound.yaml` file defines the integration with CAPIF, including API specifications and OpenCapif SDK settings.

#### Key Fields

- **`ip`**: The IP address to expose.
- **`port`**: The port to expose.
- **`opencapif_sdk_configuration`**: Configures the OpenCapif SDK.
- **`openapi`**: Specifies the API exposed to CAPIF.

#### OpenCapif SDK Configuration

Here are the required fields for the `opencapif_sdk_configuration`:

- `capif_host`: CAPIF server domain.
- `register_host`: Registration server domain.
- `capif_https_port`: CAPIF server HTTPS port.
- `capif_register_port`: Registration server port.
- `capif_username`: CAPIF username.
- `capif_password`: CAPIF password.
- `debug_mode`: Enables detailed logs (`True` or `False`).
- `provider`: Specific fields of the provider(`cert_generation`,`supported_features`,`apiSuppFeats`)

**Example of a opencapif_sdk_configuration settings:**

```yaml
opencapif_sdk_configuration:
  capif_host: "capifcore"
  register_host: "register.capif"
  capif_https_port: "443"
  capif_register_port: "8004"
  capif_username: "echeva_0"
  capif_password: "excalibur"
  debug_mode: "True"
  provider:
    cert_generation:
      csr_common_name: "provider"
      csr_organizational_unit: "discovery"
      csr_organization: "telefonica"
      csr_locality: "madrid"
      csr_state_or_province_name: "madrid"
      csr_country_name: "ES"
      csr_email_address: "hola@gmail.com"
    supported_features: "0"
    apiSuppFeats: "0"
```

#### OpenAPI Configuration

The `openapi` field must adhere to the [OpenAPI Specification](https://spec.openapis.org/oas/v3.0.3). Use tools like [Swagger Editor](https://editor.swagger.io/) to validate the configuration.

**Example Configuration:**

```yaml
openapi:
  openapi: 3.0.0
  info:
    title: My API
    description: Example API for demonstration
    version: 1.0.0
  paths:
    /greet:
      get:
        summary: Say hello
        description: Returns a greeting message.
        responses:
          '200':
            description: Success
            content:
              application/json:
                schema:
                  type: object
                  properties:
                    message:
                      type: string
                      example: "Hello!"
```

---

### 2. Southbound Configuration

The `southbound.yaml` file defines how PROVIDER_GW interacts with legacy systems.

#### Key Fields

- **`ip`**: The IP address to expose.
- **`port`**: The port to expose.
- **`type`**: The type of endpoint (`REST` is currently supported).
- **`authentication_method`**: Authentication options:
  - `HTTP Basic Authentication`
  - `JWT Bearer Token`
- **`credentials`**:
  - For HTTP Basic Authentication:
    ```yaml
    username: "admin"
    password: "password123"
    ```
  - For JWT Bearer Token:
    ```yaml
    jwt: "your-token"
    ```
- **`paths`**: Maps Northbound API paths to Southbound API paths, including HTTP methods and parameter mappings.

**Example Configuration:**

```yaml
southbound:
  ip: 0.0.0.0
  port: 8000
  type: REST
  authentication_method: "JWT Bearer Token"
  credentials:
    jwt: "example-token"
  paths:
    - northbound_path: "/greet"
      southbound_path: "/hello"
      method: GET
    - northbound_path: "/greet/{name}"
      southbound_path: "/hello/{person}"
      method: GET
      parameters:
        - name: person
```

---

## Usage

1. Place the `northbound.yaml` and `southbound.yaml` configuration files in a working directory.
2. Use the following commands to interact with PROVIDER_GW:

- **Start the gateway (first-time setup):**
  ```bash
  cd ./directory/with/configuration/files
  provider_gw start
  ```

- **Run the gateway (after initial setup):**
  ```bash
  cd ./directory/with/configuration/files
  provider_gw run
  ```

- **Remove the gateway interface:**
  ```bash
  cd ./directory/with/configuration/files
  provider_gw remove
  ```

---

### Adding a New Endpoint

To add a new API endpoint:

1. Update `northbound.yaml` to define the endpoint.
2. Map the corresponding route in `southbound.yaml`.
3. Start the gateway with:
   ```bash
   cd ./directory/with/configuration/files
   provider_gw start
   ```

---

### Refreshing the Southbound JWT Token

To refresh the Southbound JWT token:

1. Update the `jwt` field in the `southbound.yaml` file.
2. Apply the changes with:
   ```bash
   cd ./directory/with/configuration/files
   provider_gw refresh
   ```

This ensures the new token is applied seamlessly.