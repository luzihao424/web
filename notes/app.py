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