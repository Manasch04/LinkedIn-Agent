"""
Unit tests for src/generator.py
Run with: pytest tests/
"""

import pytest
from unittest.mock import patch, MagicMock
from src.generator import generate_post, _parse_output, _build_type_instruction


class TestParseOutput:
    def test_valid_delimiters(self):
        raw = "---POST---\nPost body\n---IMAGE CONCEPT---\nImage body"
        post, image = _parse_output(raw)
        assert post == "Post body"
        assert image == "Image body"

    def test_missing_delimiters_falls_back_gracefully(self):
        raw = "Some raw output without delimiters"
        post, image = _parse_output(raw)
        assert post == raw.strip()
        assert "re-run" in image


class TestBuildTypeInstruction:
    def test_known_types_return_instructions(self):
        for t in ("internal_story", "founder_spotlight", "tool_breakdown", "contrarian"):
            assert _build_type_instruction(t) != ""

    def test_unknown_type_returns_auto_instruction(self):
        result = _build_type_instruction("unknown")
        assert "suitable post type" in result


class TestGeneratePost:
    @patch("src.generator.requests.post")
    def test_returns_expected_keys(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "---POST---\nHook\n---IMAGE CONCEPT---\nImage"}}]
        }
        mock_post.return_value = mock_response

        result = generate_post("AI tools", "tool_breakdown")

        assert result["topic"] == "AI tools"
        assert result["post_type"] == "tool_breakdown"
        assert result["post"] == "Hook"
        assert result["image_concept"] == "Image"
        assert "generated_at" in result

    @patch("src.generator.requests.post")
    def test_http_error_raises(self, mock_post):
        mock_post.return_value.raise_for_status.side_effect = Exception("HTTP 401")
        with pytest.raises(Exception, match="HTTP 401"):
            generate_post("some topic")
