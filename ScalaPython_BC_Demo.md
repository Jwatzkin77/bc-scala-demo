# BC REST API — Python → Scala Proxy Demo
**Location:** `~/Desktop/bc-scala-demo/`  
**Files:** `fetch_products.sc` (Scala server) + `client.py` (Python client)  
**Status:** ✅ Working — confirmed output May 2026

---

## What This Program Does

```
Python client → Scala HTTP server (localhost:8080) → BigCommerce REST API
```

1. **Scala** starts a lightweight HTTP server on `localhost:8080` using Java's built-in `HttpServer`
2. **Python** sends a GET request to `localhost:8080/products`
3. **Scala** receives it, forwards the request to the BC REST API with the auth token
4. **BC API** returns a JSON list of products
5. **Scala** passes the response back to Python
6. **Python** formats and prints the product table to the terminal

---

## How to Run

**Terminal 1 — Start Scala server:**
```bash
cd ~/Desktop/bc-scala-demo
scala-cli run fetch_products.sc
```
Leave running. You should see:
```
[Scala Server] Running on http://localhost:8080
[Scala Server] Press Ctrl+C to stop
```

**Terminal 2 — Run Python client:**
```bash
cd ~/Desktop/bc-scala-demo
python3 client.py
```

---

## fetch_products.sc — Scala Server

### Imports
```scala
import java.net.{InetSocketAddress, HttpURLConnection, URL}
import com.sun.net.httpserver.{HttpServer, HttpExchange}
import scala.io.Source
```
- `InetSocketAddress` — binds the server to a port
- `HttpURLConnection` — makes outbound HTTP requests to BC API
- `HttpServer` — Java's built-in lightweight HTTP server
- `HttpExchange` — represents an incoming request/response pair
- `Source` — reads the BC API response stream into a String

---

### Config
```scala
val STORE_HASH = "c2f9eeasqw"
val AUTH_TOKEN = "YOUR_AUTH_TOKEN_HERE"
val BC_API_URL = s"https://api.bigcommerce.com/stores/$STORE_HASH/v3/catalog/products?limit=10"
```
- `val` — immutable value (Scala equivalent of a constant)
- `s"..."` — string interpolation, `$STORE_HASH` is substituted at runtime
- `limit=10` — returns first 10 products from the BC catalog

---

### callBC() Function
```scala
def callBC(): String =
  val url = URL(BC_API_URL)
  val conn = url.openConnection().asInstanceOf[HttpURLConnection]
  conn.setRequestMethod("GET")
  conn.setRequestProperty("X-Auth-Token", AUTH_TOKEN)
  conn.setRequestProperty("Accept", "application/json")
  Source.fromInputStream(conn.getInputStream).mkString
```
- `def` — defines a function
- `: String` — return type annotation
- `asInstanceOf[HttpURLConnection]` — Scala type cast
- `setRequestProperty` — sets HTTP headers (equivalent to `-H` in curl)
- `Source.fromInputStream(...).mkString` — reads the full response body as a String

---

### HTTP Server Setup
```scala
val server = HttpServer.create(InetSocketAddress(8080), 0)
```
- Creates a server bound to port `8080`
- Second argument `0` = default backlog (connection queue size)

---

### /products Route
```scala
server.createContext("/products", (exchange: HttpExchange) => {
  println("[Scala Server] GET /products")
  val body = callBC()
  val bytes = body.getBytes("UTF-8")
  exchange.getResponseHeaders.set("Content-Type", "application/json")
  exchange.sendResponseHeaders(200, bytes.length)
  exchange.getResponseBody.write(bytes)
  exchange.getResponseBody.close()
})
```
- `createContext` — registers a route handler (equivalent to `@app.route` in Flask)
- `exchange` — the incoming HTTP request and outgoing response object
- `callBC()` — calls the BC REST API and returns JSON string
- `getBytes("UTF-8")` — converts String to byte array for HTTP response
- `sendResponseHeaders(200, bytes.length)` — sends status code + content length
- `write` / `close` — writes the body and closes the connection

---

### /health Route
```scala
server.createContext("/health", (exchange: HttpExchange) => {
  val body = """{"status":"ok"}"""
  ...
})
```
- Simple health check endpoint
- `"""..."""` — triple-quoted string literal in Scala (no escaping needed)

---

### Server Start
```scala
server.start()
println("[Scala Server] Running on http://localhost:8080")
Thread.currentThread().join()
```
- `server.start()` — starts accepting connections
- `Thread.currentThread().join()` — **keeps the process alive** indefinitely
- Without this line the script would compile, start, and immediately exit

---

## client.py — Python Client

### Health Check
```python
response = requests.get(f"{SCALA_SERVER}/health")
```
- Hits the `/health` endpoint on the Scala server before requesting data
- Confirms the server is running before proceeding

### Product Fetch
```python
response = requests.get(f"{SCALA_SERVER}/products")
data = response.json()
products = data.get("data", [])
```
- Calls `/products` on the Scala server
- Scala proxies this to BC and returns the full JSON response
- `data.get("data", [])` — BC v3 API wraps results in a `data` key

### Output Table
```python
print(f"{'ID':<8} {'Name':<50} {'Price'}")
for product in products:
    pid   = product.get("id", "N/A")
    name  = product.get("name", "N/A")[:48]
    price = product.get("price", "N/A")
    print(f"{pid:<8} {name:<50} ${price}")
```
- `:<8` — left-align with minimum width of 8 characters
- `[:48]` — truncates name to 48 characters to fit the column
- f-string formatting for clean tabular output

---

## Confirmed Output
```
ID       Name                                               Price
----------------------------------------------------------------------
25110    Tax product display test                           $5
25111    Amani Upholstered Side Chair                       $0
25112    Amani Sofa Table                                   $0
...
```

---

## Key Concepts Demonstrated

| Concept | Scala | Python |
|---------|-------|--------|
| HTTP server | `HttpServer.create()` | N/A (client only) |
| HTTP client | `HttpURLConnection` | `requests.get()` |
| String interpolation | `s"$variable"` | `f"{variable}"` |
| Immutable values | `val` | N/A (`=` assignment) |
| Type annotation | `: String` | type hints (optional) |
| Route handler | `createContext("/path", handler)` | `@app.route("/path")` in Flask |
| Keep process alive | `Thread.currentThread().join()` | N/A |
