import sqlite3
import re
from jinja2 import Environment, FileSystemLoader

class CodeGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))

    def get_db_schema(self, db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema = []
        for table in tables:
            table_name = table[0]
            if table_name == 'sqlite_sequence' or table_name.endswith('_fts'):
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
        if sqlite_type == '':
            return 'str'
        elif 'int' in sqlite_type:
            return 'bool' if col_name.lower() in ['isadmin', 'is_admin'] else 'int'
        elif 'char' in sqlite_type or 'clob' in sqlite_type or 'text' in sqlite_type:
            return 'str'
        elif 'real' in sqlite_type or 'floa' in sqlite_type or 'doub' in sqlite_type:
            return 'float'
        elif 'blob' in sqlite_type:
            return 'bytes'
        elif 'boolean' in sqlite_type:
            return 'bool'
        elif 'date' in sqlite_type or 'time' in sqlite_type:
            return 'datetime'
        else:
            print(f"Unknown SQLite type: {sqlite_type}")
            return 'Any'

    def generate_code(self, db_path):
        schema = self.get_db_schema(db_path)
        
        generated_files = {
            'main.py': self.env.get_template('main.py.jinja').render(tables=schema),
            'database.py': self.env.get_template('database.py.jinja').render(db_name=db_path),
            'models.py': self.env.get_template('models.py.jinja').render(tables=schema),
            'routers/__init__.py': '',
        }

        for table in schema:
            router_file = f"routers/{table['name'].lower()}.py"
            generated_files[router_file] = self.env.get_template('router.py.jinja').render(table=table)

        # Apply additional formatting to each file
        for filename, content in generated_files.items():
            generated_files[filename] = content

        return generated_files