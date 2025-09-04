"""
BookBridge-MCP Client Example
Demonstrates how to use the BookBridge MCP server with client-side LLM processing
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from openai import AsyncOpenAI
import os
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BookBridgeClient:
    """
    Client for BookBridge MCP server with integrated LLM processing
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1", model: str = "gpt-4o-mini"):
        """
        Initialize the BookBridge client
        
        Args:
            api_key: OpenAI API key
            base_url: OpenAI API base URL
            model: Model name for translation
        """
        self.llm_client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        
        # This would typically connect to the MCP server
        # For this example, we'll simulate server responses
        self.mcp_server = None
    
    async def get_translation_prompt(self, content_type: str = "general") -> str:
        """
        Get translation prompt from MCP server
        
        Args:
            content_type: Type of content (general, academic, technical, creative)
            
        Returns:
            Translation prompt template
        """
        # In a real implementation, this would call the MCP server's prompt resource
        prompts = {
            "general": """You are a professional translator specializing in Chinese to English translation. 
            Your task is to translate the given Chinese text to natural, fluent English while preserving:
            - Original meaning and context
            - Writing style and tone
            - All formatting (headers, lists, emphasis)
            - Technical terms accuracy
            
            Please translate the following Chinese text to English:""",
            
            "academic": """You are an academic translator with expertise in scholarly texts. 
            Translate the Chinese academic content to English while maintaining:
            - Academic tone and precision
            - Technical terminology accuracy
            - Citation formats and references
            - Formal academic style
            
            Please translate this Chinese academic text to English:""",
            
            "technical": """You are a technical translator specializing in documentation and manuals.
            Translate the Chinese technical content while preserving:
            - Technical accuracy and precision
            - Procedural instructions clarity
            - Code examples and technical terms
            - Professional technical style
            
            Please translate this Chinese technical content to English:""",
            
            "creative": """You are a literary translator skilled in creative content.
            Translate the Chinese creative text while maintaining:
            - Narrative voice and style
            - Emotional tone and atmosphere
            - Cultural context when appropriate
            - Literary devices and flow
            
            Please translate this Chinese creative text to English:"""
        }
        
        return prompts.get(content_type, prompts["general"])
    
    async def process_document(self, file_path: str) -> Dict[str, Any]:
        """
        Process document using MCP server tools
        
        Args:
            file_path: Path to document file
            
        Returns:
            Document processing result
        """
        # In a real implementation, this would call the MCP server's process_document tool
        # For this example, we'll simulate the response
        
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Simulate reading document content
        if path.suffix.lower() == '.docx':
            # Would call MCP server's word_to_markdown tool
            content = f"# Sample Document\n\nThis is simulated content from {path.name}"
        else:
            content = path.read_text(encoding='utf-8')
        
        return {
            "file_id": str(path.absolute()),
            "name": path.name,
            "file_type": path.suffix.lower(),
            "content": content,
            "word_count": len(content.split()),
            "char_count": len(content)
        }
    
    async def translate_content(
        self, 
        content: str, 
        content_type: str = "general",
        chunk_size: int = 3000
    ) -> Dict[str, Any]:
        """
        Translate content using LLM with proper chunking
        
        Args:
            content: Content to translate
            content_type: Type of content for appropriate prompt
            chunk_size: Maximum characters per chunk
            
        Returns:
            Translation result
        """
        try:
            logger.info(f"Translating content: {len(content)} characters")
            
            # Get appropriate prompt from MCP server
            prompt = await self.get_translation_prompt(content_type)
            
            # Check if content needs chunking
            if len(content) <= chunk_size:
                return await self._translate_chunk(content, prompt)
            else:
                return await self._translate_chunks(content, prompt, chunk_size)
                
        except Exception as e:
            logger.error(f"Translation error: {e}")
            raise
    
    async def _translate_chunk(self, content: str, prompt: str) -> Dict[str, Any]:
        """Translate a single chunk of content"""
        try:
            messages = [
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ]
            
            response = await self.llm_client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.3,
                max_tokens=4000
            )
            
            translated_content = response.choices[0].message.content.strip()
            
            return {
                "translated_content": translated_content,
                "token_usage": response.usage.total_tokens if response.usage else 0,
                "chunks": 1
            }
            
        except Exception as e:
            logger.error(f"Chunk translation error: {e}")
            raise
    
    async def _translate_chunks(self, content: str, prompt: str, chunk_size: int) -> Dict[str, Any]:
        """Translate content by splitting into chunks"""
        try:
            # Smart chunking - preserve paragraph structure
            chunks = self._smart_chunk_content(content, chunk_size)
            logger.info(f"Split content into {len(chunks)} chunks")
            
            translated_chunks = []
            total_tokens = 0
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Translating chunk {i+1}/{len(chunks)}")
                
                result = await self._translate_chunk(chunk, prompt)
                translated_chunks.append(result["translated_content"])
                total_tokens += result.get("token_usage", 0)
                
                # Rate limiting delay
                await asyncio.sleep(0.5)
            
            # Combine chunks
            full_translation = "\n\n".join(translated_chunks)
            
            return {
                "translated_content": full_translation,
                "token_usage": total_tokens,
                "chunks": len(chunks)
            }
            
        except Exception as e:
            logger.error(f"Multi-chunk translation error: {e}")
            raise
    
    def _smart_chunk_content(self, content: str, chunk_size: int) -> List[str]:
        """Intelligently split content into chunks preserving structure"""
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_length = 0
        
        for line in lines:
            line_length = len(line)
            
            # If adding this line would exceed chunk size and we have content
            if current_length + line_length > chunk_size and current_chunk:
                # Save current chunk
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_length = line_length
            else:
                current_chunk.append(line)
                current_length += line_length + 1  # +1 for newline
        
        # Add the last chunk
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
    
    async def translate_document(self, file_path: str, content_type: str = "general") -> Dict[str, Any]:
        """
        Complete document translation workflow
        
        Args:
            file_path: Path to document file
            content_type: Type of content for appropriate translation prompt
            
        Returns:
            Complete translation result
        """
        try:
            logger.info(f"Starting document translation: {file_path}")
            
            # Step 1: Process document using MCP server
            doc_result = await self.process_document(file_path)
            logger.info(f"Document processed: {doc_result['word_count']} words")
            
            # Step 2: Translate content using LLM
            translation_result = await self.translate_content(
                doc_result["content"], 
                content_type
            )
            
            # Step 3: Combine results
            return {
                "original_document": doc_result,
                "translation": translation_result,
                "summary": {
                    "original_words": doc_result["word_count"],
                    "original_chars": doc_result["char_count"],
                    "translated_chars": len(translation_result["translated_content"]),
                    "token_usage": translation_result["token_usage"],
                    "chunks_processed": translation_result["chunks"]
                }
            }
            
        except Exception as e:
            logger.error(f"Document translation error: {e}")
            raise
    
    async def save_translation(
        self, 
        translation_result: Dict[str, Any], 
        output_path: str,
        format_type: str = "markdown"
    ) -> str:
        """
        Save translation result to file
        
        Args:
            translation_result: Result from translate_document
            output_path: Output file path
            format_type: Output format (markdown, docx)
            
        Returns:
            Path to saved file
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            content = translation_result["translation"]["translated_content"]
            
            if format_type == "docx":
                # In a real implementation, this would use the MCP server's
                # markdown_to_word tool
                logger.info("Would convert to Word format using MCP server")
                output_file = output_file.with_suffix('.docx')
            else:
                output_file = output_file.with_suffix('.md')
                output_file.write_text(content, encoding='utf-8')
            
            logger.info(f"Translation saved to: {output_file}")
            return str(output_file.absolute())
            
        except Exception as e:
            logger.error(f"Save translation error: {e}")
            raise


async def main():
    """Example usage of BookBridge client"""
    
    # Initialize client (you would use your actual OpenAI API key)
    api_key = os.getenv("OPENAI_API_KEY", "your_api_key_here")
    client = BookBridgeClient(api_key=api_key)
    
    # Example: Translate a document
    try:
        # This would be the path to your actual document
        document_path = "./sample_document.md"
        
        # Create a sample document for testing
        sample_content = """# 示例文档

这是一个示例文档，用于展示 BookBridge MCP 的翻译功能。

## 主要特性

1. **文档处理**: 支持 Word 和 Markdown 格式
2. **智能翻译**: 基于 OpenAI 的高质量翻译
3. **客户端架构**: LLM 处理在客户端进行

## 技术优势

- 高效的文档转换
- 保持格式完整性
- 支持大文档分块处理

这个系统能够帮助用户快速准确地翻译各种类型的文档。"""
        
        Path("./sample_document.md").write_text(sample_content, encoding='utf-8')
        
        # Translate the document
        logger.info("Starting document translation example...")
        result = await client.translate_document(
            file_path="./sample_document.md",
            content_type="technical"
        )
        
        # Save the translation
        output_path = await client.save_translation(
            result,
            "./output/translated_document.md"
        )
        
        # Display results
        print("\n=== Translation Complete ===")
        print(f"Original words: {result['summary']['original_words']}")
        print(f"Token usage: {result['summary']['token_usage']}")
        print(f"Chunks processed: {result['summary']['chunks_processed']}")
        print(f"Output saved to: {output_path}")
        
        print("\n=== Sample Translation ===")
        print(result["translation"]["translated_content"][:500] + "...")
        
    except Exception as e:
        logger.error(f"Example error: {e}")
        print(f"Error running example: {e}")
        print("Make sure to set OPENAI_API_KEY environment variable")


if __name__ == "__main__":
    asyncio.run(main())
