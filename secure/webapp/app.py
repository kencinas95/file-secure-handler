import logging
from io import BytesIO
from typing import Annotated

from fastapi import FastAPI
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import Response
from fastapi import UploadFile
from fastapi.responses import StreamingResponse

from secure.exporter import SecureExporter
from secure.importer import SecureImporter

app = FastAPI()

MAX_FILE_SIZE = 1024 ** 3

DEFAULT_ENCODING = "utf-8"

log = logging.getLogger("uvicorn.error")


class CryptoError(ValueError):
    pass


def ex_handler(ex: Exception):
    log.exception("Something went wrong, unable to continue!")
    raise CryptoError from ex


@app.exception_handler(CryptoError)
async def http_ex_handler(request, ex):
    return Response(
        status_code=400,
        media_type="text/plain",
        content="A crypto error has occurred, please review your password or file.")


def get_data_stream(content: str | bytes, encoding: str = DEFAULT_ENCODING):
    if isinstance(content, bytes):
        bs = BytesIO(content)
    else:
        bs = BytesIO(content.encode(encoding))
    while True:
        chunk = bs.read(256)
        if not chunk:
            break
        yield chunk


@app.post("/api/v1/secure/export")
async def export(file: Annotated[UploadFile, File()],
                 password: Annotated[str, Form()],
                 encoding: str = DEFAULT_ENCODING):
    # Validates file size
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Max size for file: {MAX_FILE_SIZE}, got {file.size}"
        )

    # Create exporter
    exporter = SecureExporter(password)

    # Reads and export data from file
    data = await file.read()
    data = exporter.export(data, ex_handler)

    return StreamingResponse(
        get_data_stream(data, encoding),
        status_code=200,
        media_type="application/octet-stream",
        headers={
            "Content-Disposition": f"attachment; filename={file.filename}.out.txt"
        }
    )


@app.post("/api/v1/secure/import")
async def import_(file: Annotated[UploadFile, File()], password: Annotated[str, Form()],
                  encoding: str = DEFAULT_ENCODING):
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Max size for file: {MAX_FILE_SIZE}, got {file.size}"
        )

    importer = SecureImporter(password)

    data = await file.read()
    data = importer.resolve(data.decode(encoding), ex_handler)

    return StreamingResponse(
        get_data_stream(data),
        status_code=200,
        media_type="application/octet-stream",
        headers={
            f"Content-Disposition": f"attachment; filename={file.filename.removesuffix('.out.txt')}"
        }
    )
