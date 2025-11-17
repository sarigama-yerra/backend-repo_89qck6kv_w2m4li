import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any

app = FastAPI(title="SaaS HR Platform API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health/root
@app.get("/")
def read_root():
    return {"message": "SaaS HR API is running"}

# Basic hello
@app.get("/api/hello")
def hello():
    return {"message": "Hello from the HR backend API!"}

# Database connectivity test
@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response: Dict[str, Any] = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        from database import db

        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Check environment variables
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Expose schemas for the low-code DB viewer
@app.get("/schema")
def get_schemas():
    import inspect
    import schemas as app_schemas
    from pydantic import BaseModel as _BaseModel

    schema_defs = {}
    for name, obj in inspect.getmembers(app_schemas):
        if inspect.isclass(obj) and issubclass(obj, _BaseModel) and obj is not _BaseModel:
            # collection name is lowercase of class name
            collection = name.lower()
            schema_defs[collection] = obj.model_json_schema()

    return {"schemas": schema_defs}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
