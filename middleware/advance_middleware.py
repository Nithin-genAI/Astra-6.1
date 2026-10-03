"""
Small Django API demonstrating middleware that attaches structured
request metadata (a correlation ID and request timing) to every JSON
response, including JSON error responses produced by other middleware.
"""
import json
import time
import uuid

import django
from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        ALLOWED_HOSTS=["*"],
        ROOT_URLCONF="main",
        MIDDLEWARE=[
            # TODO: Both middleware classes below must be listed here, in the
            # correct order. Think about which one needs to be able to wrap
            # (and enrich) the response the other one produces.
            "main.RequestMetadataMiddleware",
            "main.APIKeyMiddleware",
        ],
        SECRET_KEY="not-a-secret",
        USE_TZ=True,
    )
django.setup()

from django.http import JsonResponse
from django.urls import path


def build_error_response(code, message, status):
    """Builds a predictable JSON error payload: {"error": {"code", "message"}}."""
    return JsonResponse({"error": {"code": code, "message": message}}, status=status)


class APIKeyMiddleware:
    """Rejects any request missing an 'X-API-Key' header with a JSON 401."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.headers.get("X-API-Key"):
            return build_error_response(
                "unauthorized", "Missing required 'X-API-Key' header.", status=401
            )
        return self.get_response(request)


class RequestMetadataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. On the way IN: Correlation ID & Start Time
        header_id = request.headers.get("X-Correlation-ID")
        if header_id:
            request.correlation_id = header_id
        else:
            request.correlation_id = uuid.uuid4().hex

        request.start_time = time.monotonic()

        # Pass request down the chain
        response = self.get_response(request)

        # 2. On the way OUT: Response Headers & Duration
        duration_ms = (time.monotonic() - request.start_time) * 1000
        response["X-Correlation-ID"] = request.correlation_id
        response["X-Response-Time-Ms"] = str(duration_ms)

        # 3. Inject meta block if JSON response
        content_type = response.get("Content-Type", "")
        if content_type.startswith("application/json"):
            data = json.loads(response.content)
            data["meta"] = {
                "correlation_id": request.correlation_id,
                "duration_ms": duration_ms
            }
            response.content = json.dumps(data)
            response["Content-Length"] = str(len(response.content))

        return response
        
    
            
    """
    TODO: Implement this middleware.

    On the way IN (before calling self.get_response):
      - Read 'X-Correlation-ID' from the incoming request headers. If present,
        reuse it; otherwise generate a new one with uuid.uuid4().hex.
      - Store it on the request as `request.correlation_id`.
      - Record a start time (e.g. time.monotonic()) as `request.start_time`.

    On the way OUT (after calling self.get_response):
      - Compute elapsed time in milliseconds since `request.start_time`.
      - Always set two response headers: 'X-Correlation-ID' and
        'X-Response-Time-Ms'.
      - If response["Content-Type"] starts with "application/json", parse the
        JSON body, add a top-level "meta" key equal to
        {"correlation_id": <id>, "duration_ms": <elapsed>} without touching any
        other existing top-level keys, then re-serialize the body and update
        response["Content-Length"] to match the new body length.
      - Return the (possibly modified) response.

    Remember: this middleware must also correctly enrich responses that were
    returned EARLY by other middleware further down the chain - that only
    works if it is positioned correctly in MIDDLEWARE above.
    """



def calculate_view(request):
    a_raw = request.GET.get("a")
    b_raw = request.GET.get("b")
    try:
        a = float(a_raw)
        b = float(b_raw)
    except (TypeError, ValueError):
        return build_error_response(
            "invalid_request",
            "Query parameters 'a' and 'b' must both be valid numbers.",
            status=400,
        )
    if b == 0:
        return build_error_response(
            "division_by_zero", "Parameter 'b' must not be zero.", status=400
        )
    return JsonResponse({"result": a / b})


urlpatterns = [
    path("calculate/", calculate_view),
]


"""Yes, you nailed the mental model completely! Here is a quick breakdown to confirm your exact understanding:

1. **On the way IN**: You attach `correlation_id` (either reusing the incoming `X-Correlation-ID` header or generating a fresh `uuid`) and `start_time` directly to the `request` object. This ensures traceability and enables duration tracking.
2. **On the way OUT**:
* **Headers**: You calculate the total time elapsed (`duration_ms`) and update the HTTP response headers (`X-Correlation-ID` and `X-Response-Time-Ms`).
* **JSON Injection**: You check if the response is JSON (`Content-Type: application/json`). If yes, you parse the binary body into a Python dictionary (`json.loads`), inject the `meta` key containing `correlation_id` and `duration_ms` alongside existing data, convert it back to a JSON string (`json.dumps`), and update `Content-Length` so client parsers receive a valid payload.


"""