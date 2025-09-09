# Chat with your Data User Guide

## What to Check
- [ ] Page loads with enhanced styling
- [ ] Title displays: "📚 Chat with your Data"
- [ ] Subtitle shows: "Upload documents and get intelligent answers using RAG"
- [ ] API key input form appears when not configured
- [ ] File uploader widget visible and functional

## What to Type

### Initial Setup
1. **API Key Configuration**
   ```
   Type: sk-proj-[your-openai-api-key]
   Click: "Connect" button
   Check: Success message or error if invalid
   ```

2. **Document Upload**
   ```
   Action: Click file uploader
   Upload: One or more PDF files
   Check: "📚 Processing documents..." spinner appears
   Wait: Until processing completes
   ```

### Test Prompts

#### Document Overview
```
Type: "What is this document about?"
Check: Bot provides comprehensive summary of uploaded content
```

```
Type: "Summarize the main points covered in the document"
Check: Bot extracts and presents key topics and themes
```

#### Specific Information Extraction
```
Type: "What does the document say about machine learning?"
Check: Bot finds and quotes relevant ML sections with context
```

```
Type: "Find all mentions of 'data science' in the documents"
Check: Bot locates specific references and provides context
```

#### Factual Queries
```
Type: "What are the exact statistics mentioned in the document?"
Check: Bot extracts specific numbers, percentages, and data points
```

```
Type: "Who are the authors referenced in this paper?"
Check: Bot identifies and lists author names and citations
```

### Advanced Testing

#### Multi-Document Analysis
```
Upload: Multiple related PDFs
Type: "Compare the findings between these documents"
Check: Bot analyzes differences and similarities across documents
```

#### Detailed Exploration
```
Type: "What methodology was used in this research?"
Check: Bot identifies and explains research methods from document
```

```
Type: "What are the limitations mentioned in the study?"
Check: Bot finds and summarizes study limitations and constraints
```

#### Contextual Questions
```
Type: "How does this research relate to current industry trends?"
Check: Bot provides document-based insights with broader context
```

#### Verification Queries
```
Type: "What sources are cited for the claim about [specific topic]?"
Check: Bot identifies supporting references and citations
```

## What Should Happen
- ✅ Document processing with progress indicator
- ✅ "Analyzing documents..." spinner during query processing
- ✅ Responses include specific document excerpts
- ✅ Clear indication when information isn't found in documents
- ✅ Support for multiple PDF files simultaneously
- ✅ Intelligent mode detection (summary vs specific facts)

## Troubleshooting
- **Processing fails**: Ensure PDFs are not password-protected or corrupted
- **No relevant answers**: Try different keywords or rephrasing questions
- **Slow processing**: Large documents take time to process and index
- **Upload errors**: Check PDF file format and size limitations