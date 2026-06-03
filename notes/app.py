import socket

orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4_only(host, port, family=0, type=0, proto=0, flags=0):
    if family == socket.AF_UNSPEC:
        family = socket.AF_INET
    return orig_getaddrinfo(host, port, family, type, proto, flags)
socket.getaddrinfo = getaddrinfo_ipv4_only



import os
from dotenv import load_dotenv

load_dotenv()

from note import create_app
from note.commands import init_db, set_admin

config_name = os.getenv("FLASK_CONFIG", "dev")
app = create_app(config_name)


app.cli.add_command(init_db)
app.cli.add_command(set_admin)

if __name__ == "__main__":
    app.run(debug=True)