# /backend/app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.errors import POSException, TableLockedException
from app.api import auth, menu


app = FastAPI()

app.include_router(auth.router)
app.include_router(menu.router)

@app.exception_handler(POSException)
async def pos_exception_handler(request: Request, exc: POSException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "code": exc.status_code
        }
    )

@app.get("/health")
async def health():
    return {"status": "ok"}

# Test Routes to confirm error handler works
@app.get("/test-error")
async def test_error():
    raise TableLockedException(
        table_number=4,
        employee_name="Josh",
        tablet_id="Tablet-2"
    )