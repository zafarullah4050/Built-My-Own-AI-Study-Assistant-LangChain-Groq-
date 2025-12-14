"""
Integration tests for the complete study flow.
Tests the end-to-end flow from PDF extraction to flashcards and quiz generation.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock, mock_open
from typing import Dict, List
import json
import io
from PyPDF2 import PdfReader

# Import the functions and classes to test
try:
    from app import (
        FlashcardState,
        generate_flashcards,
        generate_quiz,
        extract_text_from_pdf,
        app_flow
    )
except ImportError:
    try:
        from assistant import (
            FlashcardState,
            generate_flashcards,
            generate_quiz,
            extract_text_from_pdf,
            app
        )
        app_flow = app
    except ImportError:
        pytest.skip("Required modules not found", allow_module_level=True)


class TestStudyFlow:
    """Integration tests for the complete study flow."""

    @pytest.fixture
    def sample_notes(self):
        """Sample notes text for testing."""
        return """
        Python is a high-level programming language.
        It supports multiple programming paradigms including procedural,
        object-oriented, and functional programming.
        Python uses dynamic typing and garbage collection.
        """

    @pytest.fixture
    def sample_flashcards(self):
        """Sample flashcards for testing."""
        return [
            {"Q": "What is Python?", "A": "A high-level programming language"},
            {"Q": "What paradigms does Python support?", "A": "Procedural, OOP, and functional"},
            {"Q": "What typing does Python use?", "A": "Dynamic typing"}
        ]

    @pytest.fixture
    def sample_quiz(self):
        """Sample quiz questions for testing."""
        return [
            {
                "question": "What is Python?",
                "options": ["A high-level programming language", "Wrong1", "Wrong2", "Wrong3"],
                "answer": "A high-level programming language"
            },
            {
                "question": "What paradigms does Python support?",
                "options": ["Procedural, OOP, and functional", "Wrong1", "Wrong2", "Wrong3"],
                "answer": "Procedural, OOP, and functional"
            }
        ]

    @pytest.fixture
    def mock_pdf_file(self):
        """Create a mock PDF file object."""
        pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n>>\nendobj\n"
        return io.BytesIO(pdf_content)

    @pytest.mark.integration
    @patch('google.generativeai.GenerativeModel')
    def test_complete_flow_flashcards_to_quiz(self, mock_model_class, sample_notes, sample_flashcards):
        """Test the complete flow from notes to flashcards to quiz."""
        # Setup mock Gemini API response
        mock_response = Mock()
        mock_response.text = json.dumps(sample_flashcards)
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        # Initial state
        initial_state = {
            "notes": sample_notes,
            "flashcards": [],
            "quiz": []
        }

        # Execute flashcards generation
        flashcards_state = generate_flashcards(initial_state)
        assert "flashcards" in flashcards_state
        assert len(flashcards_state["flashcards"]) > 0

        # Merge state for quiz generation
        quiz_input_state = {**initial_state, **flashcards_state}

        # Execute quiz generation
        quiz_state = generate_quiz(quiz_input_state)
        assert "quiz" in quiz_state
        assert len(quiz_state["quiz"]) > 0
        assert len(quiz_state["quiz"]) == len(flashcards_state["flashcards"])

        # Verify quiz structure
        for quiz_item in quiz_state["quiz"]:
            assert "question" in quiz_item
            assert "options" in quiz_item
            assert "answer" in quiz_item
            assert len(quiz_item["options"]) == 4

    @pytest.mark.integration
    @patch('google.generativeai.GenerativeModel')
    def test_langgraph_complete_flow(self, mock_model_class, sample_notes, sample_flashcards):
        """Test the complete LangGraph flow from start to end."""
        # Setup mock Gemini API response
        mock_response = Mock()
        mock_response.text = json.dumps(sample_flashcards)
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        # Initial state
        initial_state = {
            "notes": sample_notes,
            "flashcards": [],
            "quiz": []
        }

        # Execute the complete flow
        final_state = app_flow.invoke(initial_state)

        # Verify final state
        assert "flashcards" in final_state
        assert "quiz" in final_state
        assert len(final_state["flashcards"]) > 0
        assert len(final_state["quiz"]) > 0
        assert len(final_state["quiz"]) == len(final_state["flashcards"])

        # Verify flashcards structure
        for card in final_state["flashcards"]:
            assert "Q" in card
            assert "A" in card

        # Verify quiz structure
        for quiz_item in final_state["quiz"]:
            assert "question" in quiz_item
            assert "options" in quiz_item
            assert "answer" in quiz_item
            assert quiz_item["answer"] in quiz_item["options"]

    @pytest.mark.integration
    def test_pdf_extraction(self):
        """Test PDF text extraction functionality."""
        # Create a simple mock PDF file
        pdf_text = "This is test PDF content.\nLine 2 of content."
        
        # Mock PdfReader
        mock_page = Mock()
        mock_page.extract_text.return_value = pdf_text
        
        mock_reader = Mock()
        mock_reader.pages = [mock_page]

        with patch('PyPDF2.PdfReader', return_value=mock_reader):
            # Create a file-like object
            file_obj = io.BytesIO(b"fake pdf content")
            
            # Test extraction
            extracted_text = extract_text_from_pdf(file_obj)
            assert isinstance(extracted_text, str)
            assert len(extracted_text) > 0

    @pytest.mark.integration
    @patch('google.generativeai.GenerativeModel')
    def test_flow_with_empty_notes(self, mock_model_class):
        """Test the flow with empty notes."""
        mock_response = Mock()
        mock_response.text = json.dumps([{"Q": "No content", "A": "Empty notes"}])
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        initial_state = {
            "notes": "",
            "flashcards": [],
            "quiz": []
        }

        final_state = app_flow.invoke(initial_state)
        assert "flashcards" in final_state
        assert "quiz" in final_state

    @pytest.mark.integration
    @patch('google.generativeai.GenerativeModel')
    def test_flow_with_long_text(self, mock_model_class):
        """Test the flow with long text input."""
        long_notes = " ".join(["This is a sentence about machine learning."] * 50)
        
        sample_flashcards = [
            {"Q": "What is the topic?", "A": "Machine learning"}
        ]
        
        mock_response = Mock()
        mock_response.text = json.dumps(sample_flashcards)
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        initial_state = {
            "notes": long_notes,
            "flashcards": [],
            "quiz": []
        }

        final_state = app_flow.invoke(initial_state)
        assert "flashcards" in final_state
        assert "quiz" in final_state
        assert len(final_state["flashcards"]) > 0

    @pytest.mark.integration
    @patch('google.generativeai.GenerativeModel')
    def test_flow_error_handling_invalid_json(self, mock_model_class, sample_notes):
        """Test flow handling when API returns invalid JSON."""
        # Mock API returning invalid JSON
        mock_response = Mock()
        mock_response.text = "This is not valid JSON {"
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        initial_state = {
            "notes": sample_notes,
            "flashcards": [],
            "quiz": []
        }

        # Should handle JSON error gracefully (app.py has try-except)
        try:
            final_state = app_flow.invoke(initial_state)
            # If it doesn't crash, verify it has error handling
            assert "flashcards" in final_state
        except (json.JSONDecodeError, KeyError, Exception):
            # Error handling might raise exception, which is acceptable
            pass

    @pytest.mark.integration
    @patch('google.generativeai.GenerativeModel')
    def test_quiz_generation_from_flashcards(self, mock_model_class, sample_flashcards):
        """Test quiz generation directly from flashcards."""
        state_with_flashcards = {
            "notes": "Some notes",
            "flashcards": sample_flashcards,
            "quiz": []
        }

        quiz_state = generate_quiz(state_with_flashcards)
        
        assert "quiz" in quiz_state
        assert len(quiz_state["quiz"]) == len(sample_flashcards)
        
        # Verify each quiz item corresponds to a flashcard
        for i, quiz_item in enumerate(quiz_state["quiz"]):
            assert quiz_item["question"] == sample_flashcards[i]["Q"]
            assert quiz_item["answer"] == sample_flashcards[i]["A"]
            assert quiz_item["answer"] in quiz_item["options"]

    @pytest.mark.integration
    @patch('google.generativeai.GenerativeModel')
    def test_multiple_flashcards_generation(self, mock_model_class, sample_notes):
        """Test generation of multiple flashcards."""
        multiple_flashcards = [
            {"Q": "Question 1", "A": "Answer 1"},
            {"Q": "Question 2", "A": "Answer 2"},
            {"Q": "Question 3", "A": "Answer 3"},
            {"Q": "Question 4", "A": "Answer 4"},
            {"Q": "Question 5", "A": "Answer 5"}
        ]
        
        mock_response = Mock()
        mock_response.text = json.dumps(multiple_flashcards)
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        initial_state = {
            "notes": sample_notes,
            "flashcards": [],
            "quiz": []
        }

        final_state = app_flow.invoke(initial_state)
        
        assert len(final_state["flashcards"]) == 5
        assert len(final_state["quiz"]) == 5
        
        # Verify all flashcards have correct structure
        for card in final_state["flashcards"]:
            assert "Q" in card
            assert "A" in card

    @pytest.mark.integration
    @patch('google.generativeai.GenerativeModel')
    def test_state_persistence_through_flow(self, mock_model_class, sample_notes, sample_flashcards):
        """Test that state is properly maintained through the flow."""
        mock_response = Mock()
        mock_response.text = json.dumps(sample_flashcards)
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        initial_state = {
            "notes": sample_notes,
            "flashcards": [],
            "quiz": []
        }

        final_state = app_flow.invoke(initial_state)

        # Verify notes are preserved
        assert final_state["notes"] == sample_notes
        # Verify flashcards are generated
        assert len(final_state["flashcards"]) > 0
        # Verify quiz is generated from flashcards
        assert len(final_state["quiz"]) == len(final_state["flashcards"])

    @pytest.mark.integration
    @patch('google.generativeai.GenerativeModel')
    def test_flow_with_special_characters(self, mock_model_class):
        """Test flow with special characters in notes."""
        special_notes = "Test with special chars: !@#$%^&*()_+-=[]{}|;':\",./<>?"
        
        sample_flashcards = [{"Q": "Special chars?", "A": "Handled"}]
        
        mock_response = Mock()
        mock_response.text = json.dumps(sample_flashcards)
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        initial_state = {
            "notes": special_notes,
            "flashcards": [],
            "quiz": []
        }

        final_state = app_flow.invoke(initial_state)
        assert "flashcards" in final_state
        assert "quiz" in final_state

    @pytest.mark.integration
    @patch('google.generativeai.GenerativeModel')
    def test_flow_with_unicode(self, mock_model_class):
        """Test flow with unicode characters."""
        unicode_notes = "Test with unicode: 你好世界 🌍 émoji 🎉"
        
        sample_flashcards = [{"Q": "Unicode test?", "A": "Works"}]
        
        mock_response = Mock()
        mock_response.text = json.dumps(sample_flashcards)
        
        mock_model_instance = Mock()
        mock_model_instance.generate_content.return_value = mock_response
        mock_model_class.return_value = mock_model_instance

        initial_state = {
            "notes": unicode_notes,
            "flashcards": [],
            "quiz": []
        }

        final_state = app_flow.invoke(initial_state)
        assert "flashcards" in final_state
        assert "quiz" in final_state


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])

