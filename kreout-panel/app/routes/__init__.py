from .status_routes import router as status_routes
from .control_routes import router as control_routes
from .server_routes import router as server_routes

all_routes = [
    server_routes,
    control_routes,
    status_routes
]