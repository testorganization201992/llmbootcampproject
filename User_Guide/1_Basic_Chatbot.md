# Basic Chatbot User Guide

## What to Check
- [ ] Page loads with clean dark theme styling
- [ ] Title displays: "🚀 Basic Chatbot"
- [ ] Subtitle shows: "Your intelligent AI conversation partner with memory"
- [ ] API key input form appears when no key is configured

## What to Type

### Initial Setup
1. **API Key Configuration**
   ```
   Type: sk-proj-[your-openai-api-key]
   Click: "Connect" button
   Check: Success message or error if invalid
   ```

### Test Prompts

#### Basic Conversation
```
Type: "Hello! How are you today?"
Check: Bot responds with greeting and context awareness
```

```
Type: "What can you help me with?"
Check: Bot explains its capabilities
```

#### Memory Test
```
Step 1 - Type: "My name is John and I love programming"
Check: Bot acknowledges and stores information

Step 2 - Type: "What did I tell you about myself?"
Check: Bot remembers your name and programming interest
```

#### Code Assistance
```
Type: "Write a Python function to calculate the factorial of a number"
Check: Bot provides complete, working Python code with explanation
```

```
Type: "Explain the code you just wrote"
Check: Bot explains the logic step by step
```

#### Problem Solving
```
Type: "I'm getting a 'list index out of range' error in Python. How do I fix it?"
Check: Bot provides debugging advice and prevention tips
```

### Advanced Testing

#### Creative Tasks
```
Type: "Write a haiku about artificial intelligence"
Check: Bot creates proper 5-7-5 syllable haiku
```

#### Complex Explanations
```
Type: "Explain machine learning like I'm 10 years old"
Check: Bot uses simple language and analogies
```

#### Multi-turn Conversation
```
Turn 1 - Type: "I'm planning a trip to Malaysia"
Check: Bot shows interest and asks relevant questions

Turn 2 - Type: "What should I pack for Kuala Lumpur in the rainy season?"
Check: Bot remembers Malaysia context and provides seasonal advice

Turn 3 - Type: "How about food recommendations?"
Check: Bot maintains Kuala Lumpur/rainy season context in food suggestions
```

## What Should Happen
- ✅ Immediate response generation
- ✅ Conversation history preserved
- ✅ Context maintained across messages
- ✅ Professional, helpful tone
- ✅ Code blocks properly formatted
- ✅ Streaming response display
- ✅ Error handling for API issues

## Troubleshooting
- **No response**: Check API key validity and internet connection
- **Error messages**: Verify OpenAI API key format (starts with sk-)
- **Slow responses**: Normal for complex queries, wait for completion
- **Lost context**: Refresh page if memory seems broken