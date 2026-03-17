from sqlalchemy import create_engine, inspect, text

_ENGINE_CACHE = {}

def get_engine(db_url: str):
    if db_url not in _ENGINE_CACHE:
        _ENGINE_CACHE[db_url] = create_engine(db_url, pool_pre_ping=True)
    return _ENGINE_CACHE[db_url]

def get_schema(db_url: str) -> str:
    """Extracts schema and Foreign Key relationships for the LLM."""
    engine = get_engine(db_url)
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if not tables:
        return "No tables found."

    schema_lines = []
    for table in tables:
        # Get Columns
        columns = inspector.get_columns(table)
        col_strings = [f"{c['name']} ({str(c['type'])})" for c in columns]

        # Get Foreign Keys
        fks = inspector.get_foreign_keys(table)
        fk_strings = []
        for fk in fks:
            referred_table = fk['referred_table']
            referred_cols = fk['referred_columns']
            constrained_cols = fk['constrained_columns']
            fk_strings.append(f"FK: {constrained_cols} -> {referred_table}({referred_cols})")

        table_def = f"Table: {table}\nColumns: {', '.join(col_strings)}"
        if fk_strings:
            table_def += f"\nRelationships: {', '.join(fk_strings)}"

        schema_lines.append(table_def)

    return "\n\n".join(schema_lines)

def run_query(db_url: str, sql: str):
    engine = get_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        cols = list(result.keys())
    return rows, cols
