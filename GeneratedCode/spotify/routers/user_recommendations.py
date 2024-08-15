from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from models import User_recommendations, User_recommendationsCreate
from database import execute_query, execute_insert, execute_update_delete

router = APIRouter(
    prefix="/user_recommendations",
    tags=["User_recommendations"]
)

@router.get("/", response_model=List[User_recommendations])
async def get_user_recommendations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, pattern="^(asc|desc)$")
):
    query = "SELECT * FROM user_recommendations"
    if sort_by:
        query += f" ORDER BY {sort_by}"
        if order:
            query += f" {order.upper()}"
    query += " LIMIT ? OFFSET ?"
    return execute_query(query, (limit, skip))

@router.get("/{item_id}", response_model=User_recommendations)
async def get_user_recommendations_item(item_id: int):
    query = "SELECT * FROM user_recommendations WHERE recommendation_id = ?"
    result = execute_query(query, (item_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result[0]

@router.post("/", response_model=User_recommendations)
async def create_user_recommendations(item: User_recommendationsCreate):
    columns = ", ".join(item.dict().keys())
    placeholders = ", ".join("?" * len(item.dict()))
    query = f"INSERT INTO user_recommendations ({columns}) VALUES ({placeholders})"
    last_id = execute_insert(query, tuple(item.dict().values()))
    return {**item.dict(), "recommendation_id": last_id}

@router.put("/{item_id}", response_model=User_recommendations)
async def update_user_recommendations(item_id: int, item: User_recommendationsCreate):
    set_clause = ", ".join(f"{k} = ?" for k in item.dict().keys())
    query = f"UPDATE user_recommendations SET {set_clause} WHERE recommendation_id = ?"
    values = tuple(item.dict().values()) + (item_id,)
    affected_rows = execute_update_delete(query, values)
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**item.dict(), "recommendation_id": item_id}

@router.delete("/{item_id}")
async def delete_user_recommendations(item_id: int):
    query = "DELETE FROM user_recommendations WHERE recommendation_id = ?"
    affected_rows = execute_update_delete(query, (item_id,))
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}