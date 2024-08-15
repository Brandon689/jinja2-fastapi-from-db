from fastapi import FastAPI
from database import DB_NAME
from routers import users
from routers import categories
from routers import posts
from routers import comments

app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(posts.router)
app.include_router(comments.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)