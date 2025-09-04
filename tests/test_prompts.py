"""
Tests for prompt templates
"""

import pytest

from src import PromptTemplates


class TestPromptTemplates:
    """Test cases for PromptTemplates"""
    
    @pytest.fixture
    def templates(self):
        """Create a PromptTemplates instance"""
        return PromptTemplates()
    
    def test_get_translation_prompt_general(self, templates):
        """Test getting general translation prompt"""
        prompt = templates.get_translation_prompt("general")
        
        assert len(prompt) > 0
        assert "translate" in prompt.lower()
        assert "chinese" in prompt.lower()
        assert "english" in prompt.lower()
    
    def test_get_translation_prompt_academic(self, templates):
        """Test getting academic translation prompt"""
        prompt = templates.get_translation_prompt("academic")
        
        assert len(prompt) > 0
        assert "academic" in prompt.lower()
        assert "translate" in prompt.lower()
    
    def test_get_translation_prompt_technical(self, templates):
        """Test getting technical translation prompt"""
        prompt = templates.get_translation_prompt("technical")
        
        assert len(prompt) > 0
        assert "technical" in prompt.lower()
        assert "translate" in prompt.lower()
    
    def test_get_translation_prompt_creative(self, templates):
        """Test getting creative translation prompt"""
        prompt = templates.get_translation_prompt("creative")
        
        assert len(prompt) > 0
        assert "creative" in prompt.lower() or "literary" in prompt.lower()
        assert "translate" in prompt.lower()
    
    def test_get_translation_prompt_invalid(self, templates):
        """Test getting prompt with invalid type"""
        prompt = templates.get_translation_prompt("invalid_type")
        
        # Should fall back to general prompt
        general_prompt = templates.get_translation_prompt("general")
        assert prompt == general_prompt
    
    def test_get_analysis_prompt(self, templates):
        """Test getting analysis prompt"""
        prompt = templates.get_analysis_prompt()
        
        assert len(prompt) > 0
        assert "analy" in prompt.lower()  # Should contain "analysis" or "analyze"
    
    def test_get_quality_assessment_prompt(self, templates):
        """Test getting quality assessment prompt"""
        prompt = templates.get_quality_assessment_prompt()
        
        assert len(prompt) > 0
        assert "quality" in prompt.lower()
        assert "assess" in prompt.lower() or "evaluat" in prompt.lower()
    
    def test_get_batch_translation_prompt(self, templates):
        """Test getting batch translation prompt"""
        prompt = templates.get_batch_translation_prompt()
        
        assert len(prompt) > 0
        assert "batch" in prompt.lower() or "multiple" in prompt.lower()
        assert "translate" in prompt.lower()
    
    def test_all_prompts_non_empty(self, templates):
        """Test that all prompt types return non-empty strings"""
        prompt_types = ["general", "academic", "technical", "creative"]
        
        for ptype in prompt_types:
            prompt = templates.get_translation_prompt(ptype)
            assert len(prompt) > 0, f"Empty prompt for type: {ptype}"
            assert isinstance(prompt, str), f"Prompt should be string for type: {ptype}"
    
    def test_prompt_customization(self, templates):
        """Test prompt customization with parameters"""
        source_lang = "Chinese"
        target_lang = "English"
        
        # Test if prompts can be formatted (basic check)
        for ptype in ["general", "academic", "technical", "creative"]:
            prompt = templates.get_translation_prompt(ptype)
            
            # Check if prompt contains placeholders or language references
            assert "chinese" in prompt.lower() or "source" in prompt.lower()
            assert "english" in prompt.lower() or "target" in prompt.lower()
