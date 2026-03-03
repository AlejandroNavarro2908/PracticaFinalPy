from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from routes import authors, books

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description="API REST para gestionar autores y libros con persistencia en SQLite",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(authors.router)
app.include_router(books.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management API. Visit /docs for documentation."}
