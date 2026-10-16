"""Read-only AL 404 V0.2 audit overlay — NOT the production crawler.

Separates recorded legacy verdicts from evidence justified by observed HTTP status.
This module never fetches URLs, changes AL runtime allowed surfaces, or writes receipts.
Activation requires governance review: https://github.com/jsonwisdom/AL/issues/433
"""
from collections.abc import Mapping
from typing import Any


def classify_observation(http_status: Any) -> str:
    """Classify only the HTTP status actually stored in a historical receipt.

    Neither 403 nor a missing status alone proves crawler-specific blocking.
    """
    if http_status is None:
        return "FETCH_STATUS_UNOBSERVED"
    if type(http_status) is not int or not 100 <= http_status <= 599:
        return "INVALID_HTTP_STATUS"
    exact = {
        200: "HTTP_200_OBSERVED",
        401: "HTTP_401_UNAUTHORIZED",
        403: "HTTP_403_FORBIDDEN",
        404: "HTTP_404_OBSERVED",
        410: "HTTP_410_GONE",
        429: "HTTP_429_RATE_LIMITED",
    }
    if http_status in exact:
        return exact[http_status]
    if 300 <= http_status <= 399:
        return "HTTP_REDIRECT_OBSERVED"
    if 500 <= http_status <= 599:
        return "HTTP_SERVER_ERROR_OBSERVED"
    if 400 <= http_status <= 499:
        return "HTTP_CLIENT_ERROR_OBSERVED"
    if 200 <= http_status <= 299:
        return "HTTP_SUCCESS_STATUS_OBSERVED"
    return "HTTP_INFORMATIONAL_STATUS_OBSERVED"


def derived_receipt_view(receipt: Mapping[str, Any]) -> dict[str, Any]:
    """Return a new derived interpretation, leaving receipt bytes untouched."""
    return {
        "source_receipt_id": receipt.get("receipt_id"),
        "source_target_url": receipt.get("target_url"),
        "source_crawl_timestamp": receipt.get("crawl_timestamp"),
        "legacy_verdict_preserved": receipt.get("verdict"),
        "http_status": receipt.get("http_status"),
        "evidence_classification": classify_observation(receipt.get("http_status")),
        "response_hash_field_present": isinstance(receipt.get("observed_hash"), str),
        "response_hash_independently_verified": False,
        "crawler_specific_block_proven": False,
        "root_cause": "UNKNOWN",
        "source_mutated": False,
        "derived_overlay_only": True,
        "authority_created": False,
    }
