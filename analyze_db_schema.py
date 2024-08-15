import sqlite3
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def analyze_db_schema(db_path):
    logger.info(f"Analyzing schema for database: {db_path}")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    logger.info(f"Found {len(tables)} tables in the database")
    
    schema = []
    fts_tables = set()
    fts_associated_tables = set()

    # First pass: identify FTS tables and their associated tables
    for table_name, table_sql in tables:
        if table_sql:
            lower_sql = table_sql.lower()
            if any(f'using fts{i}' in lower_sql for i in ['', '3', '4', '5']):
                fts_tables.add(table_name)
                logger.info(f"Identified FTS table: {table_name}")
                logger.debug(f"FTS table SQL: {table_sql}")
                
                base_name = table_name.split('_fts')[0]
                for assoc_table in [f"{base_name}_fts_data", f"{base_name}_fts_idx", 
                                    f"{base_name}_fts_content", f"{base_name}_fts_docsize", 
                                    f"{base_name}_fts_config"]:
                    if assoc_table in [t[0] for t in tables]:
                        fts_associated_tables.add(assoc_table)
                        logger.info(f"Identified associated FTS table: {assoc_table}")
            else:
                logger.debug(f"Regular table: {table_name}")
        else:
            logger.warning(f"No SQL found for table: {table_name}")

    logger.info(f"Identified FTS tables: {fts_tables}")
    logger.info(f"Identified associated FTS tables: {fts_associated_tables}")

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
            
            for col in columns:
                col_id, col_name, col_type, not_null, default_value, pk = col
                table_schema['columns'].append({
                    'name': col_name,
                    'type': col_type,
                    'nullable': not not_null,
                    'primary_key': pk == 1
                })
            logger.debug(f"Processed {len(columns)} columns for table {table_name}")
        except sqlite3.OperationalError as e:
            logger.warning(f"Couldn't get column info for table {table_name}: {str(e)}")
        
        schema.append(table_schema)
    
    conn.close()
    logger.info(f"Analyzed schema for {len(schema)} tables")
    return schema

if __name__ == "__main__":
    db_path = "spotify.db"  # Replace with your database path
    schema = analyze_db_schema(db_path)
    
    # Print a summary of the schema
    print("\nSchema Summary:")
    for table in schema:
        print(f"Table: {table['name']}, Is FTS: {table['is_fts']}, Columns: {len(table['columns'])}")