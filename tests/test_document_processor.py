"""
Tests for document processing functionality
"""

import pytest
from pathlib import Path

from src import DocumentProcessor


class TestDocumentProcessor:
    """Test cases for DocumentProcessor"""
    
    @pytest.fixture
    def processor(self):
        """Create a DocumentProcessor instance"""
        return DocumentProcessor()
    
    @pytest.mark.asyncio
    async def test_process_markdown_content(self, processor, sample_chinese_content):
        """Test processing markdown content"""
        result = await processor.process_markdown_content(sample_chinese_content)
        
        assert result["success"] is True
        assert "content" in result
        assert len(result["content"]) > 0
        assert result["word_count"] > 0
        assert result["char_count"] == len(sample_chinese_content)
    
    @pytest.mark.asyncio
    async def test_process_markdown_file(self, processor, temp_dir, sample_chinese_content):
        """Test processing markdown file"""
        # Create test file
        test_file = temp_dir / "test.md"
        test_file.write_text(sample_chinese_content, encoding='utf-8')
        
        result = await processor.process_markdown_file(str(test_file))
        
        assert result["success"] is True
        assert result["file_path"] == str(test_file)
        assert result["content"] == sample_chinese_content
        assert result["file_size"] > 0
    
    @pytest.mark.asyncio
    async def test_process_nonexistent_file(self, processor):
        """Test processing a file that doesn't exist"""
        result = await processor.process_markdown_file("nonexistent_file.md")
        
        assert result["success"] is False
        assert "error" in result
    
    def test_markdown_to_html(self, processor, sample_chinese_content):
        """Test markdown to HTML conversion"""
        html_content = processor.markdown_to_html(sample_chinese_content)
        
        assert len(html_content) > 0
        assert "<h1>" in html_content  # Check for header conversion
        assert "<h2>" in html_content  # Check for subheader conversion
        assert "<li>" in html_content  # Check for list conversion
    
    def test_clean_html_to_text(self, processor):
        """Test cleaning HTML to text"""
        html_content = "<h1>Title</h1><p>Some <strong>bold</strong> text</p>"
        clean_text = processor.clean_html_to_text(html_content)
        
        assert "Title" in clean_text
        assert "Some bold text" in clean_text
        assert "<h1>" not in clean_text  # HTML tags should be removed
    
    def test_extract_content_structure(self, processor, sample_chinese_content):
        """Test content structure extraction"""
        structure = processor.extract_content_structure(sample_chinese_content)
        
        assert "headers" in structure
        assert "word_count" in structure
        assert "char_count" in structure
        assert "list_items" in structure
        
        # Check that headers are detected
        assert len(structure["headers"]) > 0
        assert any("测试文档" in header["text"] for header in structure["headers"])
    
    def test_validate_markdown(self, processor, sample_chinese_content):
        """Test markdown validation"""
        validation = processor.validate_markdown(sample_chinese_content)
        
        assert "is_valid" in validation
        assert "issues" in validation
        assert validation["is_valid"] is True  # Sample content should be valid
    
    @pytest.mark.asyncio
    async def test_get_file_info(self, processor, temp_dir, sample_chinese_content):
        """Test getting file information"""
        # Create test file
        test_file = temp_dir / "test.md"
        test_file.write_text(sample_chinese_content, encoding='utf-8')
        
        file_info = await processor.get_file_info(str(test_file))
        
        assert file_info["exists"] is True
        assert file_info["size"] > 0
        assert file_info["extension"] == ".md"
        assert "modified_time" in file_info
