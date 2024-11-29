from fastapi import HTTPException


class InvalidStatusChangeError(HTTPException):
    def __init__(self, new_status: str, old_status: str):
        detail = f"""
            A mudança de status de '{old_status}' para '{new_status}'
            não é permitida. Verifique as regras de transição de status
            e tente novamente."""
        super().__init__(status_code=422, detail=detail)
