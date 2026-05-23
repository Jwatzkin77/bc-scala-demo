import requests
import json

# ─── Config ───────────────────────────────────────────────────────────────────
SCALA_SERVER = "http://localhost:8080"

# ─── Health Check ─────────────────────────────────────────────────────────────
def check_health():
    print("[Python Client] Checking Scala server health...")
    try:
        response = requests.get(f"{SCALA_SERVER}/health")
        data = response.json()
        print(f"[Python Client] Server status: {data['status']}")
        return True
    except Exception as e:
        print(f"[Python Client] Server not reachable: {e}")
        print("[Python Client] Make sure the Scala server is running first.")
        return False

# ─── Fetch Products ───────────────────────────────────────────────────────────
def fetch_products():
    print("[Python Client] Requesting products from Scala server...")
    try:
        response = requests.get(f"{SCALA_SERVER}/products")
        data = response.json()

        products = data.get("data", [])

        if not products:
            print("[Python Client] No products returned.")
            return

        print(f"\n[Python Client] ✅ {len(products)} products returned:\n")
        print(f"{'ID':<8} {'Name':<50} {'Price' :<12} {'Sold':<8} {'SKU'}")
        print("-" * 100)

        for product in products:
            pid   = product.get("id", "N/A")
            name  = product.get("name", "N/A")[:48]
            price = product.get('price', 'N/A')
            sold = product.get("total_sold", "N/A")
            sku   = product.get("sku", "N/A")
            print(f"{pid:<8} {name:<50} ${price:<12} {sold:<8} {sku}")

    except Exception as e:
        print(f"[Python Client] Error: {e}")

# ─── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print(" BC REST API — Python → Scala Proxy Demo")
    print("=" * 70)
    if check_health():
        fetch_products()
