# Chatbot Agent User Guide

## What to Check
- [ ] Page loads with enhanced dark theme
- [ ] Title displays: "🌐 Chatbot Agent"
- [ ] Subtitle shows: "AI agent with real-time web search capabilities"
- [ ] Dual API key input form (OpenAI + Tavily) appears when not configured

## What to Type

### Initial Setup
1. **API Keys Configuration**
   ```
   OpenAI API Key: sk-proj-[your-openai-api-key]
   Tavily API Key: tvly-[your-tavily-api-key]
   Click: "Connect" button
   Check: Both keys validated successfully
   ```

### Test Prompts

#### Current Events
```
Type: "What's the latest news about artificial intelligence this week?"
Check: Bot searches web and provides recent AI developments with sources
```

```
Type: "What are the current cryptocurrency prices?"
Check: Bot fetches real-time crypto market data
```

#### Real-Time Information
```
Type: "What's the weather forecast for Kuala Lumpur this week?"
Check: Bot searches for current weather data and provides detailed forecast
```

```
Type: "Find the latest stock price for Apple (AAPL)"
Check: Bot retrieves current stock information with recent changes
```

#### Research Queries
```
Type: "What are the recent developments in renewable energy technology?"
Check: Bot searches multiple sources and provides comprehensive overview
```

```
Type: "Find the most recent statistics on electric vehicle adoption globally"
Check: Bot locates current EV market data and trends
```

### Advanced Testing

#### Comparative Analysis
```
Type: "Compare the latest iPhone with Samsung Galaxy flagship models"
Check: Bot searches for recent reviews and specifications, provides comparison
```

#### Market Intelligence
```
Type: "What are the trending startup funding rounds in Southeast Asia?"
Check: Bot finds recent funding news and investment trends
```

#### Time-Sensitive Queries
```
Type: "What happened in the tech industry yesterday?"
Check: Bot searches for very recent tech news and events
```

#### Multi-Step Research
```
Step 1 - Type: "Find information about Malaysia's digital transformation initiatives"
Check: Bot searches and provides government and industry information

Step 2 - Type: "What are the latest tech events happening in Kuala Lumpur?"
Check: Bot searches for current tech events and conferences in KL
```

## What Should Happen
- ✅ "Searching the web..." spinner appears during queries
- ✅ Real-time information retrieved from internet
- ✅ Sources and references provided when available
- ✅ Agent reasoning steps visible in responses
- ✅ Current dates and recent information prioritized
- ✅ Multiple search results synthesized into coherent answers

## Troubleshooting
- **No web results**: Check Tavily API key validity and credits
- **Generic responses**: Verify both API keys are working
- **Search failures**: Ensure internet connectivity
- **Outdated info**: Try rephrasing with "latest" or "recent" keywords