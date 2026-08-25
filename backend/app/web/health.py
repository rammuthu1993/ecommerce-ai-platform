import time
from app.database.connection import get_connection
from app.web.response import Response

START_TIME = time.time()

def health_check_handler(request):
    db_status = "healthy"
    try:
        conn = get_connection()
        conn.execute("SELECT 1").fetchone()
        conn.close()
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    uptime_seconds = int(time.time() - START_TIME)
    health_data = {
        "status": "UP" if db_status == "healthy" else "DEGRADED",
        "database": db_status,
        "uptime_seconds": uptime_seconds,
        "timestamp": int(time.time())
    }
    status_code = 200 if db_status == "healthy" else 503
    return Response(data=health_data, status_code=status_code)
