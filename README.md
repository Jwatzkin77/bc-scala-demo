# bc-scala-demo

A lightweight demo project showing how to proxy BigCommerce REST API requests through a Scala HTTP server and consume the results with a Python client.

```
Python client → Scala HTTP server (localhost:8080) → BigCommerce REST API
```

---

## What It Does

1. **Scala** starts a lightweight HTTP server on `localhost:8080` using Java's built-in `HttpServer`
2. **Python** sends a GET request to `localhost:8080/products`
3. **Scala** forwards the request to the BigCommerce V3 Catalog API with your auth token
4. **BC API** returns a JSON list of products sorted by total sold
5. **Python** formats and prints the product table to the terminal

---

## Prerequisites

| Tool | Install |
|------|---------|
| Scala CLI | `brew install scala-cli` |
| Python 3 | Pre-installed on macOS |
| requests (Python) | `pip3 install requests` |

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Jwatzkin77/bc-scala-demo.git
cd bc-scala-demo
```

### 2. Set environment variables

The server reads your BigCommerce credentials from environment variables — never hardcoded.

```bash
export BC_STORE_HASH="your_store_hash_here"
export BC_AUTH_TOKEN="your_auth_token_here"
```

To persist across sessions, add both lines to `~/.zshrc` and run `source ~/.zshrc`.

To generate a BC API token, go to **BigCommerce Control Panel → Settings → API Accounts → Create API Account**. The token requires `Products` read scope.

---

## Running the Demo

### Terminal 1 — Start the Scala server

```bash
scala-cli run fetch_products.sc
```

On first run, Scala CLI will download dependencies (~30 seconds). Wait for:

```
[Scala Server] Running on http://localhost:8080
[Scala Server] Press Ctrl+C to stop
```

### Terminal 2 — Run the Python client

```bash
python3 client.py
```

### Expected output

```
======================================================================
 BC REST API — Python → Scala Proxy Demo
======================================================================
[Python Client] Checking Scala server health...
[Python Client] Server status: ok
[Python Client] Requesting products from Scala server...

[Python Client] ✅ 10 products returned:

ID       Name                                               Price        Sold     SKU
-----------------------------------------------------------------------------------------------------
25110    Tax product display test                           $5           0        TAX-001
25111    Amani Upholstered Side Chair                       $0           0        AMANI-001
...
```

---

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check — returns `{"status":"ok"}` |
| `/products` | GET | Proxies to BC V3 Catalog API and returns product list |

---

## Project Structure

```
bc-scala-demo/
├── fetch_products.sc     # Scala HTTP server — proxies requests to BC API
├── client.py             # Python client — calls Scala server and formats output
├── ScalaPython_BC_Demo.md # Line-by-line code breakdown and reference
└── .gitignore
```

---

## Key Concepts

| Concept | Scala | Python |
|---------|-------|--------|
| HTTP server | `HttpServer.create()` | N/A (client only) |
| HTTP client | `HttpURLConnection` | `requests.get()` |
| String interpolation | `s"$variable"` | `f"{variable}"` |
| Immutable values | `val` | `=` assignment |
| Keep process alive | `Thread.currentThread().join()` | N/A |
| Environment variables | `sys.env.getOrElse(...)` | `os.environ.get(...)` |

---

## Security

- Credentials are read from environment variables — never committed to the repo
- Add `BC_STORE_HASH` and `BC_AUTH_TOKEN` to your shell environment before running
- Never commit a `config.sc` or `.env` file containing real credentials

---

## Built With

- [Scala CLI](https://scala-cli.virtuslab.org/) — `1.14.0`
- Scala `3.8.3`
- Python `3.x`
- [BigCommerce V3 Catalog API](https://docs.bigcommerce.com/developer/api-reference/rest/admin/catalog/products)
