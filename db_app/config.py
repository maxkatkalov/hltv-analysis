import os

import dotenv

dotenv.load_dotenv()


config = {
    "connections": {
        "default": (
            f"postgres://"
            f"{os.getenv('pg_user')}:{os.getenv('pg_user_password')}"
            f"@{os.getenv('pg_db_host')}:{os.getenv('pg_host_port')}"
            f"/{os.getenv('pg_db_name')}"
        ),
    },
    "apps": {
        "models": {
            "models": ["db_app.models"],
            "default_connection": "default",
        }
    },
}
