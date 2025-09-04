#!/usr/bin/env python3
"""
Simple MCP Server Test
Tests basic MCP server functionality
"""

import asyncio
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_server_import():
    """Test server module import"""
    logger.info("Testing server import...")
    
    try:
        import server
        logger.info("✅ Server module imported successfully")
        
        # Check if main components exist
        if hasattr(server, 'BookBridgeMCPServer'):
            logger.info("✅ BookBridgeMCPServer class found")
        else:
            logger.error("❌ BookBridgeMCPServer class not found")
            return False
            
        return True
        
    except ImportError as e:
        logger.error(f"❌ Failed to import server: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


async def test_component_imports():
    """Test individual component imports"""
    logger.info("Testing component imports...")
    
    try:
        # Add src to path
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        from document_processor import DocumentProcessor
        from resource_manager import ResourceManager
        from prompts import PromptTemplates
        from translator import TranslationUtils
        
        logger.info("✅ All components imported successfully")
        
        # Test basic instantiation
        processor = DocumentProcessor()
        manager = ResourceManager()
        templates = PromptTemplates()
        utils = TranslationUtils()
        
        logger.info("✅ All components instantiated successfully")
        return True
        
    except ImportError as e:
        logger.error(f"❌ Failed to import components: {e}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False


async def test_basic_functionality():
    """Test basic functionality of components"""
    logger.info("Testing basic functionality...")
    
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        
        from prompts import PromptTemplates
        from translator import TranslationUtils
        
        # Test prompt templates
        templates = PromptTemplates()
        general_prompt = await templates.get_translation_prompt("Chinese", "English", "general")
        assert len(general_prompt) > 0, "Empty general prompt"
        logger.info(f"✅ General prompt: {len(general_prompt)} characters")
        
        # Test translation utils
        utils = TranslationUtils()
        test_content = "这是测试内容。" * 10
        chunks = utils.smart_chunk_content(test_content)
        assert len(chunks) > 0, "No chunks generated"
        logger.info(f"✅ Content chunking: {len(chunks)} chunks")
        
        # Test metrics calculation
        metrics = utils.calculate_translation_metrics("中文内容", "English content")
        assert "length_ratio" in metrics, "Missing length_ratio"
        logger.info(f"✅ Translation metrics calculated")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Basic functionality test failed: {e}")
        return False


async def main():
    """Run all tests"""
    logger.info("🚀 Starting BookBridge-MCP Simple Tests")
    logger.info("=" * 50)
    
    try:
        # Test server import
        if not await test_server_import():
            logger.error("❌ Server import test failed")
            return False
        
        # Test component imports
        if not await test_component_imports():
            logger.error("❌ Component import test failed")
            return False
        
        # Test basic functionality
        if not await test_basic_functionality():
            logger.error("❌ Basic functionality test failed")
            return False
        
        logger.info("=" * 50)
        logger.info("🎉 All tests passed! MCP Server is ready!")
        logger.info("\n✅ Next steps:")
        logger.info("1. Start the MCP server: poetry run python start.py")
        logger.info("2. Test with client: poetry run python examples/client_example.py")
        logger.info("3. Run full tests: poetry run pytest")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
