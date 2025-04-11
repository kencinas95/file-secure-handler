from typer import Typer

from secure.cli.commands import exporter, importer

app = Typer()

app.command(name="export")(exporter.export)
app.command(name="import")(importer.import_)
