import java.net.{InetSocketAddress, HttpURLConnection, URL}
import com.sun.net.httpserver.{HttpServer, HttpExchange}
import scala.io.Source

// Load from config.sc — DO NOT commit config.sc
val STORE_HASH = sys.env.getOrElse("BC_STORE_HASH", "")
val AUTH_TOKEN = sys.env.getOrElse("BC_AUTH_TOKEN", "")
val BC_API_URL = s"https://api.bigcommerce.com/stores/$STORE_HASH/v3/catalog/products?limit=50&sort=total_sold&direction=desc"

def callBC(): String =
  try
    val url = URL(BC_API_URL)
    val conn = url.openConnection().asInstanceOf[HttpURLConnection]
    conn.setRequestMethod("GET")
    conn.setRequestProperty("X-Auth-Token", AUTH_TOKEN)
    conn.setRequestProperty("Accept", "application/json")
    val status = conn.getResponseCode
    println(s"[Scala Server] BC API status: $status")
    if status == 200 then
      Source.fromInputStream(conn.getInputStream).mkString
    else
      val error = Source.fromInputStream(conn.getErrorStream).mkString
      println(s"[Scala Server] BC API error body: $error")
      s"""{"error": "BC API returned $status", "detail": "$error"}"""
  catch
    case e: Exception =>
      println(s"[Scala Server] Exception calling BC API: ${e.getMessage}")
      s"""{"error": "${e.getMessage}"}"""

val server = HttpServer.create(InetSocketAddress(8080), 0)

server.createContext("/products", (exchange: HttpExchange) => {
  println("[Scala Server] GET /products")
  val body = callBC()
  val bytes = body.getBytes("UTF-8")
  exchange.getResponseHeaders.set("Content-Type", "application/json")
  exchange.sendResponseHeaders(200, bytes.length)
  exchange.getResponseBody.write(bytes)
  exchange.getResponseBody.close()
})

server.createContext("/health", (exchange: HttpExchange) => {
  val body = """{"status":"ok"}"""
  val bytes = body.getBytes("UTF-8")
  exchange.getResponseHeaders.set("Content-Type", "application/json")
  exchange.sendResponseHeaders(200, bytes.length)
  exchange.getResponseBody.write(bytes)
  exchange.getResponseBody.close()
})

server.start()
println("[Scala Server] Running on http://localhost:8080")
println("[Scala Server] Press Ctrl+C to stop")
Thread.currentThread().join()
