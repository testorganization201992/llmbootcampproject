# Version Management Guide

## Current Version: v1.2.0

This document outlines the versioning strategy and tagging process for the LLM Bootcamp project.

## Semantic Versioning

We follow [Semantic Versioning](https://semver.org/) (SemVer):

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: Breaking changes or major feature overhauls
- **MINOR**: New features, significant improvements, backwards compatible
- **PATCH**: Bug fixes, small improvements, backwards compatible

## Release Process

### 1. Make Changes
```bash
# Work on your feature branch
git checkout feature/your-feature-name
# Make changes...
git add .
git commit -m "Descriptive commit message"
```

### 2. Create Tag
```bash
# For a new minor release (new features)
git tag -a v1.3.0 -m "Release v1.3.0: Brief description

Features:
- New feature 1
- New feature 2

Improvements:
- Improvement 1
- Bug fix 1"

# Push the tag
git push origin v1.3.0
```

### 3. Tag Naming Convention
- **Major releases**: `v2.0.0`, `v3.0.0`
- **Minor releases**: `v1.1.0`, `v1.2.0`, `v1.3.0`
- **Patch releases**: `v1.2.1`, `v1.2.2`

## Version History

### v1.2.0 (2025-01-04)
**Enhanced Settings Panel**
- Foldable settings panel with extensive configuration options
- Quick presets (Conversational, Analytical, Creative, Professional)
- Advanced AI parameters (temperature, top_p, penalties)
- Fixed flashing UI issues and improved state management
- Added comprehensive health check diagnostic tool

### v1.1.0 (Previous)
**Modern UI Theme**
- Updated chatbot with modern UI theme
- Improved visual design and user experience

### v1.0.0 (Initial)
**Initial Release**
- Basic chatbot implementation
- Core functionality established

## Quick Commands

### View all tags:
```bash
git tag -l
```

### View tag details:
```bash
git show v1.2.0
```

### Checkout specific version:
```bash
git checkout v1.2.0
```

### Delete local tag (if needed):
```bash
git tag -d v1.2.0
```

### Delete remote tag (if needed):
```bash
git push --delete origin v1.2.0
```

## Future Releases

### Planned for v1.3.0:
- Additional chatbot features
- Performance improvements
- Enhanced error handling

### Planned for v2.0.0:
- Major architecture changes
- Breaking API changes
- New core functionality

## Notes

- Always create annotated tags (`-a` flag) with descriptive messages
- Include feature lists and improvements in tag messages
- Push tags to remote repository for team visibility
- Use tags for releases, deployments, and version references