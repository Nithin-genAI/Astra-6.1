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
            "main.APIKeyMiddleware",
            "main.RequestMetadataMiddleware",
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

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        raise NotImplementedError("Implement RequestMetadataMiddleware.__call__")


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
