from mysql.connector import MySQLConnection
import logging
from config import settings
from typing import Optional


class Database:
    def __init__(self):
        self.settings = settings

    def _connect(self):
        return MySQLConnection(
            database=self.settings.db_name,
            user=self.settings.db_user,
            password=self.settings.db_password,
            host=self.settings.db_host,
            port=self.settings.db_port,
        )

    def create_user(self, name: str, email: str, password_hash: str):
        try:
            conn = self._connect()
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO users (username, email, password)
                VALUES (%s, %s, %s)
                """,
                (name, email, password_hash),
            )

            conn.commit()

            return {"status": "success"}
        
        except Exception:
            logging.exception("Failed to create user")
            return None

    def get_user_by_username(self, username: str) -> Optional[dict]:
        try:
            with self._connect() as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, username, email, password FROM users WHERE username = %s",
                    (username,),
                )
                row = cursor.fetchone()
                if not row:
                    return None
                keys = ["id", "username", "email", "password"]
                return dict(zip(keys, row))
        except Exception:
            logging.exception("Failed to get user by email")
            return None

    def get_user_by_id(self, user_id: int) -> Optional[dict]:
        try:
            with self._connect() as conn, conn.cursor() as cursor:
                cursor.execute(
                    "SELECT id, name, email FROM users WHERE id = %s",
                    (user_id,),
                )
                row = cursor.fetchone()
                if not row:
                    return None
                keys = ["id", "username", "email"]
                return dict(zip(keys, row))
        except Exception:
            logging.exception("Failed to get user by id")
            return None
