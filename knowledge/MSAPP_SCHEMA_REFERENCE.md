# COMPLETE POWER APPS .MSAPP FILE FORMAT SCHEMA REFERENCE

This document provides a comprehensive schema reference for the Power Apps .msapp file format, based on analysis of the unpacked sample SharePoint-backed application (identifiers genericized).

---

## TABLE OF CONTENTS

1. [File Structure Overview](#file-structure-overview)
2. [Header.json](#headerjson)
3. [Properties.json](#propertiesjson)
4. [checksum.json](#checksumjson)
5. [References Directory](#references-directory)
   - [DataSources.json](#referencesdatasourcesjson)
   - [Templates.json](#referencestemplatesjson)
   - [Themes.json](#referencesthemesjson)
   - [Resources.json](#referencesresourcesjson)
   - [AuxDataMap.json](#referencesauxdatamapjson)
6. [Controls Directory](#controls-directory)
7. [Control Information Structure](#control-information-structure)
8. [Control Types Reference](#control-types-reference)
9. [Components Directory](#components-directory)
10. [ComponentsMetadata.json](#componentsmetadatajson)

---

## FILE STRUCTURE OVERVIEW

The unpacked .msapp file contains:

```
SampleApp-unpacked/
├── Header.json                 # App version and metadata
├── Properties.json             # App-level configuration and settings
├── checksum.json              # File integrity checksums
├── ComponentsMetadata.json    # Component definitions
├── AppCheckerResult.sarif     # Analysis results
├── Controls/                  # Screen and control definitions
│   ├── 1.json                # App root control
│   ├── 5.json                # Screen 1 (108 children)
│   ├── 114.json              # Screen 2 (11 children)
│   ├── 366.json
│   ├── 427.json
│   ├── 483.json
│   ├── 548.json
│   └── 664.json
├── Components/                # Component implementations
│   └── 4.json                # Component1 definition
├── References/                # Global references
│   ├── DataSources.json       # Connected data sources
│   ├── Templates.json         # Control templates
│   ├── Themes.json           # Color themes
│   ├── Resources.json        # Resource definitions
│   └── AuxDataMap.json       # Auto-generated data mappings
└── Resources/                # Binary resources
    ├── PublishInfo.json
    └── xj4tbs02.jpg
```

---

## Header.json

**Purpose**: Contains version information and basic app metadata.

**Structure**:
```json
{
  "DocVersion": "1.332",                    // Document version
  "MinVersionToLoad": "1.331",              // Minimum Power Apps version required
  "MSAppStructureVersion": "2.0",           // App structure format version
  "LastSavedDateTimeUTC": "06/30/2023 16:08:25"  // Last save timestamp
}
```

**Field Meanings**:
- `DocVersion`: The version of the document format in the Power Apps editor
- `MinVersionToLoad`: Minimum version of Power Apps required to load this app
- `MSAppStructureVersion`: Version of the .msapp file format itself (2.0 is current)
- `LastSavedDateTimeUTC`: UTC timestamp of the last save

---

## Properties.json

**Purpose**: Contains all app-level properties, settings, feature flags, and configuration.

**Key Sections**:

### Basic Info
```json
{
  "Author": "",                           // App author name
  "Name": "Task Tracker",             // App display name
  "Id": "0a4b2f5e-03e7-4357-a272-...",   // Unique app ID (GUID)
  "FileID": "0a4b2f5e-03e7-4357-a272-...",  // File ID (typically same as Id)
  "AppDescription": "",                   // App description
  "AppCreationSource": "AppFromData"      // How app was created
}
```

### Document Layout
```json
{
  "DocumentLayoutWidth": 1136,            // Canvas width in pixels
  "DocumentLayoutHeight": 640,            // Canvas height in pixels
  "DocumentLayoutOrientation": "landscape", // "portrait" or "landscape"
  "DocumentLayoutScaleToFit": true,       // Auto-scale to fit screen
  "DocumentLayoutMaintainAspectRatio": true,
  "DocumentLayoutLockOrientation": false,
  "DocumentAppType": "Phone"              // App type: "Phone", "Tablet", "Desktop"
}
```

### Connection References
```json
{
  "LocalConnectionReferences": "{...}",   // JSON string of connector references
  "LocalDatabaseReferences": "{}",        // JSON string of DB references
  "LibraryDependencies": "[]"             // Array of dependent libraries
}
```

**LocalConnectionReferences structure** (parsed JSON string):
```json
{
  "c08509b1-1d6b-4806-a09d-aec4cc081879": {
    "id": "c08509b1-1d6b-4806-a09d-aec4cc081879",
    "connectionInstanceId": "/providers/microsoft.powerapps/apis/shared_sharepointonline/connections/...",
    "dataSources": ["Task Tracker"],
    "datasets": {
      "https://contoso.sharepoint.com/sites/TaskTracker/": {
        "dataSources": {
          "Task Tracker": {
            "tableName": "d8866b71-1f31-4f44-80f4-73e30022317c"
          }
        }
      }
    },
    "dependencies": {},
    "dependents": [],
    "connectionRef": {
      "id": "/providers/microsoft.powerapps/apis/shared_sharepointonline",
      "displayName": "SharePoint",
      "apiTier": "Standard",
      "iconUri": "https://..."
    }
  }
}
```

### Control Count Map
```json
{
  "ControlCount": {
    "0f4b1301a7364e0f87fa77a8a845b869": 1,  // Component instance count
    "screen": 7,                             // 7 screens
    "rectangle": 34,                         // 34 rectangles
    "label": 441,                            // 441 labels
    "dropdown": 4,                           // etc...
    "timer": 3,
    "icon": 8,
    "button": 11,
    "group": 2,
    "form": 1,
    "typedDataCard": 48,
    "combobox": 48,
    "fluidGrid": 4,
    "dataCard": 6,
    "rating": 109,
    "gallery": 17,
    "galleryTemplate": 17
  }
}
```

### Feature Flags (AppPreviewFlagsMap)
Contains 100+ feature flags controlling behavior:
```json
{
  "delayloadscreens": true,
  "errorhandling": false,
  "blockmovingcontrol": true,
  "projectionmapping": true,
  "useguiddatatypes": true,
  "enhanceddelegation": true,
  "rtlsupport": false,
  // ... 100+ more flags
}
```

### Diagnostic Info
```json
{
  "ParserErrorCount": 0,
  "BindingErrorCount": 169,
  "ContainsThirdPartyPcfControls": false,
  "InstrumentationKey": "",
  "EnableInstrumentation": false,
  "DeserializationLoadTime": 5.3749874,
  "AnalysisLoadTime": 3.7637827
}
```

### Other Settings
```json
{
  "OriginatingVersion": "1.316",
  "DocumentType": "App",
  "ManualOfflineProfileId": "",
  "DefaultConnectedDataSourceMaxGetRowsCount": 500
}
```

---

## checksum.json

**Purpose**: Contains checksums for file integrity verification.

**Structure**:
```json
{
  "ServerStampedChecksum": "C8_Tugjhv+EliMs6Ik7pPH8iAxxhu55LqCy6+NV2fobtrg=",
  "ServerPerFileChecksums": {
    "AppCheckerResult.sarif": "C8_OvdLydi8UwAY8M3iXWsqDg5Nwt2ARKQPK5xz5VQHcNs=",
    "Components\\4.json": "C8_whRCFnqTVZJjjOuWWO+vtYiY9CJ+24alI6C7nEGMin4=",
    "Controls\\1.json": "C8_ZlATjU6e3Pq8gNpM696lFcfbFD5zpNClQof7p+/qKqI=",
    // ... one entry per file
  }
}
```

**Field Meanings**:
- `ServerStampedChecksum`: Master checksum for the entire app
- `ServerPerFileChecksums`: Map of file paths to individual checksums
- Checksums use C8 prefix (Power Apps specific format)

---

## References Directory

### References/DataSources.json

**Purpose**: Defines all connected data sources and their schemas.

**Structure**:
```json
{
  "DataSources": [
    {
      "Name": "Task Tracker",
      "IsSampleData": false,
      "IsWritable": true,
      "Type": "ConnectedDataSourceInfo",
      "DatasetName": "https://contoso.sharepoint.com/sites/TaskTracker/",
      "TableName": "d8866b71-1f31-4f44-80f4-73e30022317c",
      "ApiId": "/providers/microsoft.powerapps/apis/shared_sharepointonline",
      "EncodeDataset": true,
      "CdpRevision": {
        "RevisionNumber": 1,
        "BaseUrl": "/",
        "LastChangedTimeString": "2023-06-06T16:32:23.9260000Z"
      },
      "DataEntityMetadataJson": {
        // JSON string containing full schema with field definitions
      }
    }
  ]
}
```

**Key Fields**:
- `Name`: Display name of the data source
- `Type`: "ConnectedDataSourceInfo" or "LocalDataSourceInfo"
- `DatasetName`: URL or path to the data
- `TableName`: GUID identifying the specific table
- `ApiId`: Connector API identifier
- `DataEntityMetadataJson`: Contains the full schema (OData v3 format)
  - Fields like `ID`, `Title`, `Author`, `Created By`, etc.
  - Sortable/filterable properties
  - Filter function support
  - Server paging options

---

### References/Templates.json

**Purpose**: Contains the XML template definitions for all control types.

**Structure** (simplified):
```json
{
  "UsedTemplates": [
    {
      "Name": "rectangle",
      "Version": "2.3.0",
      "Template": "<widget ... ><!-- SVG and markup --></widget>"
    },
    {
      "Name": "button",
      "Version": "2.2.0",
      "Template": "<widget ... ><!-- Button template --></widget>"
    }
    // ... one per control type used
  ]
}
```

**Key Points**:
- Templates are XML declarations with OpenAjax spec
- Include JavaScript and CSS dependencies
- Define data-bind expressions for Knockout.js
- Specify input properties and converters
- Include accessibility attributes

---

### References/Themes.json

**Purpose**: Defines color schemes and visual themes.

**Structure**:
```json
{
  "CurrentTheme": "defaultTheme",
  "CustomThemes": [
    {
      "name": "defaultTheme",
      "palette": [
        {
          "name": "ScreenBkgColor",
          "value": "Color.White",
          "type": "c"  // 'c' = color
        },
        {
          "name": "PrimaryColor1",
          "value": "RGBA(56, 96, 178, 1)",
          "type": "c"
        },
        {
          "name": "TextMainColor",
          "value": "RGBA(0, 0, 0, 1)",
          "type": "c"
        },
        // ... 30+ color definitions
      ]
    }
  ]
}
```

**Common Theme Colors**:
- `ScreenBkgColor`: Screen background
- `PrimaryColor1/2/3`: Primary brand colors
- `TextMainColor`, `TextMainColorInverted`: Text colors
- `InputBkgColor`, `InputBorderColor`: Input styling
- `ReservedSuccessColor`, `ReservedErrorColor`: Status colors
- `HoverButtonBkgColor`: Interactive states

---

### References/Resources.json

**Purpose**: Lists external resource references.

**Structure**:
```json
{
  "Resources": []  // Empty in this app
}
```

---

### References/AuxDataMap.json

**Purpose**: Auto-generated mappings for App-From-Data (AFD) features.

**Structure**:
```json
{
  "AppFromDataMetaDataIdsToEntityNameMappings": "{
    \"%DataSourceName.AFD%\": \"Task Tracker\",
    \"%DataSourceValue.AFD%\": \"[@'Task Tracker']\",
    \"%SortFieldName.AFD%\": \"\\\"Title\\\"\",
    \"%SearchFieldName.AFD%\": \"\\\"Title\\\"\",
    \"%StartsWithFieldName.AFD%\": \"Title\",
    \"%DeleteConfirmFieldName.AFD%\": \"Title\",
    \"%SortDescending.AFD%\": \"SortDescending1\",
    \"%BrowseScreen.AFD%\": \"BrowseScreen1\",
    \"%DetailScreen.AFD%\": \"DetailScreen1\",
    \"%EditScreen.AFD%\": \"EditScreen1\",
    \"%BrowseContainer.ID%\": \"BrowseGallery1\",
    \"%DetailEditContainer.ID%\": \"EditForm1\"
  }"
}
```

**Field Meanings**:
- Maps template variables to actual screen/control names
- Used when app was generated with "App from Data" feature
- Enables automatic UI generation for CRUD operations

---

## Controls Directory

Each screen and all its controls are defined in a single JSON file.

**Files in this app**:
- `1.json` - App root (Host control)
- `5.json` - ViewScreen (108 children, galleries with rating controls)
- `114.json` - EditScreen1 (11 children, form with dataCards)
- `366.json`, `427.json`, `483.json` - Other screens
- `548.json`, `664.json` - Additional screens with galleries

---

## Control Information Structure

Every control in Controls/*.json files follows this structure:

### Top-Level Structure
```json
{
  "TopParent": {
    "Type": "ControlInfo",
    "Name": "App",  // or screen name like "EditScreen1"
    "Template": { /* ... */ },
    "Index": 0.0,
    "PublishOrderIndex": 0,
    "VariantName": "",
    "LayoutName": "",
    "MetaDataIDKey": "",
    "PersistMetaDataIDKey": false,
    "IsFromScreenLayout": false,
    "StyleName": "",
    "Parent": "",
    "IsDataControl": true,
    "AllowAccessToGlobals": true,
    "IsGroupControl": false,
    "IsAutoGenerated": false,
    "Rules": [ /* ... */ ],
    "ControlPropertyState": [ /* ... */ ],
    "IsLocked": false,
    "ControlUniqueId": "1",
    "Children": [ /* ... */ ]
  }
}
```

### Control Fields

| Field | Type | Purpose |
|-------|------|---------|
| `Type` | string | Always "ControlInfo" |
| `Name` | string | Unique name within parent |
| `HasDynamicProperties` | bool | Control has computed properties |
| `Template` | object | Template definition (see below) |
| `Index` | float | Z-order index |
| `PublishOrderIndex` | int | Publication order |
| `VariantName` | string | Design variant name |
| `LayoutName` | string | Layout variant |
| `MetaDataIDKey` | string | Metadata reference |
| `PersistMetaDataIDKey` | bool | Persist metadata flag |
| `IsFromScreenLayout` | bool | Generated from layout |
| `StyleName` | string | Applied style name |
| `Parent` | string | Parent control name |
| `IsDataControl` | bool | Can access data sources |
| `AllowAccessToGlobals` | bool | Can use global variables |
| `IsGroupControl` | bool | Is a group container |
| `IsAutoGenerated` | bool | Generated by form or gallery |
| `Rules` | array | Property definitions (see Rules section) |
| `ControlPropertyState` | array | State tracking for properties |
| `IsLocked` | bool | Locked in editor |
| `ControlUniqueId` | string | Unique numeric ID |
| `Children` | array | Child controls |

### Template Object
```json
{
  "Id": "http://microsoft.com/appmagic/button",  // Template URI
  "Version": "2.2.0",                             // Template version
  "LastModifiedTimestamp": "0",                   // Last modification
  "Name": "button",                               // Template name
  "FirstParty": true,                             // Microsoft template
  "IsPremiumPcfControl": false,                   // Not a premium PCF
  "IsCustomGroupControlTemplate": false,          // Not custom group
  "CustomGroupControlTemplateName": "",           // Custom name (if applicable)
  "IsComponentDefinition": false,                 // Not a component
  "OverridableProperties": {}                     // Props that can be overridden
}
```

### Rule Object
```json
{
  "Property": "Text",                    // Property name
  "Category": "Data",                    // Category: Data, Design, Behavior
  "InvariantScript": "\"Submit\"",       // PowerFx formula
  "RuleProviderType": "Unknown"          // Provider: Unknown, System, User
}
```

**Categories**:
- `Data`: Data binding and values (Items, Default, Text, etc.)
- `Design`: Styling and layout (Fill, Color, X, Y, Width, Height, etc.)
- `Behavior`: Event handlers (OnSelect, OnChange, OnVisible, etc.)
- `ConstantData`: Fixed data values

**RuleProviderType**:
- `Unknown`: User-defined
- `System`: Generated by system
- `User`: User-defined

---

## Control Types Reference

This app uses 15 control types. Here's the complete reference:

### 1. SCREEN

**Template**: `http://microsoft.com/appmagic/screen` (v1.0)

**Purpose**: Top-level container for controls

**Properties**:
- `Fill`: RGBA color
- `Height`: Screen height
- `Width`: Screen width
- `Orientation`: Portrait/Landscape
- `Size`: Screen size category
- `LoadingSpinner`: Loading indicator type
- `LoadingSpinnerColor`: Spinner color
- `OnVisible`: Event handler (Behavior)
- `ImagePosition`: Background image position

**Example**:
```json
{
  "Name": "EditScreen1",
  "Template": { "Name": "screen", "Version": "1.0" },
  "Rules": [
    { "Property": "Fill", "Category": "Design", "InvariantScript": "RGBA(255,255,255,1)" },
    { "Property": "Height", "Category": "Design", "InvariantScript": "640" },
    { "Property": "Width", "Category": "Design", "InvariantScript": "1136" }
  ],
  "Children": [ /* ... */ ]
}
```

---

### 2. RECTANGLE

**Template**: `http://microsoft.com/appmagic/shapes/rectangle` (v2.3.0)

**Purpose**: Shape/container for visual design

**Properties**:
- `Fill`: Background color
- `BorderColor`: Border color
- `BorderStyle`: BorderStyle.Solid, Dashed, Dotted, etc.
- `BorderThickness`: Border width in pixels
- `DisabledFill`: Color when disabled
- `HoverFill`: Color on hover
- `PressedFill`: Color when pressed
- `FocusedBorderColor`: Border when focused
- `FocusedBorderThickness`: Focused border width
- `Visible`: Boolean visibility
- `DisplayMode`: DisplayMode.Edit or View
- `X, Y, Width, Height`: Positioning/sizing
- `ZIndex`: Stacking order

**Minimal Example**:
```json
{
  "Name": "Rectangle1",
  "Template": { "Name": "rectangle", "Version": "2.3.0" },
  "Rules": [
    { "Property": "Fill", "InvariantScript": "RGBA(56, 96, 178, 1)" },
    { "Property": "Width", "InvariantScript": "150" },
    { "Property": "Height", "InvariantScript": "50" },
    { "Property": "X", "InvariantScript": "10" },
    { "Property": "Y", "InvariantScript": "20" }
  ]
}
```

---

### 3. LABEL

**Template**: `http://microsoft.com/appmagic/label` (v2.5.1)

**Purpose**: Display static or dynamic text

**Properties**:
- `Text`: Text content (string or formula)
- `Color`: Text color
- `Fill`: Background color
- `Font`: Font name (e.g., Font.'Open Sans')
- `Size`: Font size (pt)
- `FontWeight`: FontWeight.Normal, Bold, Semibold, etc.
- `Italic`: Boolean
- `Underline`: Boolean
- `Strikethrough`: Boolean
- `Align`: Align.Left, Center, Right, Justify
- `VerticalAlign`: VerticalAlign.Top, Middle, Bottom
- `AutoHeight`: Auto-expand height
- `LineHeight`: Line spacing
- `Wrap`: Text wrapping
- `Overflow`: Overflow.Hidden, Clip, etc.
- `Live`: ARIA live region
- `Role`: ARIA role
- `BorderColor`, `BorderThickness`, `BorderStyle`: Border styling
- `PaddingLeft`, `PaddingRight`, `PaddingTop`, `PaddingBottom`: Padding
- `Visible`: Visibility
- `DisplayMode`: Edit or View
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

**Example**:
```json
{
  "Name": "Label2",
  "Template": { "Name": "label", "Version": "2.5.1" },
  "Rules": [
    { "Property": "Text", "Category": "Data", "InvariantScript": "\"Welcome\"" },
    { "Property": "Color", "Category": "Design", "InvariantScript": "RGBA(0, 0, 0, 1)" },
    { "Property": "Font", "Category": "Design", "InvariantScript": "Font.'Open Sans'" },
    { "Property": "Size", "Category": "Design", "InvariantScript": "14" }
  ]
}
```

---

### 4. BUTTON

**Template**: `http://microsoft.com/appmagic/button` (v2.2.0)

**Purpose**: Interactive button with click handler

**Properties**:
- `Text`: Button label
- `OnSelect`: Event handler (formula, often navigation or actions)
- `Color`: Text color
- `Fill`: Background color
- `DisabledColor`: Text color when disabled
- `DisabledFill`: Background when disabled
- `HoverColor`: Text color on hover
- `HoverFill`: Background on hover
- `PressedColor`: Text color when pressed
- `PressedFill`: Background when pressed
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `BorderThickness`: Border width
- `DisabledBorderColor`: Border when disabled
- `HoverBorderColor`: Border on hover
- `PressedBorderColor`: Border when pressed
- `FocusedBorderColor`: Border when focused
- `FocusedBorderThickness`: Focused border width
- `Font`: Font name
- `Size`: Font size
- `FontWeight`: Font weight
- `Italic`, `Underline`, `Strikethrough`: Text styling
- `Align`: Horizontal alignment
- `VerticalAlign`: Vertical alignment
- `RadiusTopLeft`, `RadiusTopRight`, `RadiusBottomLeft`, `RadiusBottomRight`: Corner radius
- `DisplayMode`: Edit or View
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

**Example**:
```json
{
  "Name": "Button1",
  "Template": { "Name": "button", "Version": "2.2.0" },
  "Rules": [
    { "Property": "Text", "Category": "Data", "InvariantScript": "\"Submit\"" },
    { "Property": "OnSelect", "Category": "Behavior", "InvariantScript": "SubmitForm(EditForm1)" },
    { "Property": "Fill", "Category": "Design", "InvariantScript": "RGBA(56, 96, 178, 1)" },
    { "Property": "Color", "Category": "Design", "InvariantScript": "RGBA(255, 255, 255, 1)" }
  ]
}
```

---

### 5. ICON

**Template**: `http://microsoft.com/appmagic/icon` (v2.5.0)

**Purpose**: Display an icon

**Properties**:
- `Icon`: Icon name (e.g., Icon.ChevronLeft)
- `Color`: Icon color
- `Fill`: Background color
- `DisabledColor`: Color when disabled
- `DisabledFill`: Background when disabled
- `HoverColor`: Color on hover
- `HoverFill`: Background on hover
- `PressedColor`: Color when pressed
- `PressedFill`: Background when pressed
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `DisabledBorderColor`: Border when disabled
- `HoverBorderColor`: Border on hover
- `PressedBorderColor`: Border when pressed
- `FocusedBorderColor`: Border when focused
- `OnSelect`: Click handler
- `AccessibleLabel`: Accessible label for screen readers
- `Tooltip`: Tooltip text
- `TabIndex`: Tab order
- `DisplayMode`: Edit or View
- `PaddingLeft`, `PaddingRight`, `PaddingTop`, `PaddingBottom`: Padding
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

---

### 6. DROPDOWN

**Template**: `http://microsoft.com/appmagic/dropdown` (v2.3.1)

**Purpose**: Single-select dropdown list

**Properties**:
- `Items`: Array of options (formula)
- `Default`: Default selected value
- `OnChange`: Event handler when selection changes
- `Color`: Text color
- `Fill`: Background color
- `DisabledColor`: Text color when disabled
- `DisabledFill`: Background when disabled
- `HoverColor`: Text color on hover
- `HoverFill`: Background on hover
- `PressedColor`: Text color when pressed
- `PressedFill`: Background when pressed
- `SelectionColor`: Selected text color
- `SelectionFill`: Selected background color
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `BorderThickness`: Border width
- `DisabledBorderColor`: Border when disabled
- `HoverBorderColor`: Border on hover
- `PressedBorderColor`: Border when pressed
- `FocusedBorderColor`: Border when focused
- `FocusedBorderThickness`: Focused border width
- `ChevronFill`: Dropdown arrow color
- `ChevronBackground`: Dropdown arrow background
- `ChevronHoverFill`: Arrow color on hover
- `ChevronHoverBackground`: Arrow background on hover
- `ChevronDisabledFill`: Arrow color when disabled
- `ChevronDisabledBackground`: Arrow background when disabled
- `Font`: Font name
- `Size`: Font size
- `FontWeight`: Font weight
- `Italic`, `Underline`, `Strikethrough`: Text styling
- `PaddingLeft`, `PaddingRight`, `PaddingTop`, `PaddingBottom`: Padding
- `DisplayMode`: Edit or View
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

---

### 7. COMBOBOX

**Template**: `http://microsoft.com/appmagic/combobox` (v2.4.0)

**Purpose**: Searchable dropdown with multi-select capability

**Properties** (50 properties):
- `Items`: Data source array
- `SearchItems`: Formula for search results
- `SearchFields`: Fields to search in
- `DisplayFields`: Fields to display
- `NavigateFields`: Navigation field mappings
- `DefaultSelectedItems`: Pre-selected values
- `SelectMultiple`: Enable multi-select
- `IsSearchable`: Allow search input
- `Color`: Text color
- `Fill`: Background color
- `SelectionColor`: Selected text color
- `SelectionFill`: Selected item background
- `SelectionTagColor`: Tag text color
- `SelectionTagFill`: Tag background
- `MoreItemsButtonColor`: "More items" button color
- `ChevronFill`: Dropdown arrow color
- `ChevronBackground`: Arrow background
- `ChevronHoverFill`: Arrow hover color
- `ChevronHoverBackground`: Arrow hover background
- `ChevronDisabledFill`: Arrow disabled color
- `ChevronDisabledBackground`: Arrow disabled background
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `BorderThickness`: Border width
- `DisabledBorderColor`: Border when disabled
- `HoverBorderColor`: Border on hover
- `PressedBorderColor`: Border when pressed
- `FocusedBorderColor`: Border when focused
- `FocusedBorderThickness`: Focused border width
- `DisabledColor`: Text when disabled
- `DisabledFill`: Background when disabled
- `HoverColor`: Text on hover
- `HoverFill`: Background on hover
- `PressedColor`: Text when pressed
- `PressedFill`: Background when pressed
- `Font`: Font name
- `Size`: Font size
- `FontWeight`: Font weight
- `Template`: Item template
- `Tooltip`: Tooltip text
- `PaddingLeft`, `PaddingRight`, `PaddingTop`, `PaddingBottom`: Padding
- `DisplayMode`: Edit or View
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

**Example (from form dataCard)**:
```json
{
  "Name": "DataCardValue10",
  "Template": { "Name": "combobox", "Version": "2.4.0" },
  "Rules": [
    { "Property": "Items", "Category": "Data", "InvariantScript": "[@'Task Tracker']" },
    { "Property": "SearchFields", "Category": "Data", "InvariantScript": "[\"Title\"]" },
    { "Property": "DisplayFields", "Category": "Data", "InvariantScript": "[\"Title\"]" },
    { "Property": "DefaultSelectedItems", "InvariantScript": "Parent.Default" }
  ]
}
```

---

### 8. TIMER

**Template**: `http://microsoft.com/appmagic/timer` (v2.1.0)

**Purpose**: Background timer for timed events

**Properties**:
- `Start`: Start condition (boolean formula)
- `Duration`: Timer duration in milliseconds
- `OnTimerEnd`: Event handler when timer ends
- `Repeat`: Repeat timer
- `Text`: Display text (can be countdown)
- `Color`: Text color
- `Fill`: Background color
- `Font`: Font name
- `Size`: Font size
- `FontWeight`: Font weight
- `Italic`, `Underline`, `Strikethrough`: Text styling
- `Align`: Horizontal alignment
- `VerticalAlign`: Vertical alignment
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `BorderThickness`: Border width
- `DisabledBorderColor`: Border when disabled
- `DisabledColor`: Text when disabled
- `DisabledFill`: Background when disabled
- `HoverBorderColor`: Border on hover
- `HoverColor`: Text on hover
- `HoverFill`: Background on hover
- `PressedBorderColor`: Border when pressed
- `PressedColor`: Text when pressed
- `PressedFill`: Background when pressed
- `FocusedBorderColor`: Border when focused
- `FocusedBorderThickness`: Focused border width
- `DisplayMode`: Edit or View
- `Visible`: Visibility
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

---

### 9. RATING

**Template**: `http://microsoft.com/appmagic/rating` (v2.1.0)

**Purpose**: Star or numeric rating input

**Properties**:
- `Default`: Default rating value
- `RatingFill`: Color of filled stars/items
- `Fill`: Background color
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `BorderThickness`: Border width
- `DisabledBorderColor`: Border when disabled
- `DisabledFill`: Background when disabled
- `HoverFill`: Background on hover
- `PressedFill`: Background when pressed
- `FocusedBorderColor`: Border when focused
- `FocusedBorderThickness`: Focused border width
- `Tooltip`: Tooltip text
- `TabIndex`: Tab order
- `DisplayMode`: Edit or View
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

**Used in**: Form dataCards for rating fields (109 instances in this app)

**Example**:
```json
{
  "Name": "DataCardValue45",
  "Template": { "Name": "rating", "Version": "2.1.0" },
  "Rules": [
    { "Property": "Default", "InvariantScript": "Parent.Default" },
    { "Property": "RatingFill", "InvariantScript": "RGBA(56, 96, 178, 1)" }
  ]
}
```

---

### 10. FORM

**Template**: `http://microsoft.com/appmagic/form` (v2.4.0)

**Purpose**: Data-bound form with automatic field generation

**Properties**:
- `DataSource`: [@'TableName'] - Data source reference
- `DefaultMode`: FormMode.New, FormMode.Edit, or FormMode.View
- `Item`: Current record to display/edit
- `NumberOfColumns`: Columns for field layout (typically 1-3)
- `UseFluentV9Cards`: Use new Fluent design
- `OnSuccess`: Event when form submits successfully
- `Fill`: Background color
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `BorderThickness`: Border width
- `FocusedBorderColor`: Border when focused
- `FocusedBorderThickness`: Focused border width
- `AcceptsFocus`: Can receive focus
- `TabIndex`: Tab order
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

**Children**: Each field in the data source becomes a typedDataCard child

**Example**:
```json
{
  "Name": "EditForm1",
  "Template": { "Name": "form", "Version": "2.4.0" },
  "Rules": [
    { "Property": "DataSource", "Category": "Data", "InvariantScript": "[@'Task Tracker']" },
    { "Property": "DefaultMode", "Category": "Data", "InvariantScript": "FormMode.New" },
    { "Property": "NumberOfColumns", "InvariantScript": "3" },
    { "Property": "OnSuccess", "Category": "Behavior", "InvariantScript": "Back()" }
  ],
  "Children": [
    { "Name": "Ability_to_..._DataCard2", "Template": { "Name": "typedDataCard" } },
    // ... 47 more dataCards, one per field
  ]
}
```

---

### 11. TYPEDDATACARD

**Template**: `http://microsoft.com/appmagic/card` (v1.0.5)

**Purpose**: Auto-generated form field container

**Properties**:
- `DataField`: Field name from data source (encoded)
- `DisplayName`: Human-readable field name
- `Default`: Default value formula
- `Update`: Formula to save edited value
- `Required`: Is field required
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `DisplayMode`: Edit or View (usually Parent.DisplayMode)
- `Fill`: Background color
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

**Children**: Typically 4 children:
1. **Label** (field label/error indicator)
2. **Label** (field name display)
3. **Control** (combobox, rating, etc. - the actual input)
4. **Label** (error message display)

**Example**:
```json
{
  "Name": "Ability_to_liaise_..._DataCard2",
  "Template": { "Name": "typedDataCard", "Version": "1.0.5" },
  "Rules": [
    { "Property": "DataField", "InvariantScript": "\"Ability_x0020_to_x0020_liaise...\"" },
    { "Property": "DisplayName", "InvariantScript": "\"Ability to liaise across...\"" },
    { "Property": "Default", "InvariantScript": "ThisItem.'Ability to liaise...'" },
    { "Property": "Update", "InvariantScript": "DataCardValue10.Selected" },
    { "Property": "Required", "InvariantScript": "false" }
  ],
  "Children": [
    { "Name": "StarVisible9", "Template": { "Name": "label" } },
    { "Name": "DataCardKey10", "Template": { "Name": "label" } },
    { "Name": "DataCardValue10", "Template": { "Name": "combobox" } },
    { "Name": "ErrorMessage9", "Template": { "Name": "label" } }
  ]
}
```

---

### 12. DATACARD

**Template**: `http://microsoft.com/appmagic/card` (v1.0.2)

**Purpose**: Simple container card (less auto-generated than typedDataCard)

**Properties**:
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `BorderThickness`: Border width
- `DisplayMode`: Edit or View
- `Fill`: Background color
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

**Note**: Rarely used; typedDataCard is more common in modern apps

---

### 13. FLUIDGRID

**Template**: `http://microsoft.com/appmagic/fluidGrid` (v2.3.0)

**Purpose**: Responsive grid layout container

**Properties**:
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `BorderThickness`: Border width
- `DisplayMode`: Edit or View
- `Fill`: Background color
- `FocusedBorderColor`: Border when focused
- `FocusedBorderThickness`: Focused border width
- `TabIndex`: Tab order
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

---

### 14. GALLERY

**Template**: `http://microsoft.com/appmagic/gallery` (v2.13.2)

**Purpose**: Data-bound repeating container for displaying lists

**Properties**:
- `Items`: Data source array (formula)
- `Layout`: Layout.Vertical, Layout.Horizontal, etc.
- `TemplateSize`: Height/width of each item
- `TemplatePadding`: Spacing between items
- `WrapCount`: Items per row (for horizontal layout)
- `Fill`: Background color
- `BorderColor`: Border color
- `BorderStyle`: Border style
- `DisabledBorderColor`: Border when disabled
- `FocusedBorderColor`: Border when focused
- `HoverBorderColor`: Border on hover
- `PressedBorderColor`: Border when pressed
- `DisabledFill`: Background when disabled
- `HoverFill`: Background on hover
- `PressedFill`: Background when pressed
- `LoadingSpinner`: LoadingSpinner.None, Dots, Ring, etc.
- `LoadingSpinnerColor`: Spinner color
- `Transition`: Transition.None, Pop, Push, etc.
- `X, Y, Width, Height`: Positioning
- `DisplayMode`: Edit or View
- `ZIndex`: Stacking order

**Children**: 
- One **galleryTemplate** child that defines the item layout
- Template automatically repeats for each item in Items

**Example**:
```json
{
  "Name": "ML Engineer_Gallery_7",
  "Template": { "Name": "gallery", "Version": "2.13.2" },
  "Rules": [
    { "Property": "Items", "Category": "Data", "InvariantScript": "Sort(Filter(...))" },
    { "Property": "Layout", "InvariantScript": "Layout.Vertical" },
    { "Property": "TemplateSize", "InvariantScript": "68" },
    { "Property": "WrapCount", "InvariantScript": "1" }
  ],
  "Children": [
    { "Name": "galleryTemplate2_19", "Template": { "Name": "galleryTemplate" } },
    // ... other child controls
  ]
}
```

---

### 15. GALLERYTEMPLATE

**Template**: `http://microsoft.com/appmagic/galleryTemplate` (v1.0)

**Purpose**: Template definition for gallery items

**Properties**:
- `TemplateFill`: Background color of template

**Usage**: Parent gallery repeats this template for each item

**Context**: Inside the template, `ThisItem` refers to current gallery item

**Example**:
```json
{
  "Name": "galleryTemplate2_19",
  "Template": { "Name": "galleryTemplate", "Version": "1.0" },
  "Rules": [
    { "Property": "TemplateFill", "InvariantScript": "RGBA(0, 0, 0, 0)" }
  ],
  "Children": [
    { "Name": "Label4_19", "Template": { "Name": "label" } },
    { "Name": "Label5_17", "Template": { "Name": "label" } }
  ]
}
```

---

### 16. GROUP

**Template**: `http://microsoft.com/appmagic/group` (v1)

**Purpose**: Container for grouping controls

**Properties**:
- `X, Y, Width, Height`: Positioning
- `ZIndex`: Stacking order

**Note**: Minimal properties; primarily a logical container

---

### 17. COMPONENT (Custom Component)

**Template**: Custom component template with ID like `0f4b1301a7364e0f87fa77a8a845b869`

**Purpose**: Reusable custom control

**Key Fields**:
```json
{
  "IsComponentDefinition": true,
  "ComponentType": "CanvasComponent",
  "Template": {
    "Id": "http://microsoft.com/appmagic/Component",
    "Version": "637715685382820070",
    "Name": "0f4b1301a7364e0f87fa77a8a845b869",
    "IsComponentDefinition": true
  }
}
```

---

## Control Positioning and Styling Properties

### Positioning Properties
All visual controls share these:
```json
{
  "Property": "X",
  "InvariantScript": "10"  // Pixels from left
},
{
  "Property": "Y", 
  "InvariantScript": "20"  // Pixels from top
},
{
  "Property": "Width",
  "InvariantScript": "150"  // Width in pixels
},
{
  "Property": "Height",
  "InvariantScript": "40"   // Height in pixels
},
{
  "Property": "ZIndex",
  "InvariantScript": "5"    // Stacking order
}
```

### Color Properties
Common color pattern (RGBA format):
```json
{
  "Property": "Fill",
  "InvariantScript": "RGBA(56, 96, 178, 1)"  // Red, Green, Blue, Alpha (0-1)
}
```

Color formulas can also reference:
- `Color.White`, `Color.Black`, etc.
- `Theme color names` (from Themes.json)
- `ColorFade(color, percent)` - Lighten/darken
- `Self.Fill` - Reference another property
- `RGBA(r, g, b, a)` - Direct RGBA

### Border Properties
```json
{
  "Property": "BorderColor",
  "InvariantScript": "RGBA(0, 18, 107, 1)"
},
{
  "Property": "BorderStyle",
  "InvariantScript": "BorderStyle.Solid"  // Solid, Dashed, Dotted, etc.
},
{
  "Property": "BorderThickness",
  "InvariantScript": "2"  // Pixels
}
```

### Font Properties
```json
{
  "Property": "Font",
  "InvariantScript": "Font.'Open Sans'"
},
{
  "Property": "Size",
  "InvariantScript": "14"  // Points
},
{
  "Property": "FontWeight",
  "InvariantScript": "FontWeight.Semibold"
},
{
  "Property": "Italic",
  "InvariantScript": "false"
},
{
  "Property": "Underline",
  "InvariantScript": "false"
},
{
  "Property": "Strikethrough",
  "InvariantScript": "false"
}
```

---

## Control Property State

The `ControlPropertyState` array tracks which properties have been explicitly set:

```json
"ControlPropertyState": [
  "Text",
  "BorderColor",
  {
    "InvariantPropertyName": "Font",
    "AutoRuleBindingEnabled": false,
    "AutoRuleBindingString": "",
    "NameMapSourceSchema": "?",
    "IsLockable": false,
    "AFDDataSourceName": ""
  },
  // ... more entries
]
```

**Object form includes**:
- `InvariantPropertyName`: Property name
- `AutoRuleBindingEnabled`: Auto data binding enabled
- `AutoRuleBindingString`: Default binding formula
- `NameMapSourceSchema`: Schema mapping info
- `IsLockable`: Can be locked in editor
- `AFDDataSourceName`: App-From-Data source

---

## Components Directory

### Components/4.json

Component definitions use the same ControlInfo structure as screens but with:

```json
{
  "TopParent": {
    "Type": "ControlInfo",
    "Name": "Component1",
    "Template": {
      "Id": "http://microsoft.com/appmagic/Component",
      "Version": "637715685382820070",
      "LastModifiedTimestamp": "...",
      "Name": "0f4b1301a7364e0f87fa77a8a845b869",
      "IsComponentDefinition": true,
      "ComponentType": "CanvasComponent"
    },
    "Rules": [
      { "Property": "Fill", "InvariantScript": "RGBA(0, 0, 0, 0)" },
      { "Property": "Height", "InvariantScript": "640" },
      { "Property": "Width", "InvariantScript": "640" }
    ],
    "Children": [ /* component UI */ ]
  }
}
```

---

## ComponentsMetadata.json

Metadata about all components:

```json
{
  "Components": [
    {
      "Name": "Component1",
      "TemplateName": "0f4b1301a7364e0f87fa77a8a845b869",
      "Description": "",
      "AllowCustomization": true,
      "AllowAccessToGlobals": false
    }
  ]
}
```

**Fields**:
- `Name`: Display name
- `TemplateName`: Unique template ID
- `Description`: Component description
- `AllowCustomization`: Can be customized by users
- `AllowAccessToGlobals`: Can access app globals

---

## PowerFx Formula Examples

Formulas appear in the `InvariantScript` field. Common patterns:

### Navigation
```
Navigate(DetailScreen, ScreenTransition.Fade)
Navigate(Screen1, ScreenTransition.None, {selectedId: ThisItem.ID})
Back()
```

### Data Operations
```
Filter('Task Tracker', Title = "Value")
Sort(Filter(...), Title)
Search('Task Tracker', SurveySelector.Value, "Title")
```

### Forms
```
SubmitForm(EditForm1)
ResetForm(EditForm1)
SubmitForm(EditForm1); UpdateContext({go: true})
```

### Conditions
```
If(Parent.DisplayMode = DisplayMode.Edit, true, false)
DisplayMode.Edit
ThisItem.ID = 123
```

### Colors
```
RGBA(56, 96, 178, 1)
ColorFade(Self.Fill, -20%)
Self.BorderColor
```

### Control References
```
Parent.Default
ThisItem.FieldName
EditForm1.Mode
Dropdown1.Selected
```

---

## Data Source References

In Rules, data sources are referenced as:

```json
{
  "Property": "Items",
  "InvariantScript": "[@'Task Tracker']"
}
```

Or filtered:
```json
{
  "Property": "Items",
  "InvariantScript": "Filter([@'Task Tracker'], 'Field Name' = Value)"
}
```

The `[@'...']` syntax:
- `@` = Direct data source reference
- `[@'Name']` = Named data source
- `[@]` = Implicit current context

---

## Publishing Order

Controls are processed in order of `PublishOrderIndex`:
```json
"PublishOrderIndex": 290  // Order of processing
```

Lower numbers execute first. Important for initialization order.

---

## Key Patterns Summary

### Screen Pattern
```
Screen (TopParent)
├── Rectangles (decorative)
├── Labels (text)
├── Buttons (navigation/actions)
├── Gallery (data list)
│   └── GalleryTemplate
│       ├── Labels
│       └── Controls
├── Form (data entry)
│   ├── TypedDataCard
│   │   ├── Label (field label)
│   │   ├── Label (display name)
│   │   ├── ComboBox/Rating/etc (input)
│   │   └── Label (error message)
│   └── ... more dataCards
└── Timer (if needed)
```

### Control Property Hierarchy
1. **Structural** (Type, Template, Name)
2. **Layout** (X, Y, Width, Height, ZIndex)
3. **Visual** (Fill, BorderColor, Color)
4. **Interactive** (OnSelect, OnChange, DisplayMode)
5. **Data** (Items, Default, DataSource)

### Navigation Pattern
```
OnSelect event calls:
- Navigate(ScreenName, Transition)
- Back()
- Navigate with context: Navigate(Screen, Transition, {var: value})
```

### Data Binding Pattern
```
Form:
  DataSource: [@'TableName']
  Item: SingleRecordFormula
  
Gallery:
  Items: Filter([@'TableName'], condition)
  Template contains: ThisItem.FieldName
  
Label:
  Text: EditForm.DataCardValue.Value
```

---

## Summary Statistics

This sample app contains:

- **7 Screens**: Different views (Browse, Edit, Detail, etc.)
- **441 Labels**: For titles, field labels, text display
- **109 Ratings**: Rating controls
- **48 TypedDataCards**: Form fields
- **48 ComboBoxes**: Multi-select pickers
- **17 Galleries**: Data lists with templates
- **34 Rectangles**: Visual containers/shapes
- **11 Buttons**: Interactive elements
- **8 Icons**: Visual indicators
- **4 Dropdowns**: Simple selectors
- **4 FluidGrids**: Responsive layout
- **3 Timers**: Background processes
- **6 DataCards**: Simple containers
- **1 Form**: Main data entry form
- **1 Component**: Custom reusable control

**Total: ~800+ individual controls**

---

## Code Generator Implementation Notes

For building a code generator based on this schema:

1. **Traverse Controls Recursively**: Start with TopParent, process Children
2. **Template Mapping**: Map template Names to component types
3. **Rule Processing**: Parse InvariantScript formulas (PowerFx)
4. **Positioning**: Calculate absolute positions combining X, Y with parent context
5. **Data Binding**: Extract data source references from Rules
6. **Event Handlers**: Identify Behavior category Rules (OnSelect, OnChange, etc.)
7. **Styling**: Collect all Design category Rules for CSS generation
8. **Hierarchies**: Maintain parent-child relationships for containment
9. **Navigation**: Parse Navigate() calls to create screen maps
10. **Formulas**: Parse filter/sort formulas to understand data queries

The structure is highly hierarchical and composable, making it ideal for recursive code generation.

