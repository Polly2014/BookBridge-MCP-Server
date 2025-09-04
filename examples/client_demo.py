"""
Example usage of BookBridge-MCP client
Demonstrates how to connect to and use the MCP server
"""

import asyncio
import json
from pathlib import Path
from fastmcp import Client


async def main():
    """Example client usage"""
    
    # Initialize client pointing to our server
    client = Client("server.py")
    
    async with client:
        print("🌉 BookBridge-MCP Client Demo")
        print("=" * 50)
        
        # 1. List available documents
        print("\n📚 Listing available documents...")
        docs_result = await client.call_tool("list_documents", {})
        print(f"Found {docs_result.get('documents', {}).get('total_source', 0)} source documents")
        
        # 2. Example: Convert a Word document to Markdown
        # Note: This requires a sample Word document in the input_documents folder
        print("\n📄 Converting Word to Markdown...")
        word_path = "./input_documents/sample_chapter.docx"
        
        if Path(word_path).exists():
            conversion_result = await client.call_tool("word_to_markdown", {
                "document_path": word_path
            })
            print(f"Conversion status: {conversion_result.get('status')}")
            if conversion_result.get('status') == 'success':
                print(f"Output: {conversion_result.get('output_path')}")
        else:
            print(f"Sample file not found: {word_path}")
            print("Please place a Word document in ./input_documents/sample_chapter.docx to test")
        
        # 3. Example: Translate content
        print("\n🌐 Testing translation...")
        sample_chinese_text = """
        这是一个示例章节的开头。主人公小明是一个勇敢的年轻人，他住在一个美丽的小村庄里。
        村庄被青山绿水环绕，空气清新，景色宜人。小明从小就梦想着探索外面的世界。
        """
        
        translation_result = await client.call_tool("translate_content", {
            "content": sample_chinese_text,
            "source_lang": "chinese",
            "target_lang": "english",
            "content_type": "book_chapter"
        })
        
        print(f"Translation status: {translation_result.get('status')}")
        if translation_result.get('status') == 'success':
            print("Original:")
            print(sample_chinese_text)
            print("\nTranslation:")
            print(translation_result.get('translated_content', ''))
            print(f"Confidence: {translation_result.get('confidence_score', 0):.2f}")
        
        # 4. Example: Access resources
        print("\n📖 Accessing translation prompt...")
        try:
            prompt_result = await client.get_prompt("translation_prompt", {
                "source_language": "Chinese",
                "target_language": "English",
                "content_type": "book_chapter"
            })
            print("Translation prompt loaded successfully")
            print(f"Prompt length: {len(prompt_result)} characters")
        except Exception as e:
            print(f"Error accessing prompt: {e}")
        
        # 5. Example: Batch processing (if input directory has files)
        print("\n⚙️ Batch processing example...")
        input_dir = "./input_documents"
        output_dir = "./output_documents"
        
        if Path(input_dir).exists() and any(Path(input_dir).glob("*.docx")):
            batch_result = await client.call_tool("batch_process_book", {
                "input_directory": input_dir,
                "output_directory": output_dir,
                "source_lang": "chinese",
                "target_lang": "english"
            })
            
            print(f"Batch processing status: {batch_result.get('status')}")
            print(f"Total files: {batch_result.get('total_files', 0)}")
            print(f"Successful: {batch_result.get('successful_files', 0)}")
            print(f"Failed: {batch_result.get('failed_files', 0)}")
        else:
            print("No Word documents found for batch processing")
            print(f"Place .docx files in {input_dir} to test batch processing")
        
        print("\n✅ Demo completed!")


if __name__ == "__main__":
    asyncio.run(main())
