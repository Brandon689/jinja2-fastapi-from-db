import os
from jinja2 import Environment, FileSystemLoader

class CodeGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))
        self.template_string = """
import sqlite3
from fastapi import FastAPI, HTTPException, Query, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

DB_NAME = "{{ db_name }}"

def execute_query(query: str, params: tuple = ()) -> List[dict]:
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = [dict(row) for row in cursor.fetchall()]
    conn.commit()
    conn.close()
    return result

{% for table in tables %}
class {{ table.name | capitalize }}Base(BaseModel):
    {% for column in table.columns %}{% if column.name != table.primary_key %}{{ column.name }}: {{ column.py_type }}{% if column.nullable %} = None{% endif %}
    {% endif %}{% endfor %}

class {{ table.name | capitalize }}Create({{ table.name | capitalize }}Base):
    pass

class {{ table.name | capitalize }}({{ table.name | capitalize }}Base):
    {{ table.primary_key }}: int

@app.get("/{{ table.name | lower }}", response_model=List[{{ table.name | capitalize }}])
async def get_{{ table.name | lower }}(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    sort_by: Optional[str] = None,
    order: Optional[str] = Query(None, pattern="^(asc|desc)$")
):
    query = "SELECT * FROM {{ table.name }}"
    if sort_by:
        query += f" ORDER BY {sort_by}"
        if order:
            query += f" {order.upper()}"
    query += " LIMIT ? OFFSET ?"
    return execute_query(query, (limit, skip))

@app.get("/{{ table.name | lower }}/{item_id}", response_model={{ table.name | capitalize }})
async def get_{{ table.name | lower }}_item(item_id: int):
    query = "SELECT * FROM {{ table.name }} WHERE {{ table.primary_key }} = ?"
    result = execute_query(query, (item_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result[0]

@app.post("/{{ table.name | lower }}", response_model={{ table.name | capitalize }})
async def create_{{ table.name | lower }}(item: {{ table.name | capitalize }}Create):
    columns = ", ".join(item.dict().keys())
    placeholders = ", ".join("?" * len(item.dict()))
    query = f"INSERT INTO {{ table.name }} ({columns}) VALUES ({placeholders})"
    execute_query(query, tuple(item.dict().values()))
    return {**item.dict(), "{{ table.primary_key }}": execute_query("SELECT last_insert_rowid()")[0]['last_insert_rowid()']}

@app.put("/{{ table.name | lower }}/{item_id}", response_model={{ table.name | capitalize }})
async def update_{{ table.name | lower }}(item_id: int, item: {{ table.name | capitalize }}Create):
    set_clause = ", ".join(f"{k} = ?" for k in item.dict().keys())
    query = f"UPDATE {{ table.name }} SET {set_clause} WHERE {{ table.primary_key }} = ?"
    values = tuple(item.dict().values()) + (item_id,)
    execute_query(query, values)
    return {**item.dict(), "{{ table.primary_key }}": item_id}

@app.delete("/{{ table.name | lower }}/{item_id}")
async def delete_{{ table.name | lower }}(item_id: int):
    query = "DELETE FROM {{ table.name }} WHERE {{ table.primary_key }} = ?"
    execute_query(query, (item_id,))
    return {"message": "Item deleted successfully"}
{% endfor %}"""
        self.template = Template(self.template_string)

    def get_db_schema(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema = []
        for table in tables:
            table_name = table[0]
            if table_name == 'sqlite_sequence':
                continue  # Skip this system table
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            primary_key = next((col[1] for col in columns if col[5] == 1), 'id')
            
            table_schema = {
                'name': table_name,
                'columns': [],
                'primary_key': primary_key
            }
            
            for col in columns:
                col_id, col_name, col_type, not_null, _, _ = col
                py_type = self.map_sqlite_to_python_type(col_type, col_name)
                table_schema['columns'].append({
                    'name': col_name,
                    'type': col_type,
                    'py_type': py_type,
                    'nullable': not not_null
                })
            
            schema.append(table_schema)
        
        conn.close()
        return schema

    def map_sqlite_to_python_type(self, sqlite_type, col_name):
        sqlite_type = sqlite_type.lower()
        if 'int' in sqlite_type:
            return 'bool' if col_name.lower() in ['isadmin', 'is_admin'] else 'int'
        elif 'char' in sqlite_type or 'clob' in sqlite_type or 'text' in sqlite_type:
            return 'datetime' if 'date' in col_name.lower() or 'time' in col_name.lower() else 'str'
        elif 'real' in sqlite_type or 'floa' in sqlite_type or 'doub' in sqlite_type:
            return 'float'
        elif 'blob' in sqlite_type:
            return 'bytes'
        elif 'boolean' in sqlite_type:
            return 'bool'
        else:
            print(f"Unknown SQLite type: {sqlite_type}")
            return 'Any'

    def generate_code(self, db_path):
        schema = self.get_db_schema(db_path)
        
        generated_files = {
            'main.py': self.env.get_template('main.py.jinja').render(db_name=db_path),
            'database.py': self.env.get_template('database.py.jinja').render(db_name=db_path),
            'models.py': self.env.get_template('models.py.jinja').render(tables=schema),
            'routers/__init__.py': '',
        }

        for table in schema:
            router_file = f"routers/{table['name'].lower()}.py"
            generated_files[router_file] = self.env.get_template('router.py.jinja').render(table=table)

        return generated_files