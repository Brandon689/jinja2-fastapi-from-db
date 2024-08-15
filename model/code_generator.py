import sqlite3
import re
from jinja2 import Environment, FileSystemLoader
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CodeGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))

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
        logger.debug(f"Starting code generation for database: {db_path}")
        schema = self.get_db_schema(db_path)
        
        logger.debug(f"Schema extracted: {schema}")
        
        generated_files = {
            'main.py': self.env.get_template('main.py.jinja').render(tables=schema),
            'database.py': self.env.get_template('database.py.jinja').render(db_name=db_path),
            'models.py': self.env.get_template('models.py.jinja').render(tables=schema),
            'routers/__init__.py': '',
        }

        logger.debug("Generated main.py, database.py, and models.py")

        for table in schema:
            logger.debug(f"Generating router for table: {table['name']}")
            logger.debug(f"Table schema: {table}")
            
            router_file = f"routers/{table['name'].lower()}.py"
            generated_files[router_file] = self.env.get_template('router.py.jinja').render(table=table)
            
            logger.debug(f"Generated router file: {router_file}")

        # Apply additional formatting to each file
        for filename, content in generated_files.items():
            logger.debug(f"Formatting file: {filename}")
            generated_files[filename] = content

        logger.debug("Code generation completed")
        return generated_files

    def get_db_schema(self, db_path):
        logger.debug(f"Extracting schema from database: {db_path}")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        logger.debug(f"Found {len(tables)} tables in the database")
        
        schema = []
        fts_tables = set()
        fts_associated_tables = set()

        # First pass: identify FTS tables and their associated tables
        for table_name, table_sql in tables:
            if table_sql:
                lower_sql = table_sql.lower()
                if any(f'using fts{i}' in lower_sql for i in ['', '3', '4', '5']):
                    fts_tables.add(table_name)
                    logger.debug(f"Identified FTS table: {table_name}")
                    logger.debug(f"FTS table SQL: {table_sql}")
                    
                    base_name = table_name.split('_fts')[0]
                    for assoc_table in [f"{base_name}_fts_data", f"{base_name}_fts_idx", 
                                        f"{base_name}_fts_content", f"{base_name}_fts_docsize", 
                                        f"{base_name}_fts_config"]:
                        if assoc_table in [t[0] for t in tables]:
                            fts_associated_tables.add(assoc_table)
                            logger.debug(f"Identified associated FTS table: {assoc_table}")
                else:
                    logger.debug(f"Regular table: {table_name}")
            else:
                logger.warning(f"No SQL found for table: {table_name}")

        logger.debug(f"Identified FTS tables: {fts_tables}")
        logger.debug(f"Identified associated FTS tables: {fts_associated_tables}")

        # Second pass: process all tables
        for table_name, table_sql in tables:
            if (table_name == 'sqlite_sequence' or 
                table_name.startswith('sqlite_') or 
                table_name in fts_associated_tables):
                logger.debug(f"Skipping table: {table_name} (system or FTS-related)")
                continue
            
            is_fts = table_name in fts_tables
            
            table_schema = {
                'name': table_name,
                'is_fts': is_fts,
                'columns': []
            }
            
            logger.debug(f"Processing {'FTS' if is_fts else 'regular'} table: {table_name}")
            
            try:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                primary_key = next((col[1] for col in columns if col[5] == 1), 'id')
                table_schema['primary_key'] = primary_key
                
                for col in columns:
                    col_id, col_name, col_type, not_null, default_value, pk = col
                    py_type = self.map_sqlite_to_python_type(col_type, col_name)
                    table_schema['columns'].append({
                        'name': col_name,
                        'type': col_type,
                        'py_type': py_type,
                        'nullable': not not_null,
                        'primary_key': pk == 1
                    })
                logger.debug(f"Processed {len(columns)} columns for table {table_name}")
            except sqlite3.OperationalError as e:
                logger.warning(f"Couldn't get column info for table {table_name}: {str(e)}")
            
            schema.append(table_schema)
        
        conn.close()
        logger.debug(f"Extracted schema for {len(schema)} tables")
        return schema
