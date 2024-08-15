from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from models import Comments, CommentsCreate
from database import execute_query, execute_insert, execute_update_delete

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.get("/", response_model=List[Comments])
async def get_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, pattern="^(asc|desc)$")
):
    query = "SELECT * FROM Comments"
    if sort_by:
        query += f" ORDER BY {sort_by}"
        if order:
            query += f" {order.upper()}"
    query += " LIMIT ? OFFSET ?"
    return execute_query(query, (limit, skip))

@router.get("/{item_id}", response_model=Comments)
async def get_comments_item(item_id: int):
    query = "SELECT * FROM Comments WHERE Id = ?"
    result = execute_query(query, (item_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result[0]

@router.post("/", response_model=Comments)
async def create_comments(item: CommentsCreate):
    columns = ", ".join(item.dict().keys())
    placeholders = ", ".join("?" * len(item.dict()))
    query = f"INSERT INTO Comments ({columns}) VALUES ({placeholders})"
    last_id = execute_insert(query, tuple(item.dict().values()))
    return {**item.dict(), "Id": last_id}

@router.put("/{item_id}", response_model=Comments)
async def update_comments(item_id: int, item: CommentsCreate):
    set_clause = ", ".join(f"{k} = ?" for k in item.dict().keys())
    query = f"UPDATE Comments SET {set_clause} WHERE Id = ?"
    values = tuple(item.dict().values()) + (item_id,)
    affected_rows = execute_update_delete(query, values)
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**item.dict(), "Id": item_id}

@router.delete("/{item_id}")
async def delete_comments(item_id: int):
    query = "DELETE FROM Comments WHERE Id = ?"
    affected_rows = execute_update_delete(query, (item_id,))
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}