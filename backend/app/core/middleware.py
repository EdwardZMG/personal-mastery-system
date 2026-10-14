import time
import uuid
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app.middleware")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        logger.info(
            "%s %s %d %.3fms request_id=%s",
            request.method,
            request.url.path,
            response.status_code,
            process_time * 1000,
            request_id,
        )

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.3f}"
        return response


def setup_request_logging(app):
    app.add_middleware(RequestLoggingMiddleware)
