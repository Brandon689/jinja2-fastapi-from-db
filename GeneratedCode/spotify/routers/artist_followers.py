from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from models import Artist_followers, Artist_followersCreate
from database import execute_query, execute_insert, execute_update_delete

router = APIRouter(
    prefix="/artist_followers",
    tags=["Artist_followers"]
)

@router.get("/", response_model=List[Artist_followers])
async def get_artist_followers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, pattern="^(asc|desc)$")
):
    query = "SELECT * FROM artist_followers"
    if sort_by:
        query += f" ORDER BY {sort_by}"
        if order:
            query += f" {order.upper()}"
    query += " LIMIT ? OFFSET ?"
    return execute_query(query, (limit, skip))

@router.get("/{item_id}", response_model=Artist_followers)
async def get_artist_followers_item(item_id: int):
    query = "SELECT * FROM artist_followers WHERE user_id = ?"
    result = execute_query(query, (item_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result[0]

@router.post("/", response_model=Artist_followers)
async def create_artist_followers(item: Artist_followersCreate):
    columns = ", ".join(item.dict().keys())
    placeholders = ", ".join("?" * len(item.dict()))
    query = f"INSERT INTO artist_followers ({columns}) VALUES ({placeholders})"
    last_id = execute_insert(query, tuple(item.dict().values()))
    return {**item.dict(), "user_id": last_id}

@router.put("/{item_id}", response_model=Artist_followers)
async def update_artist_followers(item_id: int, item: Artist_followersCreate):
    set_clause = ", ".join(f"{k} = ?" for k in item.dict().keys())
    query = f"UPDATE artist_followers SET {set_clause} WHERE user_id = ?"
    values = tuple(item.dict().values()) + (item_id,)
    affected_rows = execute_update_delete(query, values)
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**item.dict(), "user_id": item_id}

@router.delete("/{item_id}")
async def delete_artist_followers(item_id: int):
    query = "DELETE FROM artist_followers WHERE user_id = ?"
    affected_rows = execute_update_delete(query, (item_id,))
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}