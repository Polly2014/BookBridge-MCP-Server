"""
Tests for translation utilities
"""

import pytest

from src import TranslationUtils


class TestTranslationUtils:
    """Test cases for TranslationUtils"""
    
    @pytest.fixture
    def utils(self):
        """Create a TranslationUtils instance"""
        return TranslationUtils()
    
    def test_smart_chunk_content_short(self, utils, sample_chinese_content):
        """Test chunking content that's shorter than chunk size"""
        chunks = utils.smart_chunk_content(sample_chinese_content)
        
        # Short content should result in a single chunk
        assert len(chunks) == 1
        assert chunks[0] == sample_chinese_content
    
    def test_smart_chunk_content_long(self, utils):
        """Test chunking long content"""
        # Create content longer than default chunk size
        long_content = "这是一段很长的测试内容。\n" * 200
        chunks = utils.smart_chunk_content(long_content)
        
        # Should be split into multiple chunks
        assert len(chunks) > 1
        
        # Each chunk should be reasonably sized
        for chunk in chunks:
            assert len(chunk) <= utils.max_chunk_size + 100  # Allow some flexibility
    
    def test_calculate_translation_metrics(self, utils, sample_chinese_content, sample_english_content):
        """Test calculating translation metrics"""
        metrics = utils.calculate_translation_metrics(sample_chinese_content, sample_english_content)
        
        assert "original_length" in metrics
        assert "translated_length" in metrics
        assert "length_ratio" in metrics
        assert "original_words" in metrics
        assert "translated_words" in metrics
        assert "word_ratio" in metrics
        assert "headers_preserved" in metrics
        
        # Basic sanity checks
        assert metrics["original_length"] > 0
        assert metrics["translated_length"] > 0
        assert metrics["length_ratio"] > 0
        assert metrics["original_words"] > 0
        assert metrics["translated_words"] > 0
    
    def test_calculate_translation_metrics_empty(self, utils):
        """Test metrics calculation with empty content"""
        metrics = utils.calculate_translation_metrics("", "")
        
        assert metrics["original_length"] == 0
        assert metrics["translated_length"] == 0
        assert metrics["length_ratio"] == 0
        assert metrics["original_words"] == 0
        assert metrics["translated_words"] == 0
    
    def test_validate_translation_completeness_valid(self, utils, sample_chinese_content, sample_english_content):
        """Test validation with valid translation"""
        validation = utils.validate_translation_completeness(sample_chinese_content, sample_english_content)
        
        assert "valid" in validation
        assert "issues" in validation
        assert "warnings" in validation
        assert "metrics" in validation
        
        assert validation["valid"] is True
        assert len(validation["issues"]) == 0
    
    def test_validate_translation_completeness_empty(self, utils, sample_chinese_content):
        """Test validation with empty translation"""
        validation = utils.validate_translation_completeness(sample_chinese_content, "")
        
        assert validation["valid"] is False
        assert len(validation["issues"]) > 0
        assert "empty" in validation["issues"][0].lower()
    
    def test_validate_translation_completeness_too_short(self, utils, sample_chinese_content):
        """Test validation with very short translation"""
        short_translation = "Short."
        validation = utils.validate_translation_completeness(sample_chinese_content, short_translation)
        
        # Should either be invalid or have warnings about being too short
        if not validation["valid"]:
            assert len(validation["issues"]) > 0
        else:
            # Should at least have warnings
            assert len(validation["warnings"]) > 0
    
    def test_prepare_batch_context_empty(self, utils):
        """Test batch context preparation with empty list"""
        context = utils.prepare_batch_context([])
        
        assert "batch_info" in context
        assert context["batch_info"]["total_documents"] == 0
        assert "documents" in context
        assert len(context["documents"]) == 0
    
    def test_prepare_batch_context_with_documents(self, utils, sample_chinese_content):
        """Test batch context preparation with documents"""
        documents = [
            {
                "file_id": "doc1",
                "name": "test1.md",
                "file_type": ".md",
                "content": sample_chinese_content
            },
            {
                "file_id": "doc2", 
                "name": "test2.md",
                "file_type": ".md",
                "content": "简短内容"
            }
        ]
        
        context = utils.prepare_batch_context(documents)
        
        assert context["batch_info"]["total_documents"] == 2
        assert len(context["documents"]) == 2
        assert "total_content_length" in context["batch_info"]
        assert "total_chunks_needed" in context["batch_info"]
        assert "document_types" in context["batch_info"]
        
        # Check document details
        doc_info = context["documents"][0]
        assert doc_info["file_id"] == "doc1"
        assert doc_info["name"] == "test1.md"
        assert doc_info["content_length"] > 0
        assert doc_info["word_count"] > 0
