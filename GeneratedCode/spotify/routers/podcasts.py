from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from models import Podcasts, PodcastsCreate
from database import execute_query, execute_insert, execute_update_delete

router = APIRouter(
    prefix="/podcasts",
    tags=["Podcasts"]
)

@router.get("/", response_model=List[Podcasts])
async def get_podcasts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, pattern="^(asc|desc)$")
):
    query = "SELECT * FROM podcasts"
    if sort_by:
        query += f" ORDER BY {sort_by}"
        if order:
            query += f" {order.upper()}"
    query += " LIMIT ? OFFSET ?"
    return execute_query(query, (limit, skip))

@router.get("/{item_id}", response_model=Podcasts)
async def get_podcasts_item(item_id: int):
    query = "SELECT * FROM podcasts WHERE podcast_id = ?"
    result = execute_query(query, (item_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result[0]

@router.post("/", response_model=Podcasts)
async def create_podcasts(item: PodcastsCreate):
    columns = ", ".join(item.dict().keys())
    placeholders = ", ".join("?" * len(item.dict()))
    query = f"INSERT INTO podcasts ({columns}) VALUES ({placeholders})"
    last_id = execute_insert(query, tuple(item.dict().values()))
    return {**item.dict(), "podcast_id": last_id}

@router.put("/{item_id}", response_model=Podcasts)
async def update_podcasts(item_id: int, item: PodcastsCreate):
    set_clause = ", ".join(f"{k} = ?" for k in item.dict().keys())
    query = f"UPDATE podcasts SET {set_clause} WHERE podcast_id = ?"
    values = tuple(item.dict().values()) + (item_id,)
    affected_rows = execute_update_delete(query, values)
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**item.dict(), "podcast_id": item_id}

@router.delete("/{item_id}")
async def delete_podcasts(item_id: int):
    query = "DELETE FROM podcasts WHERE podcast_id = ?"
    affected_rows = execute_update_delete(query, (item_id,))
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}