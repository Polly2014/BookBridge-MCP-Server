# Changelog

All notable changes to BookBridge-MCP will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Enhanced translation features
- Support for more document formats (PDF, EPUB)
- Improved batch processing performance
- Translation memory integration

## [1.0.2] - 2025-10-17

### Changed
- Added `bookbridge-mcp` as the primary executable name (unified with package name)
- Kept `bookbridge-server` as an alias for backward compatibility
- Now supports shorter command: `uvx bookbridge-mcp`

### Breaking Changes
None - both `bookbridge-mcp` and `bookbridge-server` work

## [1.0.1] - 2025-10-17

### Changed
- Updated README.md to highlight PyPI release
- Reorganized installation methods with PyPI as the recommended option
- Added PyPI and License badges
- Added installation methods comparison table
- Enhanced documentation section with links to all guides
- Added "Show Your Support" section

### Documentation
- Created `README_UPDATE_SUMMARY.md` documenting all README improvements

## [1.0.0] - 2025-10-17

### 🎉 First Stable Release - Published to PyPI!

**PyPI Package:** https://pypi.org/project/bookbridge-mcp/

### Added

#### PyPI Distribution
- ✅ **Published to PyPI** as `bookbridge-mcp`
- ✅ Available via `uvx --from bookbridge-mcp bookbridge-server`
- ✅ Automated publishing with GitHub Actions
- ✅ GitHub automated testing workflow

#### Installation Methods
- uvx support for direct installation from GitHub
- uvx support for installation from PyPI
- Poetry-based local development setup

#### Documentation
- Comprehensive installation documentation (INSTALLATION.md)
- Quick start guide (QUICKSTART.md)
- MCP configuration examples (MCP_CONFIG_EXAMPLES.md)
- PyPI publishing guide (PYPI_PUBLISHING.md)
- Release announcement (RELEASE_ANNOUNCEMENT.md)

### Changed
- Updated README.md with all three installation methods
- Updated pyproject.toml with correct repository URLs
- Updated pyproject.toml with correct repository URLs
- Enhanced documentation structure

### Fixed
- N/A

## [1.0.0] - 2025-10-17

### Added
- Initial release of BookBridge-MCP
- FastMCP-based server implementation
- Document processing tools (Word ↔ Markdown conversion)
- Resource management system
- Translation prompt templates
- Client-side LLM architecture
- Batch document processing
- Format preservation during translation
- Comprehensive test suite
- Poetry-based dependency management
- Development workflow automation
- Example client implementation
- Environment-based configuration

### Features

#### Tools
- `convert_word_to_markdown`: Convert Word documents to Markdown
- `convert_markdown_to_word`: Convert Markdown to Word documents
- `batch_prepare_documents`: Prepare multiple documents for translation
- `save_translated_content`: Save translations in desired format
- `list_documents`: List all available documents
- `get_document_content`: Retrieve document content and metadata
- `scan_documents`: Discover and inventory documents

#### Resources
- Project tracking and management
- Document metadata storage
- Translation progress monitoring

#### Prompts
- Academic translation prompts
- General content translation
- Technical translation
- Creative content translation

### Documentation
- README.md with comprehensive guide
- Installation instructions
- Usage examples
- Architecture overview
- API documentation
- Development setup guide

### Development Tools
- Automated testing with pytest
- Code formatting with black
- Import sorting with isort
- Linting with flake8
- Type checking with mypy
- Pre-commit hooks
- Makefile for common tasks

---

## Release History

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### How to Read This Changelog

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security vulnerability fixes

---

## Upgrade Notes

### From 0.x to 1.0.0

First stable release. No upgrade path needed.

---

## Contributing

When making changes:
1. Update this CHANGELOG.md
2. Follow the format above
3. Keep entries in chronological order
4. Link to relevant issues/PRs when applicable

---

[Unreleased]: https://github.com/Polly2014/BookBridge-MCP-Server/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Polly2014/BookBridge-MCP-Server/releases/tag/v1.0.0
