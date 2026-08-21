#!/usr/bin/env python3
"""Regression tests for Scout's aggregate-only public data contract."""

from __future__ import annotations

import copy
import json
import unittest

from validate import DATA_PATH, validate_data


class PublicBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(DATA_PATH.read_text(encoding="utf-8"))

    def test_current_summary_is_valid(self) -> None:
        self.assertEqual(validate_data(self.payload), [])

    def test_live_application_fields_are_rejected(self) -> None:
        forbidden_fields = (
            "employer",
            "title",
            "status",
            "deadline",
            "fit_score",
            "priority",
            "next_action",
            "url",
        )
        for field in forbidden_fields:
            with self.subTest(field=field):
                payload = copy.deepcopy(self.payload)
                payload["focus_areas"][0][field] = "must stay private"
                errors = validate_data(payload)
                self.assertTrue(
                    any("forbidden public field" in error for error in errors),
                    errors,
                )

    def test_contact_details_are_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["notice"] = "Contact applicant@example.com"
        self.assertTrue(
            any("email address" in error for error in validate_data(payload))
        )

    def test_direct_urls_are_rejected(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["notice"] = "See https://example.com/private-target"
        self.assertTrue(any("direct URLs" in error for error in validate_data(payload)))


if __name__ == "__main__":
    unittest.main()
