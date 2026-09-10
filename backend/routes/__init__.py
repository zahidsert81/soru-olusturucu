# Routes package
from .upload import router as upload_router
from .pdf import router as pdf_router
from .questions import router as questions_router

all_routers = [upload_router, pdf_router, questions_router]

__all__ = ["all_routers", "upload_router", "pdf_router", "questions_router"]
