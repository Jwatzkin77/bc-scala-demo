import strawberry
from typing import List
import uvicorn
from strawberry.asgi import GraphQL

# --- TYPE ---
@strawberry.type
class Product:
    id: int
    name: str
    price: float
    sku: str

# --- RESOLVER DATA ---
def get_products() -> List[Product]:
    return [
        Product(id=1, name="Bravo", price=0.52, sku="70005"),
        Product(id=2, name="Alpha", price=9.99, sku="70006"),
        Product(id=3, name="Charlie", price=14.99, sku="70007"),
    ]

# --- SCHEMA ---
@strawberry.type
class Query:
    products: List[Product] = strawberry.field(resolver=get_products)

    @strawberry.field
    def product(self, id: int) -> Product:
        all_products = get_products()
        for p in all_products:
            if p.id == id:
                return p
        raise ValueError(f"Product with id {id} not found")

schema = strawberry.Schema(query=Query)
app = GraphQL(schema)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)