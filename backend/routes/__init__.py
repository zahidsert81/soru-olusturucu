# Routes initialization
from .upload import router as upload_router
from .questions import router as questions_router
from .pdf import router as pdf_router

all_routers = [
    upload_router,
    questions_router,
    pdf_router
]
