"""
Test configuration and fixtures for BookBridge-MCP
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def sample_chinese_content():
    """Sample Chinese content for testing"""
    return """# 测试文档

这是一个测试文档，用于验证翻译功能。

## 主要特性

1. **文档处理**: 支持多种格式
2. **智能翻译**: 高质量的中英翻译
3. **格式保持**: 保持原始格式结构

## 技术细节

这个系统使用了先进的自然语言处理技术，
能够准确理解中文语境并生成流畅的英文翻译。

### 应用场景

- 学术论文翻译
- 技术文档翻译  
- 创意内容翻译
- 商务文档翻译

**重要提示**: 请在使用前配置相关参数。"""


@pytest.fixture
def sample_english_content():
    """Sample English content for testing"""
    return """# Test Document

This is a test document used to verify translation functionality.

## Main Features

1. **Document Processing**: Support for multiple formats
2. **Smart Translation**: High-quality Chinese-English translation
3. **Format Preservation**: Maintain original format structure

## Technical Details

This system uses advanced natural language processing technology,
capable of accurately understanding Chinese context and generating fluent English translations.

### Application Scenarios

- Academic paper translation
- Technical documentation translation
- Creative content translation
- Business document translation

**Important Note**: Please configure relevant parameters before use."""


@pytest.fixture
def mock_openai_response():
    """Mock OpenAI API response"""
    return {
        "choices": [
            {
                "message": {
                    "content": "This is a mocked translation result."
                }
            }
        ],
        "usage": {
            "total_tokens": 150
        }
    }
