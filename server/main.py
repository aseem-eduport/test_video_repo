"""My server runtime"""
from server.app import app
from server.routes.doubt_clearance import router as DoubtClearanceRoutes

app.include_router(DoubtClearanceRoutes)