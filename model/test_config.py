with open("model/conf.py", "w") as fhand:
    fhand.write(
            """WTF_CSRF_ENABLED = False
SERVER_NAME     = "127.0.0.1:5000"
DATABASE        = "test"
USER            = "chris"
PASSWORD        = "x"
HOST            = "127.0.0.1"
DB_PORT         = "5432"
PORT            = "5000"
DEBUG           = True""")
