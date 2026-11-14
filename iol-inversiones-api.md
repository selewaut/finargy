# IOL Inversiones API

- **OpenAPI Version:** `3.1.2`
- **API Version:** `1.0.0`

## Introducción

Bienvenido a la API de IOL Inversiones. Accede a tus cuentas de brokerage de forma programática.

## Primeros Pasos

1. **Autenticarse:** Llamar a `POST /auth/token` con tus credenciales
2. **Obtener tu token:** Copiar el `access_token` de la respuesta
3. **Hacer requests:** Incluir el header `Authorization: Bearer <tu_token>`

## Formato de Respuesta

Todas las respuestas siguen esta estructura:

```json
{
  "meta": {
    "timestamp": "2025-12-24T10:00:00.000Z",
    "path": "/endpoint",
    "method": "GET",
    "status_code": 200,
    "trace_id": "0c5f1e4a-8a52-4b0e-9d3f-2f6f1f0b7c11"
  },
  "data": { ... },
  "error": null
}
```

En caso de error, `data` será `null` y `error` contendrá:

- `message`: Descripción del error
- `code`: Código de error
- `details`: Información adicional (errores de validación)

`meta.trace_id` identifica cada request y también se devuelve en el header `X-IOL-Trace-ID`. Informalo al contactar a soporte.

## Servers

- **URL:** `https://api.iolinversiones.com`
  - **Description:** Servidor API

## Tags

### Estado

Endpoints de verificación de estado

### Autenticación

Endpoints de autenticación y autorización

### Cuentas

Saldos de cuenta, posiciones, actividades y operaciones

### Assets

Datos de referencia de assets e información de trading

### Datos de Mercado

Cotizaciones de mercado en tiempo real, datos de precios y plazos de caución

### Órdenes

Endpoints para crear y gestionar órdenes de trading

### Cauciones

Operaciones de caución (repo)

### FCI

Suscripciones y rescates de Fondos Comunes de Inversión

### Watchlists

Listas de favoritos (watchlists) de assets

## Operations

### Verificación de estado

- **Method:** `GET`
- **Path:** `/health`
- **Tags:** Estado

Verificar disponibilidad y uptime de la API

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`status` (required)**

    `string` — Estado del servicio

  - **`timestamp` (required)**

    `string` — Timestamp ISO 8601

  - **`uptime` (required)**

    `number` — Segundos desde el inicio del servidor

  - **`version` (required)**

    `string` — Versión de la API

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "status": "ok",
    "timestamp": "",
    "uptime": 1,
    "version": ""
  },
  "error": null
}
```

### Obtener o refrescar token de autenticación

- **Method:** `POST`
- **Path:** `/auth/token`
- **Tags:** Autenticación

Autenticarse y obtener un access token. Usa grant password para el login inicial, o grant refresh\_token para renovar un token expirado.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`grant_type` (required)**

  `string`, possible values: `"password", "refresh_token"`

- **`password`**

  `string` — Tu contraseña (requerido para grant password)

- **`refresh_token`**

  `string` — Refresh token (requerido cuando grant\_type es "refresh\_token")

- **`username`**

  `string` — Tu nombre de usuario (requerido para grant password)

**Example:**

```json
{
  "grant_type": "password",
  "username": "",
  "password": "",
  "refresh_token": ""
}
```

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`access_token` (required)**

    `string` — Token JWT para autenticar requests

  - **`expires_at` (required)**

    `string` — Fecha y hora de expiración del access\_token (ISO 8601, UTC)

  - **`expires_in` (required)**

    `number` — Segundos que faltan hasta que expire el access\_token

  - **`refresh_token` (required)**

    `string` — Token para renovar el access\_token

  - **`token_type` (required)**

    `string` — Tipo de token (siempre "bearer")

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "access_token": "",
    "refresh_token": "",
    "expires_in": 1,
    "expires_at": "",
    "token_type": "bearer"
  },
  "error": null
}
```

### Obtener Saldos de Cuenta

- **Method:** `GET`
- **Path:** `/broker/accounts/{country}/balances`
- **Tags:** Cuentas

Obtener saldos de todas las cuentas de moneda en un país específico (AR retorna ARS+USD, US retorna solo USD).

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `country` required

- **In:** `path`

`string`, possible values: `"AR", "US"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "ars": {
      "currency": "ARS",
      "totals": {
        "t0": 1,
        "t1": 1,
        "t2": 1,
        "t3": 1
      },
      "available": {
        "t0": 1,
        "t1": 1,
        "t2": 1,
        "t3": 1
      },
      "committed": {
        "t0": 1,
        "t1": 1,
        "t2": 1,
        "t3": 1
      },
      "available_for_withdrawal": 1
    },
    "usd": {
      "currency": "USD",
      "totals": {
        "t0": 1,
        "t1": 1,
        "t2": 1,
        "t3": 1
      },
      "available": {
        "t0": 1,
        "t1": 1,
        "t2": 1,
        "t3": 1
      },
      "committed": {
        "t0": 1,
        "t1": 1,
        "t2": 1,
        "t3": 1
      },
      "available_for_withdrawal": 1
    }
  },
  "error": null
}
```

### Obtener Posiciones

- **Method:** `GET`
- **Path:** `/broker/accounts/{country}/positions`
- **Tags:** Cuentas

Obtener todas las posiciones (tenencias) para una cuenta de país específico. Usar valuation\_currency para cuentas AR.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `country` required

- **In:** `path`

`string`, possible values: `"AR", "US"`

##### `valuation_currency`

- **In:** `query`

`string`, possible values: `"ARS", "USD", "MEP", "CCL"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`account` (required)**

    `string` — Código de país de la cuenta

  - **`currency` (required)**

    `string` — Moneda de valuación

  - **`positions` (required)**

    `array`

    **Items:**

    - **`availability` (required)**

      `object`

      - **`quantity_available` (required)**

        `number`

      - **`quantity_held` (required)**

        `number`

      - **`quantity_pending` (required)**

        `number`

    - **`cost_basis` (required)**

      `object`

      - **`average_entry_price` (required)**

        `number`

      - **`days_held` (required)**

        `number`

      - **`entry_date` (required)**

        `string | null`

      - **`total_cost` (required)**

        `number`

    - **`instrument` (required)**

      `object`

      - **`asset_class` (required)**

        `string`

      - **`country` (required)**

        `string | null`

      - **`currency` (required)**

        `string`

      - **`exchange` (required)**

        `string`

      - **`lot_size` (required)**

        `number`

      - **`minimum_quantity` (required)**

        `number`

      - **`name` (required)**

        `string`

      - **`symbol` (required)**

        `string`

      - **`tradable` (required)**

        `boolean`

      - **`type` (required)**

        `string`

    - **`is_accredited` (required)**

      `boolean`

    - **`market_value` (required)**

      `object`

      - **`current_price` (required)**

        `number`

      - **`price_change` (required)**

        `number`

      - **`price_change_percent` (required)**

        `number`

    - **`maturity_date` (required)**

      `string | null`

    - **`parent_instrument` (required)**

      `object | null`

      - **`asset_class` (required)**

        `string`

      - **`country` (required)**

        `string | null`

      - **`currency` (required)**

        `string`

      - **`exchange` (required)**

        `string`

      - **`lot_size` (required)**

        `number`

      - **`minimum_quantity` (required)**

        `number`

      - **`name` (required)**

        `string`

      - **`symbol` (required)**

        `string`

      - **`tradable` (required)**

        `boolean`

      - **`type` (required)**

        `string`

    - **`portfolio_weight_percent` (required)**

      `number`

    - **`profit_loss` (required)**

      `object`

      - **`unrealized_pl` (required)**

        `number`

      - **`unrealized_pl_percent` (required)**

        `number`

    - **`quantity` (required)**

      `number`

  - **`positions_count` (required)**

    `number` — Cantidad de posiciones

  - **`total_market_value` (required)**

    `number` — Valor total del portfolio

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "account": "",
    "total_market_value": 1,
    "currency": "",
    "positions": [
      {
        "instrument": {
          "symbol": "",
          "name": "",
          "type": "",
          "asset_class": "",
          "exchange": "",
          "currency": "",
          "country": null,
          "tradable": true,
          "lot_size": 1,
          "minimum_quantity": 1
        },
        "quantity": 1,
        "availability": {
          "quantity_available": 1,
          "quantity_held": 1,
          "quantity_pending": 1
        },
        "cost_basis": {
          "average_entry_price": 1,
          "total_cost": 1,
          "entry_date": null,
          "days_held": 1
        },
        "market_value": {
          "current_price": 1,
          "price_change": 1,
          "price_change_percent": 1
        },
        "profit_loss": {
          "unrealized_pl": 1,
          "unrealized_pl_percent": 1
        },
        "portfolio_weight_percent": 1,
        "is_accredited": true,
        "parent_instrument": {
          "symbol": "",
          "name": "",
          "type": "",
          "asset_class": "",
          "exchange": "",
          "currency": "",
          "country": null,
          "tradable": true,
          "lot_size": 1,
          "minimum_quantity": 1
        },
        "maturity_date": null
      }
    ],
    "positions_count": 1
  },
  "error": null
}
```

### Obtener Actividades de Cuenta

- **Method:** `GET`
- **Path:** `/broker/accounts/activities`
- **Tags:** Cuentas

Obtener todos los movimientos de cuenta: depósitos, extracciones, débitos, créditos y también las operaciones (compras, ventas, cauciones, FCI, etc.). Filtrar por fecha, tipo, estado, país o moneda. Con `movement_type=operation` se obtienen solo los movimientos que provienen de operaciones; para el detalle de cada operación usar `/operations`.

`activity_type` y `activity_type_id` identifican el tipo de movimiento; pueden agregarse valores nuevos en el futuro.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `start_date` required

- **In:** `query`

`string` — Fecha de inicio (YYYY-MM-DD)

##### `end_date` required

- **In:** `query`

`string` — Fecha de fin (YYYY-MM-DD)

##### `movement_type`

- **In:** `query`

`string`, possible values: `"all", "deposit", "extraction", "debit", "credit", "operation", "currency_buy", "currency_sell"`

##### `state`

- **In:** `query`

`string`, possible values: `"all", "completed", "pending", "cancelled"`

##### `country`

- **In:** `query`

`string`, possible values: `"all", "AR", "US"`

##### `currency`

- **In:** `query`

`string`, possible values: `"all", "ARS", "USD"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `array`

  **Items:**

  - **`account_type` (required)**

    `string` — Tipo de cuenta, con el formato "{categoría} {moneda}" (ej: "CI AR$"). Categorías conocidas: | Código | Significado | |---|---| | CI | Cuenta de Inversión | | CI Ext. | Inversión Extranjera | La moneda es "AR$" (pesos argentinos) o "US$" (dólares estadounidenses). Por ejemplo, "CI AR$" es una Cuenta de Inversión en pesos argentinos.

  - **`activity_type` (required)**

    `string` — Tipo de movimiento, en inglés. Valores conocidos y su significado en español: | activity\_type | Español | |---|---| | Buy | Compra | | Sell | Venta | | Deposit | Depósito | | Withdrawal | Extracción | | Debit | Débito | | Credit | Crédito | | Rent Payment | Pago de Renta | | Amortization Payment | Pago de Amortización | | Dividend Payment | Pago de Dividendos | | Securities Lending | Préstamo de Títulos | | Collateral Liquidation | Liquidación de Caución | | Collateral | Caución | | Short Sale | Venta en Corto | | Call Writing | Lanzamiento de Calls | | Put Writing | Lanzamiento de Puts | | Securities Transfer In | Transferencia de Títulos Entrante | | Securities Transfer Out | Transferencia de Títulos Saliente | | Deferred Check Liquidation | Liquidación de Cheque de Pago Diferido | | Deferred Check Purchase | Compra de Cheque de Pago Diferido | | Deferred Check Sale | Venta de Cheque de Pago Diferido | | OTC Subscription | Suscripción OTC | | Mutual Fund (FCI) Subscription | Suscripción de FCI | | Mutual Fund (FCI) Redemption | Rescate de FCI | | Trust Subscription | Suscripción de Fideicomiso | | Trust Redemption | Rescate de Fideicomiso | | Collateral Taker Liquidation | Liquidación de Caución Tomadora | | Collateral Taker | Caución Tomadora | | Balance Remuneration | Remuneración de Saldos | | Stock Subscription | Suscripción de Acciones | | Capital Increase Subscription | Suscripción por Incremento de Capital | | Capital Increase Sale | Venta por Incremento de Capital | | Dividend Purchase | Compra de Dividendo | | Dividend Sale | Venta de Dividendo |

  - **`activity_type_id` (required)**

    `number` — Identificador numérico del tipo de movimiento

  - **`currency` (required)**

    `string` — Moneda: ARS o USD

  - **`fees` (required)**

    `object`

    - **`commission` (required)**

      `number` — Comisión neta

    - **`other` (required)**

      `number` — Otros impuestos

    - **`vat` (required)**

      `number` — IVA de comisión

  - **`id` (required)**

    `string` — Identificador único del movimiento

  - **`net_amount` (required)**

    `number` — Monto neto del movimiento

  - **`price` (required)**

    `number` — Precio del asset

  - **`qty` (required)**

    `number` — Cantidad del asset

  - **`settlement_date` (required)**

    `string` — Fecha de liquidación

  - **`status` (required)**

    `string` — Estado: completed, pending, cancelled

  - **`ticket_id` (required)**

    `string` — Identificador del ticket

  - **`trade_date` (required)**

    `string` — Fecha de la operación

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

  - **`total_count`**

    `number` — Cantidad total de actividades

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": "",
    "total_count": 1
  },
  "data": [
    {
      "id": "",
      "ticket_id": "",
      "activity_type": "",
      "activity_type_id": 1,
      "account_type": "",
      "trade_date": "",
      "settlement_date": "",
      "qty": 1,
      "price": 1,
      "currency": "",
      "net_amount": 1,
      "fees": {
        "commission": 1,
        "vat": 1,
        "other": 1
      },
      "status": ""
    }
  ],
  "error": null
}
```

### Obtener Operaciones de Trading

- **Method:** `GET`
- **Path:** `/broker/accounts/activities/operations`
- **Tags:** Cuentas

Obtener todas las operaciones de trading (compras, ventas, suscripciones, etc.). Filtrar por fecha, tipo, estado y más.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `start_date` required

- **In:** `query`

`string` — Fecha de inicio (YYYY-MM-DD) - requerido

##### `end_date` required

- **In:** `query`

`string` — Fecha de fin (YYYY-MM-DD) - requerido

##### `country`

- **In:** `query`

`string`, possible values: `"all", "AR", "US"`

##### `transaction_id`

- **In:** `query`

`string` — ID de transacción

##### `state`

- **In:** `query`

`string`, possible values: `"all", "completed", "pending", "cancelled", "finished"`

##### `specific_operations`

- **In:** `query`

`string` — Devuelve solo las operaciones de esa fecha (YYYY-MM-DD)

##### `transaction_type`

- **In:** `query`

`string`, possible values: `"purchase", "sale", "subscription", "redemption", "repo", "repo_borrowing", "capital_increase", "dividend_payment", "rent_payment", "amortization_payment"`

##### `currency`

- **In:** `query`

`string`, possible values: `"all", "ARS", "USD"`

##### `symbol`

- **In:** `query`

`string` — Símbolo del asset

##### `specie`

- **In:** `query`

`string`, possible values: `"c", "d", "ars"`

##### `term`

- **In:** `query`

`string`, possible values: `"T0", "T1", "T2", "T3", "T4"`

##### `asset_id`

- **In:** `query`

`string` — ID del asset

##### `asset_type`

- **In:** `query`

`string`, possible values: `"cedears", "stocks", "ons", "government_bonds", "letters", "options", "adrs", "deferred_payment_check", "collateral", "collateral_usd", "fci"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `array`

  **Items:**

  - **`asset_type` (required)**

    `string | null` — Tipo de asset

  - **`currency` (required)**

    `string` — Moneda: ARS o USD

  - **`description` (required)**

    `string` — Descripción legible

  - **`executed` (required)**

    `object`

    - **`amount` (required)**

      `number` — Monto ejecutado

    - **`price` (required)**

      `number` — Precio ejecutado

    - **`qty` (required)**

      `number` — Cantidad ejecutada

  - **`execution_date` (required)**

    `string` — Fecha cuando se ejecutó la orden

  - **`order` (required)**

    `object`

    - **`amount` (required)**

      `number` — Monto solicitado

    - **`price` (required)**

      `number` — Precio solicitado

    - **`qty` (required)**

      `number` — Cantidad solicitada

  - **`order_date` (required)**

    `string` — Fecha cuando se colocó la orden

  - **`order_id` (required)**

    `string` — Identificador único de la orden

  - **`status` (required)**

    `string` — Estado: completed, pending, cancelled, rejected

  - **`symbol` (required)**

    `string` — Símbolo/ticker del asset

  - **`term` (required)**

    `string` — Plazo de liquidación (T0, T1, T2, T3, T4)

  - **`ticket_id` (required)**

    `string` — Identificador del ticket

  - **`type` (required)**

    `string` — Tipo de operación (compra, venta, etc.)

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

  - **`total_count`**

    `number` — Cantidad total de operaciones

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": "",
    "total_count": 1
  },
  "data": [
    {
      "order_id": "",
      "ticket_id": "",
      "order_date": "",
      "execution_date": "",
      "type": "",
      "status": "",
      "symbol": "",
      "description": "",
      "asset_type": null,
      "term": "",
      "currency": "",
      "order": {
        "qty": 1,
        "price": 1,
        "amount": 1
      },
      "executed": {
        "qty": 1,
        "price": 1,
        "amount": 1
      }
    }
  ],
  "error": null
}
```

### Obtener Evolución de la Cuenta

- **Method:** `GET`
- **Path:** `/broker/accounts/{country}/portfolio/history`
- **Tags:** Cuentas

Obtener la evolución del patrimonio (Assets Under Management) de la cuenta entre dos fechas, día a día.

Útil para construir gráficos de evolución de patrimonio. Fines de semana y feriados del país indicado no se incluyen. Si `status` es `partial`, algunos días del rango todavía no tienen snapshot calculado (se encolaron para procesamiento en background) y deben reintentarse más tarde.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `country` required

- **In:** `path`

`string`, possible values: `"AR", "US"`

##### `start_date` required

- **In:** `query`

`string` — Fecha de inicio, inclusive (YYYY-MM-DD)

##### `end_date` required

- **In:** `query`

`string` — Fecha de fin, inclusive (YYYY-MM-DD)

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`account` (required)**

    `string` — Código de país de la cuenta

  - **`history` (required)**

    `array` — Snapshots de patrimonio por día hábil del rango

    **Items:**

    - **`cash_flow` (required)**

      `object`

      - **`deposits` (required)**

        `object`

        - **`ars` (required)**

          `number` — Depósitos del día en pesos

        - **`usd` (required)**

          `number` — Depósitos del día en dólares

      - **`withdrawals` (required)**

        `object`

        - **`ars` (required)**

          `number` — Retiros del día en pesos

        - **`usd` (required)**

          `number` — Retiros del día en dólares

    - **`date` (required)**

      `string` — Fecha del snapshot (YYYY-MM-DD)

    - **`equity` (required)**

      `object`

      - **`ars` (required)**

        `number` — Patrimonio valuado en pesos

      - **`usd_ccl` (required)**

        `number` — Patrimonio valuado en dólares CCL

      - **`usd_mep` (required)**

        `number` — Patrimonio valuado en dólares MEP

    - **`exchange_rate` (required)**

      `object`

      - **`ccl` (required)**

        `number` — Tipo de cambio CCL del día

      - **`mep` (required)**

        `number` — Tipo de cambio MEP del día

    - **`has_pledged_collateral` (required)**

      `boolean` — Si la cuenta tiene caución tomadora vigente ese día

  - **`missing_dates` (required)**

    `array` — Días hábiles del rango sin snapshot todavía (encolados para backfill si status es partial)

    **Items:**

    `string`

  - **`status` (required)**

    `string`, possible values: `"complete", "partial"`

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "account": "",
    "status": "complete",
    "history": [
      {
        "date": "",
        "equity": {
          "ars": 1,
          "usd_mep": 1,
          "usd_ccl": 1
        },
        "exchange_rate": {
          "mep": 1,
          "ccl": 1
        },
        "cash_flow": {
          "deposits": {
            "ars": 1,
            "usd": 1
          },
          "withdrawals": {
            "ars": 1,
            "usd": 1
          }
        },
        "has_pledged_collateral": true
      }
    ],
    "missing_dates": [
      ""
    ]
  },
  "error": null
}
```

### Crear Nueva Orden

- **Method:** `POST`
- **Path:** `/broker/orders`
- **Tags:** Órdenes

Colocar una nueva orden de compra o venta para un asset específico. Proporcionar quantity O notional, no ambos.

**Requiere header `X-Idempotency-Key`** - Identificador único (UUID) para prevenir órdenes duplicadas por reintentos de red.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `X-Idempotency-Key` required

- **In:** `header`

Identificador único para prevenir duplicados (UUID v4)

`string`, format: `uuid`

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`due_date` (required)**

  `string` — Fecha de vencimiento de la orden (YYYY-MM-DD)

- **`market_id` (required)**

  `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

- **`order_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`side` (required)**

  `string`, possible values: `"buy", "sell"`

- **`symbol` (required)**

  `string` — Símbolo ticker del asset

- **`limit_price`**

  `number` — Precio límite (requerido para órdenes limit)

- **`notional`**

  `number` — Monto en moneda (usar esto O quantity)

- **`quantity`**

  `number` — Cantidad de acciones (usar esto O notional)

- **`settlement_term`**

  `string`, possible values: `"T0", "T1", "T2"`

**Example:**

```json
{
  "symbol": "",
  "market_id": "BCBA",
  "side": "buy",
  "order_type": "limit",
  "quantity": 1,
  "notional": 1,
  "limit_price": 1,
  "due_date": "",
  "settlement_term": "T0"
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`due_date` (required)**

  `string` — Fecha de vencimiento de la orden (YYYY-MM-DD)

- **`market_id` (required)**

  `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

- **`order_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`side` (required)**

  `string`, possible values: `"buy", "sell"`

- **`symbol` (required)**

  `string` — Símbolo ticker del asset

- **`limit_price`**

  `number` — Precio límite (requerido para órdenes limit)

- **`notional`**

  `number` — Monto en moneda (usar esto O quantity)

- **`quantity`**

  `number` — Cantidad de acciones (usar esto O notional)

- **`settlement_term`**

  `string`, possible values: `"T0", "T1", "T2"`

**Example:**

```json
{
  "symbol": "",
  "market_id": "BCBA",
  "side": "buy",
  "order_type": "limit",
  "quantity": 1,
  "notional": 1,
  "limit_price": 1,
  "due_date": "",
  "settlement_term": "T0"
}
```

##### Content-Type: multipart/form-data

- **`due_date` (required)**

  `string` — Fecha de vencimiento de la orden (YYYY-MM-DD)

- **`market_id` (required)**

  `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

- **`order_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`side` (required)**

  `string`, possible values: `"buy", "sell"`

- **`symbol` (required)**

  `string` — Símbolo ticker del asset

- **`limit_price`**

  `number` — Precio límite (requerido para órdenes limit)

- **`notional`**

  `number` — Monto en moneda (usar esto O quantity)

- **`quantity`**

  `number` — Cantidad de acciones (usar esto O notional)

- **`settlement_term`**

  `string`, possible values: `"T0", "T1", "T2"`

**Example:**

```json
{
  "symbol": "",
  "market_id": "BCBA",
  "side": "buy",
  "order_type": "limit",
  "quantity": 1,
  "notional": 1,
  "limit_price": 1,
  "due_date": "",
  "settlement_term": "T0"
}
```

#### Responses

##### Status: 201 Response for status 201

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`messages` (required)**

    `array`

    **Items:**

    - **`code` (required)**

      `string` — Código del mensaje

    - **`message` (required)**

      `string` — Texto del mensaje

  - **`order_id` (required)**

    `string` — Identificador único de la orden

  - **`successful_purchase` (required)**

    `boolean` — Si la orden fue colocada exitosamente

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "successful_purchase": true,
    "messages": [
      {
        "code": "",
        "message": ""
      }
    ],
    "order_id": ""
  },
  "error": null
}
```

### Estimar Costos de Orden

- **Method:** `POST`
- **Path:** `/broker/orders/estimate`
- **Tags:** Órdenes

Previsualizar comisiones y cargos regulatorios para una orden antes de colocarla.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`due_date` (required)**

  `string` — Fecha de vencimiento de la orden (YYYY-MM-DD)

- **`market_id` (required)**

  `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

- **`order_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`side` (required)**

  `string`, possible values: `"buy", "sell"`

- **`symbol` (required)**

  `string` — Símbolo ticker del asset

- **`limit_price`**

  `number` — Precio límite (requerido para órdenes limit)

- **`notional`**

  `number` — Monto en moneda (usar esto O quantity)

- **`quantity`**

  `number` — Cantidad de acciones (usar esto O notional)

- **`settlement_term`**

  `string`, possible values: `"T0", "T1", "T2"`

**Example:**

```json
{
  "symbol": "",
  "market_id": "BCBA",
  "side": "buy",
  "order_type": "limit",
  "quantity": 1,
  "notional": 1,
  "limit_price": 1,
  "due_date": "",
  "settlement_term": "T0"
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`due_date` (required)**

  `string` — Fecha de vencimiento de la orden (YYYY-MM-DD)

- **`market_id` (required)**

  `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

- **`order_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`side` (required)**

  `string`, possible values: `"buy", "sell"`

- **`symbol` (required)**

  `string` — Símbolo ticker del asset

- **`limit_price`**

  `number` — Precio límite (requerido para órdenes limit)

- **`notional`**

  `number` — Monto en moneda (usar esto O quantity)

- **`quantity`**

  `number` — Cantidad de acciones (usar esto O notional)

- **`settlement_term`**

  `string`, possible values: `"T0", "T1", "T2"`

**Example:**

```json
{
  "symbol": "",
  "market_id": "BCBA",
  "side": "buy",
  "order_type": "limit",
  "quantity": 1,
  "notional": 1,
  "limit_price": 1,
  "due_date": "",
  "settlement_term": "T0"
}
```

##### Content-Type: multipart/form-data

- **`due_date` (required)**

  `string` — Fecha de vencimiento de la orden (YYYY-MM-DD)

- **`market_id` (required)**

  `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

- **`order_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`side` (required)**

  `string`, possible values: `"buy", "sell"`

- **`symbol` (required)**

  `string` — Símbolo ticker del asset

- **`limit_price`**

  `number` — Precio límite (requerido para órdenes limit)

- **`notional`**

  `number` — Monto en moneda (usar esto O quantity)

- **`quantity`**

  `number` — Cantidad de acciones (usar esto O notional)

- **`settlement_term`**

  `string`, possible values: `"T0", "T1", "T2"`

**Example:**

```json
{
  "symbol": "",
  "market_id": "BCBA",
  "side": "buy",
  "order_type": "limit",
  "quantity": 1,
  "notional": 1,
  "limit_price": 1,
  "due_date": "",
  "settlement_term": "T0"
}
```

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`amount` (required)**

    `object`

    - **`currency` (required)**

      `string` — Código de moneda

    - **`value` (required)**

      `number` — Monto total

  - **`commission` (required)**

    `object`

    - **`currency` (required)**

      `string` — Código de moneda

    - **`value` (required)**

      `number` — Monto de comisión

  - **`regulatory_fees` (required)**

    `object`

    - **`market_fee` (required)**

      `object`

      - **`currency` (required)**

        `string` — Código de moneda

      - **`value` (required)**

        `number` — Cargo del mercado

    - **`vat` (required)**

      `object`

      - **`currency` (required)**

        `string` — Código de moneda

      - **`value` (required)**

        `number` — Monto de IVA

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "amount": {
      "currency": "",
      "value": 1
    },
    "commission": {
      "currency": "",
      "value": 1
    },
    "regulatory_fees": {
      "vat": {
        "currency": "",
        "value": 1
      },
      "market_fee": {
        "currency": "",
        "value": 1
      }
    }
  },
  "error": null
}
```

### Cancelar Orden

- **Method:** `DELETE`
- **Path:** `/broker/orders/{order_id}`
- **Tags:** Órdenes

Cancelar una orden existente. Solo se pueden cancelar órdenes pendientes o en progreso.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `order_id` required

- **In:** `path`

`string` — ID de la orden a cancelar

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`cancelled` (required)**

    `boolean` — Si la cancelación fue exitosa

  - **`order_id` (required)**

    `string` — Identificador de la orden

  - **`status` (required)**

    `string` — Nuevo estado de la orden (cancelled)

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "order_id": "",
    "status": "",
    "cancelled": true
  },
  "error": null
}
```

### Obtener Cotización de Mercado

- **Method:** `GET`
- **Path:** `/broker/market-data/{symbol}/quote`
- **Tags:** Datos de Mercado

Obtener cotización de mercado en tiempo real para un asset incluyendo precio actual, rango diario y volumen operado.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `symbol` required

- **In:** `path`

`string` — Símbolo ticker del asset (ej: GGAL, AL30, AAPL)

##### `market` required

- **In:** `query`

`string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

##### `term` required

- **In:** `query`

`string`, possible values: `"T0", "T1"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`change` (required)**

    `object`

    - **`amount` (required)**

      `number`

    - **`percent` (required)**

      `number`

  - **`currency` (required)**

    `string` — Moneda de operación

  - **`last_updated` (required)**

    `string`

  - **`lot_size` (required)**

    `number`

  - **`market` (required)**

    `string` — Mercado/bolsa (mayúsculas)

  - **`maturity_date` (required)**

    `string | null`

  - **`prices` (required)**

    `object`

    - **`close` (required)**

      `number`

    - **`current` (required)**

      `number`

    - **`high` (required)**

      `number`

    - **`low` (required)**

      `number`

    - **`open` (required)**

      `number`

    - **`previous_close` (required)**

      `number`

  - **`settlement_term` (required)**

    `string` — Plazo de liquidación (mayúsculas)

  - **`symbol` (required)**

    `string` — Símbolo ticker del asset (mayúsculas)

  - **`volume` (required)**

    `object`

    - **`amount` (required)**

      `number`

    - **`shares` (required)**

      `number`

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "symbol": "",
    "market": "",
    "settlement_term": "",
    "currency": "",
    "prices": {
      "current": 1,
      "open": 1,
      "close": 1,
      "high": 1,
      "low": 1,
      "previous_close": 1
    },
    "change": {
      "amount": 1,
      "percent": 1
    },
    "volume": {
      "shares": 1,
      "amount": 1
    },
    "lot_size": 1,
    "last_updated": "",
    "maturity_date": null
  },
  "error": null
}
```

### Obtener Order Book

- **Method:** `GET`
- **Path:** `/broker/market-data/{symbol}/depth`
- **Tags:** Datos de Mercado

Obtener el order book (profundidad de mercado) mostrando órdenes de compra y venta a diferentes niveles de precio.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `symbol` required

- **In:** `path`

`string` — Símbolo ticker del asset (ej: GGAL, AL30, AAPL)

##### `market` required

- **In:** `query`

`string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

##### `term` required

- **In:** `query`

`string`, possible values: `"T0", "T1"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`asks` (required)**

    `array`

    **Items:**

    - **`position` (required)**

      `number`

    - **`price` (required)**

      `number`

    - **`size` (required)**

      `number`

  - **`bids` (required)**

    `array`

    **Items:**

    - **`position` (required)**

      `number`

    - **`price` (required)**

      `number`

    - **`size` (required)**

      `number`

  - **`last_updated` (required)**

    `string`

  - **`lot_size` (required)**

    `number`

  - **`market` (required)**

    `string` — Mercado/bolsa (mayúsculas)

  - **`settlement_term` (required)**

    `string` — Plazo de liquidación (mayúsculas)

  - **`symbol` (required)**

    `string` — Símbolo ticker del asset (mayúsculas)

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "symbol": "",
    "market": "",
    "settlement_term": "",
    "bids": [
      {
        "price": 1,
        "size": 1,
        "position": 1
      }
    ],
    "asks": [
      {
        "price": 1,
        "size": 1,
        "position": 1
      }
    ],
    "lot_size": 1,
    "last_updated": ""
  },
  "error": null
}
```

### Screener de Mercado

- **Method:** `GET`
- **Path:** `/broker/market-data/screener`
- **Tags:** Datos de Mercado

Navegar múltiples assets a la vez filtrados por país, tipo de asset y panel de trading.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `country` required

- **In:** `query`

`string`, possible values: `"AR", "US"`

##### `asset_type` required

- **In:** `query`

`string` — Tipo de asset (ej: Acciones, Bonos, Cedears)

##### `panel` required

- **In:** `query`

`string` — Nombre del panel de trading (ej: general, merval, panel\_general)

##### `term` required

- **In:** `query`

`string`, possible values: `"T0", "T1"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `array`

  **Items:**

  - **`book` (required)**

    `object`

    - **`ask` (required)**

      `object`

      - **`price` (required)**

        `number`

      - **`size` (required)**

        `number`

    - **`bid` (required)**

      `object`

      - **`price` (required)**

        `number`

      - **`size` (required)**

        `number`

  - **`instrument` (required)**

    `object`

    - **`currency` (required)**

      `string` — Moneda de operación

    - **`market` (required)**

      `string` — Mercado/bolsa (mayúsculas)

    - **`name` (required)**

      `string` — Descripción del instrumento

    - **`symbol` (required)**

      `string` — Símbolo ticker (mayúsculas)

  - **`quotes` (required)**

    `object`

    - **`change_percent` (required)**

      `number` — Variación porcentual

    - **`close` (required)**

      `number` — Precio de cierre anterior

    - **`high` (required)**

      `number` — Precio máximo

    - **`last` (required)**

      `number` — Último precio

    - **`low` (required)**

      `number` — Precio mínimo

    - **`open` (required)**

      `number` — Precio de apertura

    - **`volume` (required)**

      `number` — Volumen operado

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

  - **`total_count`**

    `number`

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": "",
    "total_count": 1
  },
  "data": [
    {
      "instrument": {
        "symbol": "",
        "name": "",
        "market": "",
        "currency": ""
      },
      "quotes": {
        "last": 1,
        "open": 1,
        "close": 1,
        "high": 1,
        "low": 1,
        "change_percent": 1,
        "volume": 1
      },
      "book": {
        "bid": {
          "price": 1,
          "size": 1
        },
        "ask": {
          "price": 1,
          "size": 1
        }
      }
    }
  ],
  "error": null
}
```

### Obtener Cadena de Opciones

- **Method:** `GET`
- **Path:** `/broker/market-data/{symbol}/options`
- **Tags:** Datos de Mercado

Obtener todos los contratos de opciones disponibles para un activo subyacente.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `symbol` required

- **In:** `path`

`string` — Símbolo ticker del activo subyacente (ej: GGAL)

##### `market` required

- **In:** `query`

`string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `array`

  **Items:**

  - **`book` (required)**

    `object`

    - **`ask` (required)**

      `object`

      - **`price` (required)**

        `number`

      - **`size` (required)**

        `number`

    - **`bid` (required)**

      `object`

      - **`price` (required)**

        `number`

      - **`size` (required)**

        `number`

  - **`option` (required)**

    `object`

    - **`state` (required)**

      `string` — Estado de la opción

    - **`strike_price` (required)**

      `number` — Precio de ejercicio

    - **`type` (required)**

      `string` — Tipo de opción: call o put

  - **`quotes` (required)**

    `object`

    - **`change_percent` (required)**

      `number` — Variación porcentual

    - **`close` (required)**

      `number` — Precio de cierre anterior

    - **`high` (required)**

      `number` — Precio máximo

    - **`last` (required)**

      `number` — Último precio

    - **`low` (required)**

      `number` — Precio mínimo

    - **`open` (required)**

      `number` — Precio de apertura

    - **`volume` (required)**

      `number` — Volumen operado

  - **`symbol` (required)**

    `string` — Símbolo de la opción

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

  - **`total_count`**

    `number`

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": "",
    "total_count": 1
  },
  "data": [
    {
      "symbol": "",
      "option": {
        "type": "",
        "strike_price": 1,
        "state": ""
      },
      "quotes": {
        "last": 1,
        "open": 1,
        "close": 1,
        "high": 1,
        "low": 1,
        "change_percent": 1,
        "volume": 1
      },
      "book": {
        "bid": {
          "price": 1,
          "size": 1
        },
        "ask": {
          "price": 1,
          "size": 1
        }
      }
    }
  ],
  "error": null
}
```

### Obtener Plazos de Caución

- **Method:** `GET`
- **Path:** `/broker/market-data/repos/terms`
- **Tags:** Datos de Mercado

Obtener plazos disponibles para inversión a plazo fijo (caución/repo).

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `currency` required

- **In:** `query`

`string`, possible values: `"ARS", "USD"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `array`

  **Items:**

  - **`due_date` (required)**

    `string` — Fecha de vencimiento

  - **`max_amount` (required)**

    `number` — Monto máximo de inversión

  - **`min_amount` (required)**

    `number` — Monto mínimo de inversión

  - **`term_days` (required)**

    `number` — Duración del plazo en días

  - **`term_id` (required)**

    `number` — Identificador del plazo (usar para colocar órdenes)

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": [
    {
      "term_id": 1,
      "term_days": 1,
      "max_amount": 1,
      "min_amount": 1,
      "due_date": ""
    }
  ],
  "error": null
}
```

### Obtener Order Book de Cauciones

- **Method:** `GET`
- **Path:** `/broker/market-data/repos/quotes`
- **Tags:** Datos de Mercado

Obtener el order book para operaciones de caución mostrando tasas disponibles para un plazo específico.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `term_id` required

- **In:** `query`

`number` — ID del plazo obtenido del endpoint /repos/terms

##### `currency` required

- **In:** `query`

`string`, possible values: `"ARS", "USD"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `array`

  **Items:**

  - **`ask` (required)**

    `object`

    - **`amount` (required)**

      `number` — Monto disponible

    - **`rate` (required)**

      `number` — Tasa nominal anual (TNA) solicitada por el tomador

  - **`bid` (required)**

    `object`

    - **`amount` (required)**

      `number` — Monto disponible

    - **`rate` (required)**

      `number` — Tasa nominal anual (TNA) ofrecida por el colocador

  - **`position` (required)**

    `number` — Posición en el order book

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": [
    {
      "position": 1,
      "bid": {
        "rate": 1,
        "amount": 1
      },
      "ask": {
        "rate": 1,
        "amount": 1
      }
    }
  ],
  "error": null
}
```

### Obtener Datos Históricos OHLCV

- **Method:** `GET`
- **Path:** `/broker/market-data/{symbol}/bars`
- **Tags:** Datos de Mercado

Obtener datos históricos de precio (OHLCV - Open, High, Low, Close, Volume) para un asset en un rango de fechas. Devuelve una barra por día (no hay otros intervalos disponibles).

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `symbol` required

- **In:** `path`

`string` — Símbolo ticker del asset (ej: GGAL, AL30, AAPL)

##### `market` required

- **In:** `query`

`string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

##### `from` required

- **In:** `query`

`string` — Fecha y hora de inicio, formato yyyy-MM-dd HH:mm:ss (ej: 2023-01-01 03:00:00)

##### `to` required

- **In:** `query`

`string` — Fecha y hora de fin, formato yyyy-MM-dd HH:mm:ss (ej: 2026-02-03 23:59:59)

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`bars` (required)**

    `array`

    **Items:**

    - **`close` (required)**

      `number` — Precio de cierre

    - **`datetime` (required)**

      `string` — Fecha y hora en formato ISO 8601

    - **`high` (required)**

      `number` — Precio máximo

    - **`low` (required)**

      `number` — Precio mínimo

    - **`open` (required)**

      `number` — Precio de apertura

    - **`timestamp` (required)**

      `number` — Unix timestamp en segundos

    - **`volume` (required)**

      `number` — Volumen operado

  - **`market` (required)**

    `string` — Mercado/bolsa (mayúsculas)

  - **`symbol` (required)**

    `string` — Símbolo ticker del asset (mayúsculas)

  - **`total_bars` (required)**

    `number` — Cantidad total de barras devueltas

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "symbol": "",
    "market": "",
    "bars": [
      {
        "timestamp": 1,
        "datetime": "",
        "open": 1,
        "high": 1,
        "low": 1,
        "close": 1,
        "volume": 1
      }
    ],
    "total_bars": 1
  },
  "error": null
}
```

### Obtener Detalles del Asset

- **Method:** `GET`
- **Path:** `/broker/assets/{symbol}`
- **Tags:** Assets

Obtener información detallada sobre un asset específico incluyendo parámetros de trading.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `symbol` required

- **In:** `path`

`string` — Símbolo ticker del asset (ej: GGAL, AL30, AAPL)

##### `market` required

- **In:** `query`

`string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`asset_type` (required)**

    `string` — Tipo de asset

  - **`country` (required)**

    `string` — Código de país (AR, US, etc.)

  - **`currency` (required)**

    `string` — Moneda de operación

  - **`default_settlement_term` (required)**

    `string` — Plazo de liquidación por defecto (mayúsculas)

  - **`market` (required)**

    `string` — Mercado/bolsa (mayúsculas)

  - **`name` (required)**

    `string` — Descripción/nombre del asset

  - **`symbol` (required)**

    `string` — Símbolo ticker del asset (mayúsculas)

  - **`trading_info` (required)**

    `object`

    - **`lot_size` (required)**

      `number` — Tamaño del lote para operar

    - **`minimum_investment` (required)**

      `number` — Monto mínimo de inversión

    - **`minimum_quantity` (required)**

      `number` — Cantidad mínima operable

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "symbol": "",
    "name": "",
    "asset_type": "",
    "country": "",
    "market": "",
    "currency": "",
    "default_settlement_term": "",
    "trading_info": {
      "lot_size": 1,
      "minimum_investment": 1,
      "minimum_quantity": 1
    }
  },
  "error": null
}
```

### Obtener Tipos de Assets

- **Method:** `GET`
- **Path:** `/broker/assets/types`
- **Tags:** Assets

Obtener todos los tipos de assets disponibles para un mercado específico. Usa estos tipos para filtrar en el screener.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `country` required

- **In:** `query`

`string`, possible values: `"AR", "US"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `array`

  **Items:**

  - **`id` (required)**

    `string` — ID del tipo de asset (minúsculas, con guiones bajos)

  - **`name` (required)**

    `string` — Nombre del tipo de asset

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": [
    {
      "id": "",
      "name": ""
    }
  ],
  "error": null
}
```

### Obtener Paneles de Trading

- **Method:** `GET`
- **Path:** `/broker/assets/panels`
- **Tags:** Assets

Obtener paneles de trading disponibles (listas predefinidas de assets) para un tipo de asset. Usar con el screener de mercado.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `country` required

- **In:** `query`

`string`, possible values: `"AR", "US"`

##### `asset_type` required

- **In:** `query`

`string` — Tipo de asset (obtenido de /assets/types)

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `array`

  **Items:**

  - **`id` (required)**

    `string` — Identificador del panel

  - **`name` (required)**

    `string` — Nombre del panel

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": [
    {
      "id": "",
      "name": ""
    }
  ],
  "error": null
}
```

### Estimar Costos de Caución

- **Method:** `POST`
- **Path:** `/broker/repos/estimate`
- **Tags:** Cauciones

Previsualizar comisiones e impuestos para una operación de caución antes de colocarla.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`amount` (required)**

  `number` — Monto a invertir

- **`currency` (required)**

  `string`, possible values: `"ARS", "USD"`

- **`price_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`term_id` (required)**

  `number` — ID del plazo de GET /broker/market-data/repos/terms

- **`rate`**

  `number` — Tasa nominal anual (TNA) de la caución. Obligatoria y mayor a 0 si price\_type es limit; con market se ignora

**Example:**

```json
{
  "term_id": 1,
  "currency": "ARS",
  "rate": 1,
  "amount": 1,
  "price_type": "limit"
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`amount` (required)**

  `number` — Monto a invertir

- **`currency` (required)**

  `string`, possible values: `"ARS", "USD"`

- **`price_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`term_id` (required)**

  `number` — ID del plazo de GET /broker/market-data/repos/terms

- **`rate`**

  `number` — Tasa nominal anual (TNA) de la caución. Obligatoria y mayor a 0 si price\_type es limit; con market se ignora

**Example:**

```json
{
  "term_id": 1,
  "currency": "ARS",
  "rate": 1,
  "amount": 1,
  "price_type": "limit"
}
```

##### Content-Type: multipart/form-data

- **`amount` (required)**

  `number` — Monto a invertir

- **`currency` (required)**

  `string`, possible values: `"ARS", "USD"`

- **`price_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`term_id` (required)**

  `number` — ID del plazo de GET /broker/market-data/repos/terms

- **`rate`**

  `number` — Tasa nominal anual (TNA) de la caución. Obligatoria y mayor a 0 si price\_type es limit; con market se ignora

**Example:**

```json
{
  "term_id": 1,
  "currency": "ARS",
  "rate": 1,
  "amount": 1,
  "price_type": "limit"
}
```

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `array`

  **Items:**

  - **`amount` (required)**

    `number` — Monto de la comisión

  - **`commission_currency` (required)**

    `string` — Moneda de la comisión

  - **`commission_type` (required)**

    `string` — Forma de cálculo de la comisión (porcentaje o monto fijo)

  - **`fee_type` (required)**

    `string` — Tipo de cargo (por ejemplo, comisión o derechos de mercado)

  - **`vat_amount` (required)**

    `number` — Monto de IVA

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": [
    {
      "fee_type": "",
      "commission_type": "",
      "commission_currency": "",
      "amount": 1,
      "vat_amount": 1
    }
  ],
  "error": null
}
```

### Crear Caución

- **Method:** `POST`
- **Path:** `/broker/repos`
- **Tags:** Cauciones

Crear una nueva orden de caución (inversión a plazo fijo).

**Requiere header `X-Idempotency-Key`** - Identificador único (UUID) para prevenir órdenes duplicadas por reintentos de red.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `X-Idempotency-Key` required

- **In:** `header`

Identificador único para prevenir duplicados (UUID v4)

`string`, format: `uuid`

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`amount` (required)**

  `number` — Monto a invertir

- **`currency` (required)**

  `string`, possible values: `"ARS", "USD"`

- **`price_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`term_id` (required)**

  `number` — ID del plazo de GET /broker/market-data/repos/terms

- **`rate`**

  `number` — Tasa nominal anual (TNA) de la caución. Obligatoria y mayor a 0 si price\_type es limit; con market se ignora

**Example:**

```json
{
  "term_id": 1,
  "currency": "ARS",
  "rate": 1,
  "amount": 1,
  "price_type": "limit"
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`amount` (required)**

  `number` — Monto a invertir

- **`currency` (required)**

  `string`, possible values: `"ARS", "USD"`

- **`price_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`term_id` (required)**

  `number` — ID del plazo de GET /broker/market-data/repos/terms

- **`rate`**

  `number` — Tasa nominal anual (TNA) de la caución. Obligatoria y mayor a 0 si price\_type es limit; con market se ignora

**Example:**

```json
{
  "term_id": 1,
  "currency": "ARS",
  "rate": 1,
  "amount": 1,
  "price_type": "limit"
}
```

##### Content-Type: multipart/form-data

- **`amount` (required)**

  `number` — Monto a invertir

- **`currency` (required)**

  `string`, possible values: `"ARS", "USD"`

- **`price_type` (required)**

  `string`, possible values: `"limit", "market"`

- **`term_id` (required)**

  `number` — ID del plazo de GET /broker/market-data/repos/terms

- **`rate`**

  `number` — Tasa nominal anual (TNA) de la caución. Obligatoria y mayor a 0 si price\_type es limit; con market se ignora

**Example:**

```json
{
  "term_id": 1,
  "currency": "ARS",
  "rate": 1,
  "amount": 1,
  "price_type": "limit"
}
```

#### Responses

##### Status: 201 Response for status 201

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`order_id` (required)**

    `string` — Identificador único de la orden

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "order_id": ""
  },
  "error": null
}
```

### Cancelar Caución

- **Method:** `DELETE`
- **Path:** `/broker/repos/{order_id}`
- **Tags:** Cauciones

Cancelar una orden de caución existente. Solo se pueden cancelar órdenes pendientes o en progreso.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `order_id` required

- **In:** `path`

`string` — ID de la orden a cancelar

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`cancelled` (required)**

    `boolean` — Si la cancelación fue exitosa

  - **`order_id` (required)**

    `string` — Identificador de la orden

  - **`status` (required)**

    `string` — Nuevo estado de la orden (cancelled)

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "order_id": "",
    "status": "",
    "cancelled": true
  },
  "error": null
}
```

### Suscribirse a un FCI

- **Method:** `POST`
- **Path:** `/broker/mutual-funds/subscriptions`
- **Tags:** FCI

Crear una nueva suscripción (compra de cuotapartes) a un Fondo Común de Inversión por un monto determinado.

**Requiere header `X-Idempotency-Key`** - Identificador único (UUID) para prevenir suscripciones duplicadas por reintentos de red.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `X-Idempotency-Key` required

- **In:** `header`

Identificador único para prevenir duplicados (UUID v4)

`string`, format: `uuid`

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`amount` (required)**

  `number` — Monto a suscribir

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

**Example:**

```json
{
  "symbol": "",
  "amount": 1
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`amount` (required)**

  `number` — Monto a suscribir

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

**Example:**

```json
{
  "symbol": "",
  "amount": 1
}
```

##### Content-Type: multipart/form-data

- **`amount` (required)**

  `number` — Monto a suscribir

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

**Example:**

```json
{
  "symbol": "",
  "amount": 1
}
```

#### Responses

##### Status: 201 Response for status 201

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`messages` (required)**

    `array` — Mensajes informativos, de advertencia o de error

    **Items:**

    - **`code` (required)**

      `string` — Código del mensaje

    - **`message` (required)**

      `string` — Texto del mensaje

  - **`successful` (required)**

    `boolean` — Si la operación fue aceptada

  - **`transaction_id` (required)**

    `string | null` — Identificador de la transacción (null si la operación fue rechazada)

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "transaction_id": null,
    "successful": true,
    "messages": [
      {
        "code": "",
        "message": ""
      }
    ]
  },
  "error": null
}
```

### Validar Suscripción a un FCI

- **Method:** `POST`
- **Path:** `/broker/mutual-funds/subscriptions/validate`
- **Tags:** FCI

Previsualizar una suscripción a un FCI sin ejecutarla. Devuelve si la operación sería válida y los mensajes asociados (montos mínimos, horarios operables, etc.).

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`amount` (required)**

  `number` — Monto a suscribir

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

**Example:**

```json
{
  "symbol": "",
  "amount": 1
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`amount` (required)**

  `number` — Monto a suscribir

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

**Example:**

```json
{
  "symbol": "",
  "amount": 1
}
```

##### Content-Type: multipart/form-data

- **`amount` (required)**

  `number` — Monto a suscribir

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

**Example:**

```json
{
  "symbol": "",
  "amount": 1
}
```

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`messages` (required)**

    `array` — Mensajes de validación

    **Items:**

    - **`code` (required)**

      `string` — Código del mensaje

    - **`message` (required)**

      `string` — Texto del mensaje

  - **`valid` (required)**

    `boolean` — Si la operación pasaría la validación sin errores

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "valid": true,
    "messages": [
      {
        "code": "",
        "message": ""
      }
    ]
  },
  "error": null
}
```

### Rescatar un FCI

- **Method:** `POST`
- **Path:** `/broker/mutual-funds/redemptions`
- **Tags:** FCI

Crear un nuevo rescate (venta de cuotapartes) de un Fondo Común de Inversión por una cantidad de cuotapartes determinada, o usar redeem\_all para rescatar la totalidad de la posición.

**Requiere header `X-Idempotency-Key`** - Identificador único (UUID) para prevenir rescates duplicados por reintentos de red.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `X-Idempotency-Key` required

- **In:** `header`

Identificador único para prevenir duplicados (UUID v4)

`string`, format: `uuid`

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

- **`quantity`**

  `number` — Cantidad de cuotapartes a rescatar. No aplica si redeem\_all es true

- **`redeem_all`**

  `boolean`, default: `false` — Rescatar la totalidad de la posición. Si es true, quantity se ignora.

**Example:**

```json
{
  "symbol": "",
  "quantity": 1,
  "redeem_all": false
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

- **`quantity`**

  `number` — Cantidad de cuotapartes a rescatar. No aplica si redeem\_all es true

- **`redeem_all`**

  `boolean`, default: `false` — Rescatar la totalidad de la posición. Si es true, quantity se ignora.

**Example:**

```json
{
  "symbol": "",
  "quantity": 1,
  "redeem_all": false
}
```

##### Content-Type: multipart/form-data

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

- **`quantity`**

  `number` — Cantidad de cuotapartes a rescatar. No aplica si redeem\_all es true

- **`redeem_all`**

  `boolean`, default: `false` — Rescatar la totalidad de la posición. Si es true, quantity se ignora.

**Example:**

```json
{
  "symbol": "",
  "quantity": 1,
  "redeem_all": false
}
```

#### Responses

##### Status: 201 Response for status 201

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`messages` (required)**

    `array` — Mensajes informativos, de advertencia o de error

    **Items:**

    - **`code` (required)**

      `string` — Código del mensaje

    - **`message` (required)**

      `string` — Texto del mensaje

  - **`successful` (required)**

    `boolean` — Si la operación fue aceptada

  - **`transaction_id` (required)**

    `string | null` — Identificador de la transacción (null si la operación fue rechazada)

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "transaction_id": null,
    "successful": true,
    "messages": [
      {
        "code": "",
        "message": ""
      }
    ]
  },
  "error": null
}
```

### Validar Rescate de un FCI

- **Method:** `POST`
- **Path:** `/broker/mutual-funds/redemptions/validate`
- **Tags:** FCI

Previsualizar un rescate de un FCI sin ejecutarlo. Devuelve si la operación sería válida y los mensajes asociados (plazos de liquidación, montos mínimos, etc.).

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

- **`quantity`**

  `number` — Cantidad de cuotapartes a rescatar. No aplica si redeem\_all es true

- **`redeem_all`**

  `boolean`, default: `false` — Rescatar la totalidad de la posición. Si es true, quantity se ignora.

**Example:**

```json
{
  "symbol": "",
  "quantity": 1,
  "redeem_all": false
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

- **`quantity`**

  `number` — Cantidad de cuotapartes a rescatar. No aplica si redeem\_all es true

- **`redeem_all`**

  `boolean`, default: `false` — Rescatar la totalidad de la posición. Si es true, quantity se ignora.

**Example:**

```json
{
  "symbol": "",
  "quantity": 1,
  "redeem_all": false
}
```

##### Content-Type: multipart/form-data

- **`symbol` (required)**

  `string` — Símbolo del FCI (ej: IOLCAMA)

- **`quantity`**

  `number` — Cantidad de cuotapartes a rescatar. No aplica si redeem\_all es true

- **`redeem_all`**

  `boolean`, default: `false` — Rescatar la totalidad de la posición. Si es true, quantity se ignora.

**Example:**

```json
{
  "symbol": "",
  "quantity": 1,
  "redeem_all": false
}
```

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`messages` (required)**

    `array` — Mensajes de validación

    **Items:**

    - **`code` (required)**

      `string` — Código del mensaje

    - **`message` (required)**

      `string` — Texto del mensaje

  - **`valid` (required)**

    `boolean` — Si la operación pasaría la validación sin errores

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "valid": true,
    "messages": [
      {
        "code": "",
        "message": ""
      }
    ]
  },
  "error": null
}
```

### Cancelar Suscripción o Rescate de FCI

- **Method:** `DELETE`
- **Path:** `/broker/mutual-funds/{transaction_id}`
- **Tags:** FCI

Cancelar una suscripción o un rescate de FCI pendiente. Solo se pueden cancelar operaciones pendientes o en progreso.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `transaction_id` required

- **In:** `path`

`string` — ID de la transacción de suscripción o rescate a cancelar

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`cancelled` (required)**

    `boolean` — Si la cancelación fue exitosa

  - **`status` (required)**

    `string` — Nuevo estado de la transacción (cancelled)

  - **`transaction_id` (required)**

    `string` — Identificador de la transacción

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "transaction_id": "",
    "status": "",
    "cancelled": true
  },
  "error": null
}
```

### Crear Lista de Favoritos

- **Method:** `POST`
- **Path:** `/broker/watchlists`
- **Tags:** Watchlists

Crear una nueva lista de favoritos (watchlist), opcionalmente con uno o más assets ya incluidos.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`name` (required)**

  `string` — Nombre de la lista de favoritos

- **`items`**

  `array` — Assets a agregar al crear la lista

  **Items:**

  - **`market` (required)**

    `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

  - **`symbol` (required)**

    `string` — Símbolo ticker del asset (ej: GGAL, AAPL)

**Example:**

```json
{
  "name": "",
  "items": [
    {
      "symbol": "",
      "market": "BCBA"
    }
  ]
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`name` (required)**

  `string` — Nombre de la lista de favoritos

- **`items`**

  `array` — Assets a agregar al crear la lista

  **Items:**

  - **`market` (required)**

    `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

  - **`symbol` (required)**

    `string` — Símbolo ticker del asset (ej: GGAL, AAPL)

**Example:**

```json
{
  "name": "",
  "items": [
    {
      "symbol": "",
      "market": "BCBA"
    }
  ]
}
```

##### Content-Type: multipart/form-data

- **`name` (required)**

  `string` — Nombre de la lista de favoritos

- **`items`**

  `array` — Assets a agregar al crear la lista

  **Items:**

  - **`market` (required)**

    `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

  - **`symbol` (required)**

    `string` — Símbolo ticker del asset (ej: GGAL, AAPL)

**Example:**

```json
{
  "name": "",
  "items": [
    {
      "symbol": "",
      "market": "BCBA"
    }
  ]
}
```

#### Responses

##### Status: 201 Response for status 201

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`id` (required)**

    `number` — Identificador de la lista de favoritos

  - **`items` (required)**

    `array` — Assets incluidos en la lista, con su última cotización

    **Items:**

    - **`asset_type` (required)**

      `string | null` — Tipo de asset

    - **`market` (required)**

      `string | null` — Mercado donde cotiza el asset

    - **`name` (required)**

      `string | null` — Descripción/nombre del asset

    - **`quote` (required)**

      `object`

      - **`average_price` (required)**

        `number | null`

      - **`best_ask` (required)**

        `number | null`

      - **`best_ask_size` (required)**

        `number | null`

      - **`best_bid` (required)**

        `number | null`

      - **`best_bid_size` (required)**

        `number | null`

      - **`change_percent` (required)**

        `number | null` — Variación porcentual diaria

      - **`currency` (required)**

        `string | null`

      - **`last_price` (required)**

        `number | null`

      - **`last_updated` (required)**

        `string | null`

      - **`traded_amount` (required)**

        `number | null`

      - **`traded_quantity` (required)**

        `number | null`

      - **`volume` (required)**

        `number | null`

    - **`settlement_term` (required)**

      `string | null` — Plazo de liquidación de la cotización

    - **`symbol` (required)**

      `string` — Símbolo ticker del asset

  - **`items_count` (required)**

    `number` — Cantidad de assets en la lista

  - **`name` (required)**

    `string | null` — Nombre de la lista

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "id": 1,
    "name": null,
    "items": [
      {
        "symbol": "",
        "market": null,
        "name": null,
        "settlement_term": null,
        "asset_type": null,
        "quote": {
          "last_price": null,
          "change_percent": null,
          "volume": null,
          "traded_quantity": null,
          "traded_amount": null,
          "average_price": null,
          "best_bid": null,
          "best_ask": null,
          "best_bid_size": null,
          "best_ask_size": null,
          "currency": null,
          "last_updated": null
        }
      }
    ],
    "items_count": 1
  },
  "error": null
}
```

### Obtener Listas de Favoritos

- **Method:** `GET`
- **Path:** `/broker/watchlists`
- **Tags:** Watchlists

Obtener todas las listas de favoritos (watchlists) del cliente, con sus assets asociados.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `array`

  **Items:**

  - **`id` (required)**

    `number` — Identificador de la lista de favoritos

  - **`items` (required)**

    `array` — Assets incluidos en la lista, con su última cotización

    **Items:**

    - **`asset_type` (required)**

      `string | null` — Tipo de asset

    - **`market` (required)**

      `string | null` — Mercado donde cotiza el asset

    - **`name` (required)**

      `string | null` — Descripción/nombre del asset

    - **`quote` (required)**

      `object`

      - **`average_price` (required)**

        `number | null`

      - **`best_ask` (required)**

        `number | null`

      - **`best_ask_size` (required)**

        `number | null`

      - **`best_bid` (required)**

        `number | null`

      - **`best_bid_size` (required)**

        `number | null`

      - **`change_percent` (required)**

        `number | null` — Variación porcentual diaria

      - **`currency` (required)**

        `string | null`

      - **`last_price` (required)**

        `number | null`

      - **`last_updated` (required)**

        `string | null`

      - **`traded_amount` (required)**

        `number | null`

      - **`traded_quantity` (required)**

        `number | null`

      - **`volume` (required)**

        `number | null`

    - **`settlement_term` (required)**

      `string | null` — Plazo de liquidación de la cotización

    - **`symbol` (required)**

      `string` — Símbolo ticker del asset

  - **`items_count` (required)**

    `number` — Cantidad de assets en la lista

  - **`name` (required)**

    `string | null` — Nombre de la lista

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": [
    {
      "id": 1,
      "name": null,
      "items": [
        {
          "symbol": "",
          "market": null,
          "name": null,
          "settlement_term": null,
          "asset_type": null,
          "quote": {
            "last_price": null,
            "change_percent": null,
            "volume": null,
            "traded_quantity": null,
            "traded_amount": null,
            "average_price": null,
            "best_bid": null,
            "best_ask": null,
            "best_bid_size": null,
            "best_ask_size": null,
            "currency": null,
            "last_updated": null
          }
        }
      ],
      "items_count": 1
    }
  ],
  "error": null
}
```

### Obtener Lista de Favoritos

- **Method:** `GET`
- **Path:** `/broker/watchlists/{watchlist_id}`
- **Tags:** Watchlists

Obtener una lista de favoritos en particular por id, con la cotización de sus assets para el plazo indicado.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `watchlist_id` required

- **In:** `path`

**Any of:**

`string`, format: `numeric`, default: `0`

`number` — Identificador de la lista de favoritos

##### `term`

- **In:** `query`

`string`, possible values: `"T0", "T1", "T2"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`id` (required)**

    `number` — Identificador de la lista de favoritos

  - **`items` (required)**

    `array` — Assets incluidos en la lista, con su última cotización

    **Items:**

    - **`asset_type` (required)**

      `string | null` — Tipo de asset

    - **`market` (required)**

      `string | null` — Mercado donde cotiza el asset

    - **`name` (required)**

      `string | null` — Descripción/nombre del asset

    - **`quote` (required)**

      `object`

      - **`average_price` (required)**

        `number | null`

      - **`best_ask` (required)**

        `number | null`

      - **`best_ask_size` (required)**

        `number | null`

      - **`best_bid` (required)**

        `number | null`

      - **`best_bid_size` (required)**

        `number | null`

      - **`change_percent` (required)**

        `number | null` — Variación porcentual diaria

      - **`currency` (required)**

        `string | null`

      - **`last_price` (required)**

        `number | null`

      - **`last_updated` (required)**

        `string | null`

      - **`traded_amount` (required)**

        `number | null`

      - **`traded_quantity` (required)**

        `number | null`

      - **`volume` (required)**

        `number | null`

    - **`settlement_term` (required)**

      `string | null` — Plazo de liquidación de la cotización

    - **`symbol` (required)**

      `string` — Símbolo ticker del asset

  - **`items_count` (required)**

    `number` — Cantidad de assets en la lista

  - **`name` (required)**

    `string | null` — Nombre de la lista

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "id": 1,
    "name": null,
    "items": [
      {
        "symbol": "",
        "market": null,
        "name": null,
        "settlement_term": null,
        "asset_type": null,
        "quote": {
          "last_price": null,
          "change_percent": null,
          "volume": null,
          "traded_quantity": null,
          "traded_amount": null,
          "average_price": null,
          "best_bid": null,
          "best_ask": null,
          "best_bid_size": null,
          "best_ask_size": null,
          "currency": null,
          "last_updated": null
        }
      }
    ],
    "items_count": 1
  },
  "error": null
}
```

### Renombrar Lista de Favoritos

- **Method:** `PUT`
- **Path:** `/broker/watchlists/{watchlist_id}`
- **Tags:** Watchlists

Actualizar el nombre de una lista de favoritos existente.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `watchlist_id` required

- **In:** `path`

**Any of:**

`string`, format: `numeric`, default: `0`

`number` — Identificador de la lista de favoritos

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`name` (required)**

  `string` — Nuevo nombre de la lista

**Example:**

```json
{
  "name": ""
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`name` (required)**

  `string` — Nuevo nombre de la lista

**Example:**

```json
{
  "name": ""
}
```

##### Content-Type: multipart/form-data

- **`name` (required)**

  `string` — Nuevo nombre de la lista

**Example:**

```json
{
  "name": ""
}
```

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`id` (required)**

    `number` — Identificador de la lista de favoritos

  - **`name` (required)**

    `string` — Nombre aplicado

  - **`renamed` (required)**

    `boolean` — Si la actualización fue exitosa

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "id": 1,
    "name": "",
    "renamed": true
  },
  "error": null
}
```

### Eliminar Lista de Favoritos

- **Method:** `DELETE`
- **Path:** `/broker/watchlists/{watchlist_id}`
- **Tags:** Watchlists

Eliminar una lista de favoritos junto con todos sus assets asociados.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `watchlist_id` required

- **In:** `path`

**Any of:**

`string`, format: `numeric`, default: `0`

`number` — Identificador de la lista de favoritos

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`deleted` (required)**

    `boolean` — Si la eliminación fue exitosa

  - **`id` (required)**

    `number` — Identificador de la lista de favoritos

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "id": 1,
    "deleted": true
  },
  "error": null
}
```

### Agregar Asset a Lista de Favoritos

- **Method:** `POST`
- **Path:** `/broker/watchlists/{watchlist_id}/items`
- **Tags:** Watchlists

Agregar un asset a una lista de favoritos existente.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `watchlist_id` required

- **In:** `path`

**Any of:**

`string`, format: `numeric`, default: `0`

`number` — Identificador de la lista de favoritos

#### Request Body

**Required:** true

##### Content-Type: application/json

- **`market` (required)**

  `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

- **`symbol` (required)**

  `string` — Símbolo ticker del asset (ej: GGAL, AAPL)

**Example:**

```json
{
  "symbol": "",
  "market": "BCBA"
}
```

##### Content-Type: application/x-www-form-urlencoded

- **`market` (required)**

  `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

- **`symbol` (required)**

  `string` — Símbolo ticker del asset (ej: GGAL, AAPL)

**Example:**

```json
{
  "symbol": "",
  "market": "BCBA"
}
```

##### Content-Type: multipart/form-data

- **`market` (required)**

  `string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

- **`symbol` (required)**

  `string` — Símbolo ticker del asset (ej: GGAL, AAPL)

**Example:**

```json
{
  "symbol": "",
  "market": "BCBA"
}
```

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`added` (required)**

    `boolean` — Si el asset fue agregado exitosamente

  - **`market` (required)**

    `string` — Mercado del símbolo agregado

  - **`symbol` (required)**

    `string` — Símbolo agregado

  - **`watchlist_id` (required)**

    `number` — Identificador de la lista de favoritos

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "watchlist_id": 1,
    "symbol": "",
    "market": "",
    "added": true
  },
  "error": null
}
```

### Quitar Asset de Lista de Favoritos

- **Method:** `DELETE`
- **Path:** `/broker/watchlists/{watchlist_id}/items/{symbol}`
- **Tags:** Watchlists

Quitar un asset de una lista de favoritos existente.

#### Effective servers

- `https://api.iolinversiones.com`

  Servidor API

#### Authentication

- **bearerAuth**

  ```
  {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "Ingresar el token JWT obtenido de POST /auth/token"
  }
  ```

  Ingresar el token JWT obtenido de POST /auth/token

#### Parameters

##### `watchlist_id` required

- **In:** `path`

**Any of:**

`string`, format: `numeric`, default: `0`

`number` — Identificador de la lista de favoritos

##### `symbol` required

- **In:** `path`

`string` — Símbolo ticker a quitar

##### `market`

- **In:** `query`

`string`, possible values: `"BCBA", "NYSE", "NASDAQ"`

#### Responses

##### Status: 200 Response for status 200

###### Content-Type: application/json

- **`data` (required)**

  `object`

  - **`market` (required)**

    `string | null` — Mercado del símbolo quitado

  - **`removed` (required)**

    `boolean` — Si el asset fue quitado exitosamente

  - **`symbol` (required)**

    `string` — Símbolo quitado

  - **`watchlist_id` (required)**

    `number` — Identificador de la lista de favoritos

- **`error` (required)**

  `null`

- **`meta` (required)**

  `object`

  - **`method` (required)**

    `string` — HTTP method

  - **`path` (required)**

    `string` — Request path

  - **`status_code` (required)**

    `number` — HTTP status code

  - **`timestamp` (required)**

    `string` — ISO 8601 timestamp

  - **`trace_id` (required)**

    `string` — Request trace ID for debugging

**Example:**

```json
{
  "meta": {
    "timestamp": "",
    "path": "",
    "method": "",
    "status_code": 1,
    "trace_id": ""
  },
  "data": {
    "watchlist_id": 1,
    "symbol": "",
    "market": null,
    "removed": true
  },
  "error": null
}
```
