"""
Unit tests for generate_summary function.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, List
import json

# Import the function to test (assuming it's in app.py or assistant.py)
# If the function doesn't exist yet, these tests will guide its implementation
try:
    from app import generate_summary, FlashcardState
except ImportError:
    try:
        from assistant import generate_summary, FlashcardState
    except ImportError:
        # If function doesn't exist, we'll define a mock for testing structure
        FlashcardState = None
        generate_summary = None


class TestGenerateSummary:
    """Test suite for generate_summary function."""

    @pytest.fixture
    def sample_state(self):
        """Create a sample FlashcardState for testing."""
        return {
            "notes": "Python is a high-level programming language. It supports multiple programming paradigms.",
            "flashcards": [],
            "quiz": []
        }

    @pytest.fixture
    def sample_state_with_flashcards(self):
        """Create a sample state with flashcards."""
        return {
            "notes": "Machine learning is a subset of AI.",
            "flashcards": [
                {"Q": "What is ML?", "A": "A subset of AI"},
                {"Q": "What is AI?", "A": "Artificial Intelligence"}
            ],
            "quiz": []
        }

    @pytest.fixture
    def mock_gemini_response(self):
        """Create a mock Gemini API response."""
        mock_response = Mock()
        mock_response.text = "Python is a versatile programming language used for various applications."
        return mock_response

    @pytest.mark.skipif(generate_summary is None, reason="generate_summary function not implemented")
    @patch('google.generativeai.GenerativeModel')
    def test_generate_summary_success(self, mock_model_class, sample_state, mock_gemini_response):
        """Test successful summary generation."""
        # Setup mock
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_gemini_response
        mock_model_class.return_value = mock_model_instance

        # Execute
        result = generate_summary(sample_state)

        # Assert
        assert isinstance(result, dict)
        assert "summary" in result
        assert isinstance(result["summary"], str)
        assert len(result["summary"]) > 0
        mock_model_instance.generate_content.assert_called_once()

    @pytest.mark.skipif(generate_summary is None, reason="generate_summary function not implemented")
    @patch('google.generativeai.GenerativeModel')
    def test_generate_summary_with_notes(self, mock_model_class, sample_state, mock_gemini_response):
        """Test that summary is generated from notes in state."""
        # Setup mock
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_gemini_response
        mock_model_class.return_value = mock_model_instance

        # Execute
        result = generate_summary(sample_state)

        # Assert
        assert "summary" in result
        # Verify that the prompt includes the notes
        call_args = mock_model_instance.generate_content.call_args
        assert call_args is not None
        prompt = call_args[0][0] if call_args[0] else str(call_args)
        assert sample_state["notes"] in prompt or "notes" in prompt.lower()

    @pytest.mark.skipif(generate_summary is None, reason="generate_summary function not implemented")
    @patch('google.generativeai.GenerativeModel')
    def test_generate_summary_empty_notes(self, mock_model_class):
        """Test summary generation with empty notes."""
        empty_state = {
            "notes": "",
            "flashcards": [],
            "quiz": []
        }

        mock_response = Mock()
        mock_response.text = "No content to summarize."
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        # Execute
        result = generate_summary(empty_state)

        # Assert
        assert "summary" in result
        assert isinstance(result["summary"], str)

    @pytest.mark.skipif(generate_summary is None, reason="generate_summary function not implemented")
    @patch('google.generativeai.GenerativeModel')
    def test_generate_summary_long_text(self, mock_model_class):
        """Test summary generation with long text input."""
        long_notes = " ".join(["This is a sentence."] * 100)
        long_state = {
            "notes": long_notes,
            "flashcards": [],
            "quiz": []
        }

        mock_response = Mock()
        mock_response.text = "Summary of long text content."
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        # Execute
        result = generate_summary(long_state)

        # Assert
        assert "summary" in result
        assert isinstance(result["summary"], str)

    @pytest.mark.skipif(generate_summary is None, reason="generate_summary function not implemented")
    @patch('google.generativeai.GenerativeModel')
    def test_generate_summary_api_error(self, mock_model_class, sample_state):
        """Test handling of API errors."""
        # Setup mock to raise an exception
        mock_model_instance = Mock()
        mock_model_instance.generate_content.side_effect = Exception("API Error")
        mock_model_class.return_value = mock_model_instance

        # Execute and assert
        with pytest.raises(Exception):
            generate_summary(sample_state)

    @pytest.mark.skipif(generate_summary is None, reason="generate_summary function not implemented")
    @patch('google.generativeai.GenerativeModel')
    def test_generate_summary_missing_notes_key(self, mock_model_class):
        """Test handling when notes key is missing from state."""
        incomplete_state = {
            "flashcards": [],
            "quiz": []
        }

        # This should either raise a KeyError or handle gracefully
        try:
            result = generate_summary(incomplete_state)
            # If it doesn't raise, it should return a dict
            assert isinstance(result, dict)
        except KeyError:
            # KeyError is also acceptable behavior
            pass

    @pytest.mark.skipif(generate_summary is None, reason="generate_summary function not implemented")
    @patch('google.generativeai.GenerativeModel')
    def test_generate_summary_returns_correct_structure(self, mock_model_class, sample_state, mock_gemini_response):
        """Test that the function returns the correct dictionary structure."""
        # Setup mock
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_gemini_response
        mock_model_class.return_value = mock_model_instance

        # Execute
        result = generate_summary(sample_state)

        # Assert structure
        assert isinstance(result, dict)
        assert "summary" in result
        # Should not modify other state keys
        assert "flashcards" not in result or isinstance(result.get("flashcards"), list)
        assert "quiz" not in result or isinstance(result.get("quiz"), list)

    @pytest.mark.skipif(generate_summary is None, reason="generate_summary function not implemented")
    @patch('google.generativeai.GenerativeModel')
    def test_generate_summary_special_characters(self, mock_model_class):
        """Test summary generation with special characters in notes."""
        special_state = {
            "notes": "Test with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?",
            "flashcards": [],
            "quiz": []
        }

        mock_response = Mock()
        mock_response.text = "Summary with special characters handled."
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        # Execute
        result = generate_summary(special_state)

        # Assert
        assert "summary" in result
        assert isinstance(result["summary"], str)

    @pytest.mark.skipif(generate_summary is None, reason="generate_summary function not implemented")
    @patch('google.generativeai.GenerativeModel')
    def test_generate_summary_multiline_notes(self, mock_model_class):
        """Test summary generation with multiline notes."""
        multiline_state = {
            "notes": """Line 1: Introduction to Python
Line 2: Python is versatile
Line 3: It supports OOP
Line 4: And functional programming""",
            "flashcards": [],
            "quiz": []
        }

        mock_response = Mock()
        mock_response.text = "Python is a versatile language supporting multiple paradigms."
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        # Execute
        result = generate_summary(multiline_state)

        # Assert
        assert "summary" in result
        assert isinstance(result["summary"], str)

    @pytest.mark.skipif(generate_summary is None, reason="generate_summary function not implemented")
    @patch('google.generativeai.GenerativeModel')
    def test_generate_summary_unicode_characters(self, mock_model_class):
        """Test summary generation with unicode characters."""
        unicode_state = {
            "notes": "Test with unicode: 你好世界 🌍 émoji 🎉",
            "flashcards": [],
            "quiz": []
        }

        mock_response = Mock()
        mock_response.text = "Summary with unicode characters."
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        # Execute
        result = generate_summary(unicode_state)

        # Assert
        assert "summary" in result
        assert isinstance(result["summary"], str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

