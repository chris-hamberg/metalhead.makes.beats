import os, urllib.parse

scheme = urllib.parse.urlparse(os.environ["database_url"]).scheme
netloc = urllib.parse.urlparse(os.environ["database_url"]).netloc

DATABASE_URL = f"{scheme}://{netloc}"
DATABASE     = urllib.parse.urlparse(os.environ["database"]).path
USER         = urllib.parse.urlparse(os.environ["username"]).path
PASSWORD     = urllib.parse.urlparse(os.environ["password"]).path
HOST         = urllib.parse.urlparse(os.environ["hostname"]).path
DB_PORT      = urllib.parse.urlparse(os.environ["port"]).path
SSLMODE      = "require"
