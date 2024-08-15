from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from models import Song_fts_config, Song_fts_configCreate
from database import execute_query, execute_insert, execute_update_delete

router = APIRouter(
    prefix="/song_fts_config",
    tags=["Song_fts_config"]
)

@router.get("/", response_model=List[Song_fts_config])
async def get_song_fts_config(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, pattern="^(asc|desc)$")
):
    query = "SELECT * FROM song_fts_config"
    if sort_by:
        query += f" ORDER BY {sort_by}"
        if order:
            query += f" {order.upper()}"
    query += " LIMIT ? OFFSET ?"
    return execute_query(query, (limit, skip))

@router.get("/{item_id}", response_model=Song_fts_config)
async def get_song_fts_config_item(item_id: int):
    query = "SELECT * FROM song_fts_config WHERE k = ?"
    result = execute_query(query, (item_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result[0]

@router.post("/", response_model=Song_fts_config)
async def create_song_fts_config(item: Song_fts_configCreate):
    columns = ", ".join(item.dict().keys())
    placeholders = ", ".join("?" * len(item.dict()))
    query = f"INSERT INTO song_fts_config ({columns}) VALUES ({placeholders})"
    last_id = execute_insert(query, tuple(item.dict().values()))
    return {**item.dict(), "k": last_id}

@router.put("/{item_id}", response_model=Song_fts_config)
async def update_song_fts_config(item_id: int, item: Song_fts_configCreate):
    set_clause = ", ".join(f"{k} = ?" for k in item.dict().keys())
    query = f"UPDATE song_fts_config SET {set_clause} WHERE k = ?"
    values = tuple(item.dict().values()) + (item_id,)
    affected_rows = execute_update_delete(query, values)
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**item.dict(), "k": item_id}

@router.delete("/{item_id}")
async def delete_song_fts_config(item_id: int):
    query = "DELETE FROM song_fts_config WHERE k = ?"
    affected_rows = execute_update_delete(query, (item_id,))
    if affected_rows == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}