import strawberry
from typing import List
import uvicorn
from strawberry.asgi import GraphQL
from starlette.middleware.cors import CORSMiddleware

# --- TYPE ---
@strawberry.type
class Product:
    id: int
    name: str
    price: float
    sku: str
    latin: str
    port: str
    ital: str
    esp: str

# --- RESOLVER DATA ---
def get_products() -> List[Product]:
    return [
        Product(id=1,  name="Alpha",   price=0.52,  latin="unus",    port="um",      ital="uno",    esp="uno",    sku="70005"),
        Product(id=2,  name="Bravo",   price=9.99,  latin="duo",     port="dois",    ital="due",    esp="dos",    sku="70006"),
        Product(id=3,  name="Charlie", price=14.99, latin="tres",    port="três",    ital="tre",    esp="tres",   sku="70007"),
        Product(id=4,  name="Delta",   price=4.99,  latin="quattuor",port="quatro",  ital="quattro",esp="cuatro", sku="70008"),
        Product(id=5,  name="Echo",    price=5.99,  latin="quinque", port="cinco",   ital="cinque", esp="cinco",  sku="70009"),
        Product(id=6,  name="Foxtrot", price=6.99,  latin="sex",     port="seis",    ital="sei",    esp="seis",   sku="70010"),
        Product(id=7,  name="Golf",    price=7.99,  latin="septem",  port="sete",    ital="sette",  esp="siete",  sku="70011"),
        Product(id=8,  name="Hotel",   price=8.99,  latin="octo",    port="oito",    ital="otto",   esp="ocho",   sku="70012"),
        Product(id=9,  name="India",   price=9.49,  latin="novem",   port="nove",    ital="nove",   esp="nueve",  sku="70013"),
        Product(id=10, name="Juliet",  price=10.99, latin="decem",   port="dez",     ital="dieci",  esp="diez",   sku="70014"),
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
app = CORSMiddleware(
    app,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
