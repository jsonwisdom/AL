"""Offline-only tests for the AL 404 V0.2 audit overlay."""
import unittest

from agents.four04_crawler.derived_observation_v0_2 import (
    classify_observation,
    derived_receipt_view,
)


class DerivedObservationV02Tests(unittest.TestCase):
    def test_status_matrix(self):
        examples = {
            None: "FETCH_STATUS_UNOBSERVED",
            200: "HTTP_200_OBSERVED",
            401: "HTTP_401_UNAUTHORIZED",
            403: "HTTP_403_FORBIDDEN",
            404: "HTTP_404_OBSERVED",
            302: "HTTP_REDIRECT_OBSERVED",
            410: "HTTP_410_GONE",
            429: "HTTP_429_RATE_LIMITED",
            500: "HTTP_SERVER_ERROR_OBSERVED",
            418: "HTTP_CLIENT_ERROR_OBSERVED",
            204: "HTTP_SUCCESS_STATUS_OBSERVED",
        }
        for value, expected in examples.items():
            with self.subTest(http_status=value):
                self.assertEqual(classify_observation(value), expected)

    def test_invalid_type_is_not_http_status(self):
        for value in (False, True, "403", 700, -1):
            with self.subTest(value=value):
                self.assertEqual(classify_observation(value), "INVALID_HTTP_STATUS")

    def test_oct_11_oregon_derived_view_does_not_rewrite(self):
        receipt = {
            "receipt_id": "404_CRAWLER_BLOCKED_50a12d9dbad7",
            "target_url": "https://www.courts.oregon.gov/opinions/Documents/S070001.pdf",
            "crawl_timestamp": "2026-10-11T11:45:47.177168+00:00",
            "verdict": "CRAWLER_BLOCKED",
            "http_status": None,
            "observed_hash": None,
        }
        original = dict(receipt)
        view = derived_receipt_view(receipt)
        self.assertEqual(receipt, original)
        self.assertEqual(view["legacy_verdict_preserved"], "CRAWLER_BLOCKED")
        self.assertEqual(view["evidence_classification"], "FETCH_STATUS_UNOBSERVED")
        self.assertFalse(view["crawler_specific_block_proven"])
        self.assertFalse(view["response_hash_field_present"])
        self.assertFalse(view["source_mutated"])

    def test_403_is_not_proven_crawler_block(self):
        view = derived_receipt_view({
            "receipt_id": "404_CRAWLER_BLOCKED_38747bb7e167",
            "verdict": "CRAWLER_BLOCKED",
            "http_status": 403,
            "observed_hash": "sha256:example",
        })
        self.assertEqual(view["evidence_classification"], "HTTP_403_FORBIDDEN")
        self.assertEqual(view["legacy_verdict_preserved"], "CRAWLER_BLOCKED")
        self.assertFalse(view["crawler_specific_block_proven"])
        self.assertTrue(view["response_hash_field_present"])
        self.assertFalse(view["response_hash_independently_verified"])

    def test_404_receipt_preserved(self):
        view = derived_receipt_view({
            "receipt_id": "404_NOT_FOUND_50a12d9dbad7",
            "verdict": "NOT_FOUND",
            "http_status": 404,
        })
        self.assertEqual(view["evidence_classification"], "HTTP_404_OBSERVED")
        self.assertEqual(view["legacy_verdict_preserved"], "NOT_FOUND")


if __name__ == "__main__":
    unittest.main()
