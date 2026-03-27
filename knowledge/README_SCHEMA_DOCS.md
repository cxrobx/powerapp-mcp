# Power Apps .MSAPP File Format - Complete Schema Documentation

This documentation package contains the complete technical specification for the Power Apps .msapp file format based on comprehensive analysis of the "Task Tracker" application.

## Documents Included

### 1. MSAPP_SCHEMA_REFERENCE.md
**Main comprehensive reference document**

Covers:
- Complete file structure and directory layout
- Every file type: Header.json, Properties.json, checksum.json
- All reference directories and their purposes
- Complete control information structure specification
- 17 control types with full property documentation
- Component and metadata definitions
- Formula and data binding patterns
- Practical code generator implementation notes

**Use this for**: Understanding the overall structure, learning about specific file formats, implementing a parser

### 2. CONTROL_TYPES_JSON_SCHEMA.json
**JSON Schema (v7) definition for validation**

Contains:
- Complete ControlInfo schema definition
- Template object specification
- Rule definition format
- PropertyState tracking objects
- Real-world examples of button controls and screen structures
- Ready for JSON schema validation tools

**Use this for**: Validating JSON files, IDE code completion, schema validation in tools

### 3. CONTROL_PROPERTIES_REFERENCE.md
**Detailed property lookup tables**

Contains:
- Property categorization system (Data, Design, Behavior, ConstantData)
- Universal properties (X, Y, Width, Height, etc.)
- Common style properties across all controls
- Font property specifications
- Complete property tables for each control type
- Formula value examples with syntax
- Property value formats and their interpretation
- Common patterns for data cards and navigation

**Use this for**: Looking up specific properties, understanding property values, writing formulas

---

## Quick Start: Understanding the Format

### File Structure Pattern

Every .msapp file when unpacked contains:

```
App Root (Header.json, Properties.json, etc.)
├── Controls/
│   ├── 1.json (App + Host control)
│   ├── N.json (Screen 1)
│   ├── M.json (Screen 2)
│   └── ... more screens
├── Components/
│   └── X.json (Custom component definition)
├── References/
│   ├── DataSources.json (All connected data)
│   ├── Templates.json (Control templates)
│   ├── Themes.json (Color schemes)
│   ├── Resources.json (External resources)
│   └── AuxDataMap.json (AFD mappings)
└── Resources/
    └── Binary files (images, etc.)
```

### Control Hierarchy Pattern

Every screen follows this recursive structure:

```json
{
  "TopParent": {
    "Type": "ControlInfo",
    "Name": "ScreenName",
    "Template": { ... },
    "Rules": [ ... ],
    "Children": [
      {
        "Type": "ControlInfo",
        "Name": "Control1",
        "Template": { ... },
        "Rules": [ ... ],
        "Children": [ ... ]
      }
    ]
  }
}
```

Every control has:
- **Type**: Always "ControlInfo"
- **Name**: Unique within parent (e.g., "Button1", "EditForm1")
- **Template**: Control type definition (link, version, name)
- **Rules**: Property definitions in [Property, Category, InvariantScript, RuleProviderType] format
- **Children**: Nested controls (recursive)

### Property Definition Pattern

Each property is defined as a Rule:

```json
{
  "Property": "PropertyName",
  "Category": "Design",           // or Data, Behavior, ConstantData
  "InvariantScript": "Value",     // Literal value or PowerFx formula
  "RuleProviderType": "Unknown"   // Unknown, System, or User
}
```

Examples:
```json
{ "Property": "Text", "Category": "Data", "InvariantScript": "\"Submit\"" }
{ "Property": "X", "Category": "Design", "InvariantScript": "100" }
{ "Property": "Fill", "Category": "Design", "InvariantScript": "RGBA(56, 96, 178, 1)" }
{ "Property": "OnSelect", "Category": "Behavior", "InvariantScript": "Navigate(Screen2)" }
```

---

## Control Types Reference

This app includes **17 control types**:

### Core Controls
- **Screen**: Container for entire screen/page
- **Label**: Text display (441 instances in this app)
- **Button**: Interactive clickable element (11 instances)
- **Icon**: Icon display (8 instances)
- **Rectangle**: Shape/decorative container (34 instances)

### Input Controls
- **Dropdown**: Single-select list (4 instances)
- **ComboBox**: Multi-select searchable list (48 instances)
- **Rating**: Star/numeric rating input (109 instances)
- **Timer**: Background timer for events (3 instances)

### Data Container Controls
- **Form**: Auto-generated form for data entry (1 instance)
- **TypedDataCard**: Auto-generated form field container (48 instances)
- **DataCard**: Simple data container card (6 instances)
- **Gallery**: Repeating data list (17 instances)
- **GalleryTemplate**: Template for gallery items (17 instances)

### Layout Controls
- **FluidGrid**: Responsive grid container (4 instances)
- **Group**: Simple container/grouping (2 instances)

### Custom
- **Component**: Custom reusable control (1 instance of Component1)

---

## Data Binding Patterns

### Form Pattern
```
Screen
└── Form (DataSource: [@'TableName'])
    ├── TypedDataCard (DataField: "FieldName")
    │   ├── Label (field label)
    │   ├── ComboBox/Rating/etc (input control)
    │   └── Label (error message)
    └── ... more dataCards
```

### Gallery Pattern
```
Screen
└── Gallery (Items: Filter([@'TableName'], condition))
    └── GalleryTemplate (TemplateFill: color)
        ├── Label (ThisItem.FieldName)
        ├── Button (OnSelect: Navigate(...))
        └── ... more controls
```

### Navigation Pattern
```
Button1
└── OnSelect: Navigate(Screen2, ScreenTransition.Fade)

OR for context passing:
└── OnSelect: Navigate(DetailScreen, ScreenTransition.Fade, {item: ThisItem})
```

---

## Property Categories

### Data Category (Binding & Content)
Contains data-related properties:
- Items, Default, Text, Value
- DataSource, DataField
- Selected, SearchItems, DisplayFields
- Custom formulas

### Design Category (Styling & Layout)
Contains visual and layout properties:
- X, Y, Width, Height, ZIndex
- Fill, Color, BorderColor, BorderStyle, BorderThickness
- Font, Size, FontWeight, Italic, Underline
- Visible, DisplayMode
- All state-based colors (Hover, Pressed, Disabled, Focused)

### Behavior Category (Events)
Contains event handlers:
- OnSelect (button clicks, icon clicks)
- OnChange (dropdown/combobox selection)
- OnVisible (screen load)
- OnTimerEnd (timer completion)
- OnSuccess (form submission)

### ConstantData Category
Special category for fixed values:
- SizeBreakpoints
- MinScreenWidth, MinScreenHeight

---

## Color Value Format

Colors use RGBA format: `RGBA(Red, Green, Blue, Alpha)`

```
RGBA(56, 96, 178, 1)           // Red=56, Green=96, Blue=178, Fully opaque
RGBA(56, 96, 178, 0.5)         // Same color with 50% transparency
RGBA(255, 255, 255, 1)         // White
RGBA(0, 0, 0, 1)               // Black
```

Color references:
```
Color.White                     // Named color
Color.Black
RGBA(...) expressions           // Direct RGBA
ColorFade(color, %)            // Lighten/darken: positive = darker, negative = lighter
Self.Fill                       // Reference another property
Parent.Fill                     // Reference parent property
Theme.PrimaryColor1             // Reference theme color
```

---

## Data Source References

Data sources are referenced with special syntax:

```
[@'DataSourceName']             // Direct reference
Filter([@'Table'], 'Field' = Value)   // Filtered
Sort([@'Table'], 'Field')       // Sorted
Search([@'Table'], Term, 'Field')     // Searched
```

Inside gallery/form items:
```
ThisItem.FieldName              // Current item field
ThisItem.'Field with spaces'    // Fields with spaces (quoted)
```

---

## Checksum Mechanism

The checksum.json file contains:
1. **ServerStampedChecksum**: Master checksum for entire app
2. **ServerPerFileChecksums**: Individual checksums for each file

Format: `C8_` prefix + base64-encoded SHA-256 hash

Purpose: File integrity verification during publish/deploy

---

## Feature Flags (AppPreviewFlagsMap)

Properties.json includes 100+ feature flags that control runtime behavior:

Common flags:
- `delayloadscreens`: Lazy load screens
- `enhanceddelegation`: Query optimization
- `rtlsupport`: Right-to-left language support
- `namedformulas`: Named formula support
- `enablecopilotcontrol`: Copilot integration
- `mobilenativerendering`: Native mobile rendering

Each flag is a boolean affecting specific behaviors.

---

## Implementation Guide for Code Generators

To build a code generator based on this specification:

### 1. Parse Structure
```python
def parse_control_file(filepath):
    with open(filepath) as f:
        data = json.load(f)
    return traverse_controls(data['TopParent'])

def traverse_controls(control):
    # Process this control
    # Then recursively process children
    for child in control.get('Children', []):
        traverse_controls(child)
```

### 2. Extract Properties
```python
def extract_properties(control):
    properties = {}
    for rule in control['Rules']:
        properties[rule['Property']] = {
            'value': rule['InvariantScript'],
            'category': rule['Category']
        }
    return properties
```

### 3. Map Templates
```python
template_mapping = {
    'screen': Screen,
    'button': Button,
    'label': Label,
    'form': Form,
    'gallery': Gallery,
    # ... etc
}
```

### 4. Generate Output
For each control:
1. Get template type
2. Extract properties by category
3. Handle parent-child relationships
4. Parse formulas in InvariantScript
5. Generate target code (HTML, React, Vue, etc.)

### 5. Handle Special Cases
- Forms: Extract field metadata from typedDataCards
- Galleries: Extract template layout
- Navigation: Parse Navigate() formulas
- Data binding: Extract Filter/Sort/Search formulas

---

## Known Patterns

### Auto-Generated Content
Certain controls are auto-generated:
- **Forms**: Generate typedDataCards automatically from data source schema
- **Galleries**: Generate template layout based on data
- **App From Data (AFD)**: Auto-generates screens and fields

These are marked with `"IsAutoGenerated": true`

### Component Definition vs Instance
- **Component Definition**: In Components/X.json with `"IsComponentDefinition": true`
- **Component Instance**: Referenced in Controls/N.json by template ID

### Template Versions
Each control template has a version (e.g., "2.2.0" for button, "1.0" for screen)
Versions indicate template compatibility and feature set.

---

## File Statistics: Task Tracker App

This reference app contains:
- **7 Screens**: Different pages/views
- **441 Labels**: Text displays
- **109 Ratings**: Rating controls
- **48 TypedDataCards**: Form fields
- **48 ComboBoxes**: Multi-select inputs
- **17 Galleries**: Data lists
- **34 Rectangles**: Decorative shapes
- **11 Buttons**: Interactive elements
- **8 Icons**: Visual indicators
- **4 Dropdowns**: Single select lists
- **4 FluidGrids**: Responsive layouts
- **3 Timers**: Background timers
- **6 DataCards**: Simple containers
- **1 Form**: Main data entry form
- **1 Component**: Custom reusable control

**Total: ~800+ individual controls**

---

## Using These Documents

### For Understanding the Format
1. Start with **MSAPP_SCHEMA_REFERENCE.md** Section: "File Structure Overview"
2. Read the control types section relevant to your work
3. Reference specific properties in **CONTROL_PROPERTIES_REFERENCE.md**

### For Implementing a Parser
1. Review **CONTROL_TYPES_JSON_SCHEMA.json** for structure validation
2. Use **MSAPP_SCHEMA_REFERENCE.md** for detailed field meanings
3. Implement recursive control traversal

### For Writing Formulas
1. Check **CONTROL_PROPERTIES_REFERENCE.md** "Formula Value Examples" section
2. Understand property categories and data binding patterns
3. Reference the navigation and data source patterns

### For Validating Generated Files
1. Use **CONTROL_TYPES_JSON_SCHEMA.json** with a JSON schema validator
2. Ensure all required fields are present
3. Verify template IDs and versions match known templates

---

## Additional Resources

### Related Technologies
- **PowerFx**: Formula language used in InvariantScript
- **OpenAjax**: Template specification format (in Templates.json)
- **SharePoint**: Common data source connector
- **OData v3**: Data schema format in DataSources.json
- **Knockout.js**: Data binding library used in templates

### Version Information
- **App Format**: MSAppStructureVersion 2.0
- **Template System**: Version 1.0 (Screen), 2.x (Most controls)
- **Scope**: Power Apps 1.332+ (DocVersion)

---

## Notes

This documentation is based on the sample application (identifiers genericized), a SharePoint-backed Power App with:
- Complex multi-screen navigation
- Data-bound forms and galleries
- 50+ fields with ratings and multi-select
- Custom styling and theming
- 100+ feature flags enabled

The patterns documented here represent current best practices and cover the most common control types used in Power Apps.

