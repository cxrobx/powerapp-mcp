# Power Apps Capabilities Overview (2026)

High-level overview of what Power Apps can do, organized by capability area. Reference for understanding the full scope when building apps via the MCP server.

---

## 1. App Types

| Type | Description | Best For |
|------|-------------|----------|
| **Canvas App** | Pixel-perfect UI, drag-and-drop design, connects to any data source | Custom UIs, mobile-first, consumer-grade experiences |
| **Model-Driven App** | Auto-generated UI from Dataverse data model, forms/views/dashboards | Enterprise CRUD, CRM-style, data-heavy workflows |
| **Portal / Power Pages** | External-facing websites backed by Dataverse | Customer portals, partner portals, self-service |
| **Vibe App** (2025+) | Chat-built lightweight apps | Rapid personal/team tracking apps |

Our MCP server generates **Canvas Apps** (.msapp files).

---

## 2. Data Sources

### Tabular (show in galleries, forms, data tables)

| Source | Delegation | Premium |
|--------|:---:|:---:|
| Microsoft Dataverse | Full | Yes |
| SharePoint Lists | Partial | No |
| SQL Server | Full | Yes |
| Excel (OneDrive/SharePoint) | None | No |
| Google Sheets | None | Yes |
| Oracle Database | Full | Yes |
| MySQL | Partial | Yes |
| PostgreSQL | Partial | Yes |
| Salesforce | Full | Yes |

### Action-Based (call functions, not browse tables)

| Source | Purpose |
|--------|---------|
| Office 365 Outlook | Send email, read calendar |
| Office 365 Users | Look up user profiles |
| Microsoft Teams | Post messages, read channels |
| Power Automate | Trigger/run flows |
| Azure Blob Storage | Upload/download files |
| HTTP (custom) | Call any REST API |
| Twitter/X | Post, search |
| Salesforce | Create/update records |

### Local / In-Memory

| Source | Purpose |
|--------|---------|
| Collections | In-memory tables, created via `Collect()`/`ClearCollect()` |
| Variables | Single values via `Set()` or `UpdateContext()` |
| Local storage | Persist between sessions via `SaveData()`/`LoadData()` |

### Delegation Rules

Delegation = server-side filtering (important for large datasets):
- **Default limit**: 500 records (configurable up to 2,000)
- **Delegable functions**: Filter, Search, Sort, SortByColumns, LookUp, First, Sum, Average, Min, Max, CountRows
- **Non-delegable**: FirstN, LastN, Choices, Concat, GroupBy, Distinct
- **Best delegation**: Dataverse > SQL > SharePoint > Excel (none)

---

## 3. UI Controls (60+)

### Display
Label, HTML text, Rich text editor, Image, Shape (rectangle/circle/triangle), Icon

### Input
Button, Text input, Drop down, Combo box, Date picker, Check box, Toggle, Slider, Rating, Radio, List box, Pen input

### Data
Gallery (vertical/horizontal/flexible), Data table, Edit form, Display form, Card

### Media
Audio, Video, Camera, Microphone, Add picture, Stream Video, Barcode reader

### Layout
Screen, Horizontal container, Vertical container, Container, Grid container

### Charts
Column chart, Line chart, Pie chart

### Integration
Power BI tile, PDF viewer, Map, Export, Import

### Mixed Reality
3D object, Measuring Camera, View in MR, View shape in MR

### AI/Bot
Chatbot (Copilot Studio), App Header Copilot

---

## 4. Power Fx Formula Language

### Overview
- Declarative, functional language inspired by Excel
- 200+ built-in functions
- Strong typing with inference
- Semicolon chaining for behavior: `Action1(); Action2()`
- Dot notation: `Control.Property`
- String interpolation: `$"Hello {Name}"`
- `ThisItem` in galleries, `Parent` for parent control, `Self` for current control

### Key Function Categories
- **Table**: Filter, Sort, LookUp, Patch, Collect, ForAll, GroupBy, AddColumns, etc.
- **Text**: Concatenate, Left/Mid/Right, Replace, Substitute, Split, Trim, etc.
- **Date/Time**: Now, Today, DateAdd, DateDiff, Year/Month/Day, etc.
- **Math**: Sum, Average, Round, Abs, Mod, Rand, etc.
- **Logic**: If, Switch, Coalesce, IsBlank, IsError, etc.
- **Navigation**: Navigate, Back, Launch, Exit
- **Form**: SubmitForm, EditForm, NewForm, ResetForm
- **Variable**: Set, UpdateContext, Collect, ClearCollect
- **AI**: AISentiment, AIClassify, AIExtract, AISummarize, AIReply, AITranslate, AIGenerateText
- **Color**: RGBA, ColorFade, ColorValue

---

## 5. Key Patterns

### Browse-Detail-Edit (3-Screen)
The classic Power Apps pattern:
1. **Browse Screen** — Gallery + search box + sort, navigate to detail on select
2. **Detail Screen** — Display form showing selected record, edit/delete buttons
3. **Edit Screen** — Edit form for create/update, save/cancel buttons

### Master-Detail (Split Screen)
- Gallery on left, form/detail on right
- `Gallery.Selected` drives the form's `Item` property

### Dashboard
- Multiple galleries/charts on one screen
- Aggregate formulas (Sum, CountRows, Average) for KPIs
- Often uses collections for pre-loaded data

### Multi-Step Form (Wizard)
- Multiple screens, each with form fields
- Store partial data in variables/collections
- Submit all at once on final screen

### Offline-Capable
- `SaveData()` / `LoadData()` for local persistence
- `Connection.Connected` to detect network status
- Queue changes locally, sync when online

### Responsive Layout
- Disable "Scale to fit" and "Lock aspect ratio"
- Use containers (horizontal/vertical) instead of fixed X/Y
- `Width = Parent.Width`, `Height = Parent.Height`
- `App.SizeBreakpoints` for responsive breakpoints

---

## 6. Deployment & Sharing

### Publishing
- Power Apps Studio → Publish → available to users
- Version history maintained, rollback available
- Environment-based (Dev, Test, Prod)

### Sharing
- Share with specific users/security groups via Power Apps portal
- Embedded in Teams (as a tab)
- Embedded in SharePoint (via web part)
- Embedded in Power BI (as a visual)
- Standalone mobile app (Power Apps mobile on iOS/Android)

### Solutions
- Package apps + flows + tables into Solutions for ALM
- Export/import between environments
- Managed vs. unmanaged solutions
- Git integration via Power Platform CLI

### .msapp Import
- Power Apps Studio → Open → Import from file → select .msapp
- Prompts to remap data source connections
- This is what our MCP server generates

---

## 7. Integration Ecosystem

| Integration | How |
|-------------|-----|
| **Power Automate** | Trigger flows from buttons, receive flow results |
| **Power BI** | Embed tiles, write-back from app to BI |
| **Copilot Studio** | Embed chatbots, extend App Header Copilot |
| **Dataverse** | Native deep integration, business rules, calculated columns |
| **SharePoint** | Lists as data source, embed app in SP pages |
| **Teams** | Publish app as Teams tab |
| **Azure** | Azure Functions, Azure SQL, Azure Blob, Azure AD |
| **Dynamics 365** | Model-driven apps share the same platform |
| **Office 365** | Outlook, Calendar, Users, Excel, OneDrive |
| **External APIs** | Custom connectors (OpenAPI/Swagger) |

---

## 8. Limitations to Know

| Area | Limitation |
|------|-----------|
| Delegation | 500-2000 record limit for non-delegable operations |
| Controls per screen | ~500 recommended max for performance |
| Screens per app | No hard limit, but 20-30 screens is practical max |
| Gallery nesting | Max 2 levels (gallery inside gallery) |
| Concurrent users | No built-in real-time collaboration (unlike web apps) |
| File size | .msapp can get large with many embedded resources |
| Custom code | No JavaScript/TypeScript (unless using PCF components) |
| Version control | Basic (publish versions), no native Git branching |
| Offline | Limited to SaveData/LoadData, no background sync |
| API rate limits | Connector-specific throttling applies |

---

## 9. When to Use Power Apps vs. Other Tools

| Scenario | Use Power Apps | Alternative |
|----------|:---:|-------------|
| Internal business app with forms/lists | ✅ | — |
| Customer-facing high-traffic web app | ❌ | React/Next.js |
| Mobile app for field workers | ✅ | — |
| Complex data visualization dashboard | ⚠️ | Power BI |
| Real-time collaboration (like Google Docs) | ❌ | Custom web app |
| Simple approval workflow | ✅ | — |
| E-commerce storefront | ❌ | Shopify/custom |
| AI chatbot for customers | ⚠️ | Copilot Studio standalone |
| Rapid prototype / internal tool | ✅ | — |
| Integration-heavy process automation | ✅ (with Power Automate) | — |
