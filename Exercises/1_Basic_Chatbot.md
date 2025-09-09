# Exercise 1: Basic Chatbot - AI Personality System

## Objective
Learn how LLM parameters control response behavior by implementing multiple AI personalities.

## Prerequisites
- OpenAI API key

---

## Implementation

### Step 1: Add Configuration Methods
**File:** `project_code/langchain_helpers.py`  
**Location:** Inside `BasicChatbotHelper` class, after `get_default_config()` method

```python
@staticmethod
def get_creative_config() -> Dict[str, Any]:
    """Configuration optimized for creative and imaginative responses"""
    return {
        "model": "gpt-4o-mini",
        "temperature": 1.2,
        "max_tokens": 3000,
        "top_p": 0.9,
        "frequency_penalty": 0.3,
        "presence_penalty": 0.6,
        "response_style": "Creative"
    }

@staticmethod
def get_analytical_config() -> Dict[str, Any]:
    """Configuration for precise, analytical responses"""
    return {
        "model": "gpt-4o-mini",
        "temperature": 0.1,
        "max_tokens": 2500,
        "top_p": 0.95,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "response_style": "Technical"
    }

@staticmethod
def get_conversational_config() -> Dict[str, Any]:
    """Configuration for natural, friendly conversations"""
    return {
        "model": "gpt-4o-mini", 
        "temperature": 0.8,
        "max_tokens": 2000,
        "top_p": 0.85,
        "frequency_penalty": 0.2,
        "presence_penalty": 0.3,
        "response_style": "Casual"
    }
```

### Step 2: Add UI Selector
**File:** `project_code/pages/1_Basic_Chatbot.py`  
**Location:** Replace line 71 `config = BasicChatbotHelper.get_default_config()`

```python
# Create personality selector in sidebar
st.sidebar.markdown("### 🎭 Choose AI Personality")
config_type = st.sidebar.selectbox(
    "Select AI personality:",
    ["Default", "Creative", "Analytical", "Conversational"],
    key="basic_config_type"
)

# Map personalities to configurations
config_map = {
    "Default": BasicChatbotHelper.get_default_config(),
    "Creative": BasicChatbotHelper.get_creative_config(),
    "Analytical": BasicChatbotHelper.get_analytical_config(), 
    "Conversational": BasicChatbotHelper.get_conversational_config()
}

config = config_map[config_type]
```

---

## Usage

1. Run `streamlit run Home.py`
2. Navigate to Basic Chatbot page
3. Enter OpenAI API key
4. Select different personalities from sidebar
5. Ask the same question with different personalities to observe behavioral changes

## Key Learning Points

- **Temperature** controls creativity (0.1 = focused, 1.2 = creative)
- **Max tokens** affects response length
- **Frequency/presence penalties** reduce repetition and encourage topic diversity
- **Response style** influences the system prompt behavior