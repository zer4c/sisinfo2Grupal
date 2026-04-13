from fastapi import Response, UploadFile


class FileParser:
    @staticmethod
    async def to_bytes(file: UploadFile) -> bytes:
        file_bytes = await file.read()
        return file_bytes

    @staticmethod
    def to_response(
        file_bytes: bytes, filename: str, media_type: str = "application/octet-stream"
    ) -> Response:
        return Response(
            content=file_bytes,
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )
