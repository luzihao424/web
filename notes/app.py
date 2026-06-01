from note import create_app
from note.commands import init_db

app = create_app("dev")
app.cli.add_command(init_db)

if __name__ == "__main__":
    app.run(debug=True)