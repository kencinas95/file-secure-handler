import typer

from secure.cli.app import app as cliapp
from secure.webapp.app import app as webapp

app = typer.Typer()


@app.command("webapp")
def run_webapp(port: int = 8080):
    import uvicorn
    uvicorn.run(webapp, host="0.0.0.0", port=port)


if __name__ == '__main__':
    app.add_typer(cliapp)
    app()
