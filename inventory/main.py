from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware 
from redis_om import get_redis_connection, HashModel
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware,
               allow_origins=['http://localhost:3000'],
               allow_methods=['GET', "POST", "PATCH",  "PUT", "DELETE"],
               allow_headers=["*"]
               )

try:
    redis = get_redis_connection(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        password=os.getenv('REDIS_PASSWORD'),
        decode_responses=True
    )
    # Test the connection
    redis.ping()
    print("Successfully connected to Redis")
except Exception as e:
    print(f"Failed to connect to Redis: {str(e)}")
    raise

class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/products")
def all():
    return Product.all_pks()

@app.post("/products")
def create(product: Product):
    return product.save()