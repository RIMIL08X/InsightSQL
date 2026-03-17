import re

FORBIDDEN_KEYWORDS = {
    "insert", "update", "delete",
    "drop", "alter", "truncate",
    "create", "grant", "revoke",
    "replace", "merge"
}

MAX_LIMIT = 1000


def normalize_sql(sql: str) -> str:
    """Normalize SQL by removing comments and standardizing whitespace."""

    # remove inline comments
    sql = re.sub(r"--.*?$", "", sql, flags=re.MULTILINE)

    # remove block comments
    sql = re.sub(r"/\*.*?\*/", "", sql, flags=re.DOTALL)

    # normalize whitespace
    sql = re.sub(r"\s+", " ", sql)

    return sql.strip().lower()


def contains_forbidden_keywords(sql: str) -> bool:
    """Detect destructive SQL keywords."""
    for keyword in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{keyword}\b", sql):
            return True
    return False


def contains_multiple_statements(sql: str) -> bool:
    """Prevent stacked queries."""
    statements = [s for s in sql.split(";") if s.strip()]
    return len(statements) > 1


def starts_with_select(sql: str) -> bool:
    """Allow SELECT or WITH (CTE) queries."""
    return bool(re.match(r"^(select|with)\b", sql))


def enforce_limit(sql: str) -> str:
    """Ensure query has a LIMIT."""
    if "limit" not in sql:
        sql = sql.rstrip(";") + f" LIMIT {MAX_LIMIT}"
    return sql


def contains_suspicious_patterns(sql: str) -> bool:
    """Block common SQL injection tricks."""

    suspicious_patterns = [
        r"union\s+select",   # UNION injection
        r"sleep\s*\(",      # time-based injection
        r"benchmark\s*\(",
        r"pg_sleep\s*\(",
        r"information_schema",
        r"pg_catalog",
        r"sys\.",
    ]

    for pattern in suspicious_patterns:
        if re.search(pattern, sql):
            return True

    return False


def is_safe_sql(sql: str) -> bool:
    sql_clean = normalize_sql(sql)

    if not starts_with_select(sql_clean):
        return False

    if contains_multiple_statements(sql_clean):
        return False

    if contains_forbidden_keywords(sql_clean):
        return False

    if contains_suspicious_patterns(sql_clean):
        return False

    return True


def sanitize_sql(sql: str) -> str:
    """Validate and return safe SQL."""

    sql_clean = normalize_sql(sql)

    if not is_safe_sql(sql_clean):
        raise ValueError("Unsafe SQL detected")

    sql_clean = enforce_limit(sql_clean)

    return sql_clean
