# MCP Agent User Guide

## What to Check
- [ ] Page loads with enhanced dark theme
- [ ] Title displays: "🔧 MCP Agent"
- [ ] Subtitle shows: "Advanced AI agent powered by Model Context Protocol"
- [ ] Configuration form shows OpenAI API Key + MCP Server URL fields
- [ ] Informative welcome message about MCP capabilities

## What to Type

### Initial Setup
1. **Configuration Setup**
   ```
   OpenAI API Key: sk-proj-[your-openai-api-key]
   MCP Server URL: https://mcp.zapier.com (or your MCP server URL)
   Click: "Connect" button
   Check: Both settings validated successfully
   ```

### Test Prompts

#### Capability Discovery
```
Type: "What tools and capabilities do you have access to?"
Check: Bot lists available MCP tools and connected apps
```

```
Type: "Show me what actions I can perform through your MCP connection"
Check: Bot explains available Zapier integrations and tools
```

#### Productivity Tasks
```
Type: "Check my unread emails from today and summarize the important ones"
Check: Bot accesses email through MCP and provides summary
```

```
Type: "Create a reminder in my task app to prepare for tomorrow's presentation"
Check: Bot creates task/reminder through connected productivity app
```

#### Communication
```
Type: "Post a message in my team chat about the server maintenance"
Check: Bot sends message through connected chat platform (Slack, Teams, etc.)
```

```
Type: "Draft an email to my team about the project update"
Check: Bot composes and saves/sends email through MCP connection
```

### Workflow Testing

#### Multi-App Actions
```
Type: "Get data from my spreadsheet and create a summary document"
Check: Bot retrieves data and creates document across connected apps
```

```
Type: "Add today's meeting notes to my project management tool"
Check: Bot saves notes to connected project management app
```

#### Content Creation
```
Type: "Draft a blog post about AI productivity tips and save it to Google Docs"
Check: Bot creates content and saves to connected document app
```

```
Type: "Create a social media post about our latest product feature"
Check: Bot drafts content for connected social media platforms
```

#### Data Management
```
Type: "Update my customer database with the new lead information"
Check: Bot adds/updates records in connected CRM or database
```

## What Should Happen
- ✅ "Processing with MCP agent..." spinner during queries
- ✅ Real app connections and actions performed
- ✅ Multi-step workflows executed automatically
- ✅ Confirmation requests for important actions
- ✅ Action chaining across multiple connected apps
- ✅ Clear feedback on successful operations

## Troubleshooting
- **Connection errors**: Verify MCP server URL is correct and accessible
- **No tools available**: Check that apps are connected to your MCP server
- **Action failures**: Ensure connected apps have proper permissions
- **Authentication issues**: Verify both API key and Zapier account connections