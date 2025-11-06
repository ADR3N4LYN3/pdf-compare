# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-04

### Added

- Initial release of pdf-compare
- Visual PDF comparison using pixel-by-pixel analysis
- Multiple output formats:
  - PDF reports with highlighted differences
  - JSON reports with detailed statistics
  - HTML reports with interactive visualization
  - Individual difference images (PNG)
  - Text summary reports
- Command-line interface with comprehensive options
- Python API for programmatic use
- Advanced multi-page support
- Per-page and overall similarity statistics
- Difference region detection and highlighting
- Configurable DPI for rendering quality
- Configurable threshold for pixel difference tolerance
- Progress bar with tqdm integration
- Colored terminal output for better readability
- Exit codes for script integration (0=identical, 1=different, 2=error)
- PyInstaller build script for standalone executables
- cx_Freeze setup for MSI installer generation
- Comprehensive documentation
- Example usage scripts
- Unit tests with pytest

### Features

- **PDFRenderer**: High-quality PDF rendering using PyMuPDF
  - Configurable DPI (default: 150)
  - Page normalization for different sizes
  - Multi-page rendering support

- **PDFDiffer**: Advanced difference detection
  - Pixel-by-pixel comparison
  - Configurable threshold for minor variations
  - Region detection with bounding boxes
  - Similarity percentage calculation
  - Annotated difference images

- **DiffStats**: Detailed statistics
  - Overall similarity percentage
  - Per-page statistics
  - Difference pixel counts
  - Region analysis
  - JSON serialization

- **Reporter**: Multiple output formats
  - PDF reports with summary and annotated pages
  - HTML reports with responsive design
  - JSON for automation and integration
  - Individual image exports
  - Text summaries

- **PDFComparator**: Main orchestration
  - Simple boolean comparison
  - Detailed comparison with statistics
  - Progress tracking
  - Multiple save formats
  - Error handling

- **CLI**: User-friendly command-line interface
  - Intuitive options
  - Verbose and quiet modes
  - Color-coded output
  - Progress indicators
  - Comprehensive help

### Distribution

- PyPI package (when published)
- Windows ZIP package (PyInstaller)
- Windows MSI installer (cx_Freeze)
- Source code installation

### Documentation

- README.md with comprehensive guide
- docs/installation.md for installation instructions
- docs/examples.md for usage examples
- docs/testing.md for testing guide
- CONTRIBUTING.md for contributors
- Example scripts in examples/
- Inline code documentation
- API docstrings

### Testing

- Unit tests for core modules
- Test coverage for critical paths
- pytest configuration
- Test fixtures and mocks

## [Unreleased]

### Planned Features

- Text-based comparison mode
- Side-by-side visual comparison
- Annotation detection and comparison
- Parallel processing for large PDFs
- Docker container
- Web interface
- More output formats (Markdown, etc.)
- Performance optimizations
- Cross-platform testing

---

## Version History

### Version Numbering

- **Major version (X.0.0)**: Breaking changes
- **Minor version (0.X.0)**: New features, backwards compatible
- **Patch version (0.0.X)**: Bug fixes, backwards compatible

### Release Types

- **Alpha**: Early testing, not feature complete
- **Beta**: Feature complete, testing phase
- **RC (Release Candidate)**: Final testing before release
- **Stable**: Production ready

---

[1.0.0]: https://github.com/ADR3N4LYN3/pdf-compare/releases/tag/v1.0.0
