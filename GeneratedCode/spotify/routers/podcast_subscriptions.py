from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from models import Podcast_subscriptions, Podcast_subscriptionsCreate
from database import execute_query, execute_insert, execute_update_delete

router = APIRouter(
    prefix="/podcast_subscriptions",
    tags=["Podcast_subscriptions"]
)

@router.get("/", response_model=List[Podcast_subscriptions])
async def get_podcast_subscriptions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, pattern="^(asc|desc)$")
):
    query = "SELECT * FROM podcast_subscriptions"
    if sort_by:
        query += f" ORDER BY {sort_by}"
        if order:
            query += f" {order.upper()}"
    query += " LIMIT ? OFFSET ?"
    return execute_query(query, (limit, skip))

@router.get("/{item_id}", response_model=Podcast_subscriptions)
async def get_podcast_subscriptions_item(item_id: int):
    query = "SELECT * FROM podcast_subscriptions WHERE user_id = ?"
    result = execute_query(query, (item_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result[0]

@router.post("/", response_model=Podcast_subscriptions)
async def create_podcast_subscriptions(item: Podcast_subscriptionsCreate):
    columns = ", ".join(item.dict().keys())
    placeholders = ", ".join("?" * len(item.dict()))
    query = f"INSERT INTO podcast_subscriptions ({columns}) VALUES ({placeholders})"
    last_id = execute_insert(query, tuple(item.dict().values()))
    return {**item.dict(), "user_id": last_id}

@router.put("/{item_id}", response_model=Podcast_subscriptions)
async def update_podcast_subscriptions(item_id: int, item: Podcast_subscriptionsCreate):
    set_clause = ", ".join(f"{k} = ?" for k in item.dict().keys())
    query = f"UPDATE podcast_subscriptions SET {set_clause} WHERE user_id = ?"
    values = tuple(item.dict().values()) + (item_id,)
    affected_rows = execute_update_delete(query, values)
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**item.dict(), "user_id": item_id}

@router.delete("/{item_id}")
async def delete_podcast_subscriptions(item_id: int):
    query = "DELETE FROM podcast_subscriptions WHERE user_id = ?"
    affected_rows = execute_update_delete(query, (item_id,))
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}