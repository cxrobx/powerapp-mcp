# Power Apps AI Features Reference (2026)

Comprehensive guide to all AI capabilities available in Power Apps as of early 2026.

---

## 1. AI Power Fx Functions

Built-in functions callable directly from any Power Fx formula. No Power Automate or external service required — just write them in a control's property.

### Available Functions

| Function | Signature | Purpose |
|----------|-----------|---------|
| `AISentiment` | `AISentiment(text)` | Returns positive/negative/neutral/mixed sentiment |
| `AIClassify` | `AIClassify(text, [categories])` | Classifies text into provided category list |
| `AIExtract` | `AIExtract(text, [entities])` | Extracts named entities from text |
| `AISummarize` | `AISummarize(text)` | Summarizes long-form text |
| `AIReply` | `AIReply(context, message)` | Generates a contextual reply to a message |
| `AITranslate` | `AITranslate(text, targetLanguage)` | Translates text to target language |
| `AIGenerateText` | `AIGenerateText(prompt)` | General-purpose text generation (added 2025) |

### Usage Examples

```
// Sentiment analysis on feedback
Set(varSentiment, AISentiment(FeedbackInput.Text))

// Classify a support ticket into categories
Set(varCategory, AIClassify(
    TicketDescription.Text,
    ["Billing", "Technical", "Account", "General"]
))

// Extract entities from text
Set(varEntities, AIExtract(
    EmailBody.Text,
    ["Person", "Organization", "Date", "Location"]
))

// Summarize a long document
Set(varSummary, AISummarize(DocumentContent.Text))

// Generate a reply in context
Set(varReply, AIReply(
    ConversationHistory,
    UserMessage.Text
))

// Translate user input
Set(varTranslated, AITranslate(TextInput1.Text, "es"))

// General text generation
Set(varEmail, AIGenerateText(
    "Write a professional follow-up email about: " & MeetingNotes.Text
))
```

### Data Source Compatibility

AI Power Fx functions operate on **text values**, NOT on data sources directly. They work with any data source because you pass them a string:

```
// SharePoint list data → AI function
AISummarize(Gallery1.Selected.Description)

// Dataverse data → AI function
AISentiment(ThisItem.CustomerFeedback)

// Manual input → AI function
AIClassify(TextInput1.Text, ["Urgent", "Normal", "Low"])

// Collection data → AI function
AITranslate(LookUp(MyCollection, ID = 1).Notes, "fr")
```

### Requirements & Limitations

- **License**: Power Apps Premium or M365 E3/E5 with AI Builder capacity
- **Credits**: Consumes Copilot Credits (formerly AI Builder credits, unified 2025)
- **Throttling**: Subject to rate limits under heavy use
- **Availability**: Not available in GCC/sovereign cloud without extra config
- **Offline**: Cannot be used offline
- **Latency**: Each call is a round-trip to Azure AI — expect 1-5 seconds per call
- **Text limits**: Very long texts may be truncated; summarization works best under ~10K chars

---

## 2. App Header Copilot (Integrated Chat Pane)

A built-in Copilot chat experience that appears as a persistent side-panel across all screens.

### How It Works

1. Enable at environment level: Power Platform Admin Center → Environments → Settings → Copilot
2. In Power Apps Studio: Settings → Updates → Preview → toggle "App Copilot"
3. Copilot auto-indexes connected Dataverse tables
4. Users ask natural language questions about their data in the side-panel

### Capabilities

- Natural language queries against app data ("Show me all open orders from last week")
- Data summarization and insights
- On-demand chart/visualization generation
- Customizable via "Edit in Copilot Studio" to add custom Topics and Actions

### Limitations

- **Dataverse only** — cannot query SharePoint, SQL, Excel, or other sources directly
- New data/schema changes can take 15 min to 24 hours to become searchable
- Struggles with complex multi-select choice columns and deeply nested lookups
- Requires "Track Changes" and "Appear in search results" enabled on Dataverse tables
- Some features (Agent Feed) are US-only initially

---

## 3. Copilot Studio Bot (Chatbot Control)

Embed a full Copilot Studio agent as a control on any canvas app screen.

### How It Works

1. Build your bot/agent in Copilot Studio (custom knowledge, topics, actions, plugins)
2. Publish the bot
3. In Power Apps, add a **Chatbot** control to your screen
4. Set the control's `Schema Name` property to your published bot
5. The bot renders its conversation UI inline in your app

### Capabilities

- Full conversational AI with custom logic
- Connect to any knowledge source (SharePoint, websites, Dataverse, files)
- Custom Topics for specific workflows
- Actions that call Power Automate flows or external APIs
- Plugin support for extensibility
- Multi-turn conversation with context retention

### Data Source Compatibility

- **Any source** — you configure knowledge sources in Copilot Studio, not in Power Apps
- SharePoint, Dataverse, websites, uploaded documents, custom APIs all supported
- The bot handles the data access; Power Apps just renders the chat UI

### Authentication

- Inherits signed-in user's identity if bot is configured for Power Platform auth
- "No authentication" mode for simple scenarios
- Manual token passing needed for external-facing apps

---

## 4. AI Builder Models

Pre-built and custom AI models accessible from Power Apps via Power Automate flows or direct Power Fx calls.

### Pre-built Models

| Model | Purpose | Input |
|-------|---------|-------|
| Invoice Processing | Extract fields from invoices | PDF/image |
| Receipt Processing | Extract fields from receipts | PDF/image |
| ID Reader | Extract from passports, driver's licenses | Image |
| Business Card Reader | Extract contact info | Image |
| Text Recognizer (OCR) | Extract text from any image | Image |
| Sentiment Analysis | Positive/negative/neutral | Text |
| Language Detection | Identify language | Text |
| Translation | Multi-language translation | Text |

### Custom Models

| Model | Purpose | Training Required |
|-------|---------|-------------------|
| Document Processing | Fixed-layout form extraction | Yes — sample tagging |
| Generative Document Processing | Unstructured docs (contracts, resumes) | No — prompt-based (new 2025-2026) |
| Category Classification | Text classification into custom buckets | Semi — provide examples |
| Entity Extraction | Extract custom entities (product IDs, dates) | Yes — label examples |
| Object Detection | Identify/count objects in images | Yes — bounding boxes |
| Image Classification | Categorize images | Yes — labeled examples |

### Integration Patterns

**Pattern 1: Power Automate Flow**
```
Button.OnSelect → Run Power Automate flow → AI Builder model → Return result → Display in app
```

**Pattern 2: Direct Power Fx (simpler models)**
```
Set(varResult, AIBuilder.AnalyzeSentiment(TextInput1.Text))
```

**Pattern 3: Prompt Builder**
Low-code interface to build custom GPT prompts. Save as reusable component. Call from Power Apps or Power Automate. Supports multi-modal inputs (text + images/documents).

### Data Source Compatibility

- Works with **any data source** — AI Builder processes the data you send it
- SharePoint, Dataverse, SQL, Excel, REST, uploaded files all work
- Data flows through Power Automate, so any connector Power Automate supports is available

### 2025-2026 Changes

- **Agentic integration**: AI Builder models are now "skills" for Copilot Studio agents
- **Foundry Catalog**: Access models beyond OpenAI (including Anthropic Claude, industry models)
- **Unified Credits**: AI Builder credits merged into Copilot Credits
- **Zero-shot learning**: Many tasks now use generative AI without training samples
- **Multi-modal prompts**: Combine text + documents/images in one prompt step

---

## 5. Azure OpenAI via Custom Connector

The most flexible option — full control over model selection, system prompts, and parameters.

### How It Works

1. Deploy a model in Azure OpenAI (GPT-4o, GPT-4, etc.)
2. Create a custom connector in Power Platform pointing to the Azure OpenAI REST API
3. Call from Power Apps via:
   - Power Automate flow (most common)
   - Direct connector action in Power Fx

### Capabilities

- Any Azure OpenAI model (GPT-4o, GPT-4, embeddings, DALL-E, Whisper)
- Custom system prompts and temperature settings
- Streaming responses (via Power Automate)
- Function calling / tool use
- RAG patterns (combine with Azure AI Search)
- Vision capabilities (GPT-4o with images)

### Example Architecture

```
Power App (canvas)
  → Button.OnSelect triggers Power Automate flow
    → HTTP action calls Azure OpenAI Chat Completions API
    → System prompt: "You are a helpful assistant for inventory management"
    → User message: TextInput1.Text
    → Response parsed and returned to Power Apps
  → Label.Text = flow result
```

### "Create Text with GPT" Action

Power Automate has a native action (no custom connector needed):
- Backed by Azure OpenAI
- Simple text generation
- Callable from Power Apps via flow trigger

### Data Source Compatibility

- **Source-agnostic** — you control what data gets sent to the model
- Can pull context from SharePoint, Dataverse, SQL, or any source before sending to Azure OpenAI
- Common pattern: query data → format as context → send to GPT → return structured result

---

## 6. Copilot Maker Features (App Building AI)

These help YOU build apps, not features for end users.

### Plan Designer (Agent-Led App Building)

- Describe a business problem in natural language
- Multi-agent system generates:
  - Dataverse table definitions with relationships
  - Suggested security roles and permissions
  - Draft Power Automate flows
  - App screens with initial layout
- Iterative refinement through conversation

### Vibe Apps (Conversational Building)

- Lightweight app type built entirely through chat
- "I want to track customer orders" → full app with UI and backend
- Tweak conversationally: "Make the header blue", "Add a history gallery"
- Aimed at rapid personal/team apps

### Formula Copilot

- **Comment-to-Formula**: Type `// Filter to items updated by me today` → Enter → Power Fx generated
- **"Create a Formula" UI**: Dedicated interface with preview before applying
- **Context-aware**: Knows which control property you're editing
- **Explain This Formula**: Plain-English breakdown of any formula
- **Explain This Selection**: Highlight a fragment for targeted explanation

### Smart Paste

- Paste unstructured text (email body, PDF extract) into a form
- Copilot maps content to correct form fields automatically
- End-user facing feature

### Natural Language Filtering (Model-Driven Apps)

- Users type "Show open cases from last week" instead of using filter builder
- End-user facing feature

---

## 7. Data Source Compatibility Matrix

Which AI features work with which data sources:

| Feature | SharePoint | Dataverse | SQL Server | Excel | REST/Custom | Collections |
|---------|:---:|:---:|:---:|:---:|:---:|:---:|
| AI Power Fx functions | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| App Header Copilot | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Copilot Studio Bot | ✅ | ✅ | ✅ | ✅ | ✅ | N/A |
| AI Builder (via flows) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Azure OpenAI connector | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Smart Paste | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| NL Filtering | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |

**Key insight**: AI Power Fx functions and Azure OpenAI work with ANY data source because they operate on text values, not data connections. The App Header Copilot and NL Filtering are Dataverse-only.

---

## 8. Licensing Summary

| Feature | License Required |
|---------|-----------------|
| AI Power Fx functions | Power Apps Premium + Copilot Credits |
| App Header Copilot | Power Apps Premium + M365 Copilot |
| Copilot Studio Bot | Copilot Studio license |
| AI Builder prebuilt models | Power Apps Premium + Copilot Credits |
| AI Builder custom models | Power Apps Premium + Copilot Credits |
| Azure OpenAI connector | Azure subscription + Power Apps Premium |
| Copilot maker features | Included with Power Apps (some features require Premium) |

**Copilot Credits** (formerly AI Builder credits): Pooled at the tenant level. Each AI function call, AI Builder model run, or Copilot interaction consumes credits. M365 E3/E5 includes a base allocation; additional capacity purchasable.

---

## 9. Recommended Patterns by Use Case

| Use Case | Recommended Approach | Data Source |
|----------|---------------------|-------------|
| Sentiment analysis on feedback | `AISentiment()` in formula | Any |
| Auto-categorize support tickets | `AIClassify()` in formula | Any |
| Summarize long documents | `AISummarize()` in formula | Any |
| Chat assistant for app users | Copilot Studio Bot + Chatbot control | Any (configured in Studio) |
| "Ask your data" natural language | App Header Copilot | Dataverse only |
| Invoice/receipt processing | AI Builder prebuilt + Power Automate | Any (via flow) |
| Custom document extraction | Generative Document Processing | Any (via flow) |
| Full LLM with custom prompts | Azure OpenAI custom connector | Any |
| Multi-language support | `AITranslate()` in formula | Any |
| Auto-generate email drafts | `AIGenerateText()` in formula | Any |
| Object detection in photos | AI Builder custom model + flow | Any (via flow) |
