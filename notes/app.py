from note import create_app
from note.commands import init_db, set_admin

app = create_app("dev")
app.cli.add_command(init_db)
app.cli.add_command(set_admin)

if __name__ == "__main__":
    app.run(debug=True)