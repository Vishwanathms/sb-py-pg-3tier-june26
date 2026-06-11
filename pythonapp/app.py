import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer

import psycopg2
from psycopg2.extras import RealDictCursor


def get_db_connection():
    host = os.environ.get("POSTGRES_HOST", "db")
    port = int(os.environ.get("POSTGRES_PORT", "5432"))
    dbname = os.environ.get("POSTGRES_DB", "demo")
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
    )


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            with get_db_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        "CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, visited_at TIMESTAMP NOT NULL)"
                    )
                    cur.execute(
                        "INSERT INTO visits (visited_at) VALUES (%s) RETURNING id",
                        (datetime.utcnow(),),
                    )
                    inserted = cur.fetchone()
                    cur.execute("SELECT COUNT(*) AS visit_count FROM visits")
                    row = cur.fetchone()

            body = (
                f"Connected to PostgreSQL on {os.environ.get('POSTGRES_HOST','db')}:{os.environ.get('POSTGRES_PORT','5432')}\n"
                f"Database: {os.environ.get('POSTGRES_DB','demo')}\n"
                f"Visit count: {row['visit_count']}\n"
                f"Last insert id: {inserted['id']}\n"
            )
            self.send_response(200)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(body.encode("utf-8"))
        except Exception as exc:
            error_body = f"Unable to connect to PostgreSQL: {exc}\n"
            self.send_response(502)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(error_body.encode("utf-8"))


if __name__ == "__main__":
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, HelloHandler)
    print("Serving on port 8080...")
    httpd.serve_forever()
