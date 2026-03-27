# Power Apps Control Properties Reference

Complete reference of all properties for each control type found in the Task Tracker app.

---

## Property Categories

All properties fall into one of 4 categories in the Rules array:

| Category | Purpose | Examples |
|----------|---------|----------|
| **Data** | Data binding, values, content | Items, Default, Text, DataSource, DataField |
| **Design** | Styling and layout | Fill, Color, X, Y, Width, Height, BorderColor, Font |
| **Behavior** | Event handlers | OnSelect, OnChange, OnVisible, OnTimerEnd |
| **ConstantData** | Fixed/constant values | SizeBreakpoints |

---

## Universal Properties

These properties appear on virtually all controls:

```json
{
  "Property": "X",
  "Category": "Design",
  "Description": "Horizontal position in pixels from parent left"
},
{
  "Property": "Y",
  "Category": "Design",
  "Description": "Vertical position in pixels from parent top"
},
{
  "Property": "Width",
  "Category": "Design",
  "Description": "Width in pixels"
},
{
  "Property": "Height",
  "Category": "Design",
  "Description": "Height in pixels"
},
{
  "Property": "ZIndex",
  "Category": "Design",
  "Description": "Stacking order (higher = on top)"
},
{
  "Property": "DisplayMode",
  "Category": "Design",
  "Description": "DisplayMode.Edit or DisplayMode.View"
},
{
  "Property": "Visible",
  "Category": "Design",
  "Description": "Boolean visibility"
}
```

---

## Common Style Properties

Used by many controls:

```json
{
  "Property": "Fill",
  "Category": "Design",
  "Type": "Color",
  "Description": "Background color"
},
{
  "Property": "Color",
  "Category": "Design",
  "Type": "Color",
  "Description": "Text/foreground color"
},
{
  "Property": "BorderColor",
  "Category": "Design",
  "Type": "Color",
  "Description": "Border color"
},
{
  "Property": "BorderStyle",
  "Category": "Design",
  "Type": "Enum",
  "Values": ["BorderStyle.Solid", "BorderStyle.Dashed", "BorderStyle.Dotted"],
  "Description": "Border line style"
},
{
  "Property": "BorderThickness",
  "Category": "Design",
  "Type": "Number",
  "Description": "Border width in pixels"
},
{
  "Property": "DisabledFill",
  "Category": "Design",
  "Type": "Color",
  "Description": "Background when disabled"
},
{
  "Property": "DisabledColor",
  "Category": "Design",
  "Type": "Color",
  "Description": "Text color when disabled"
},
{
  "Property": "DisabledBorderColor",
  "Category": "Design",
  "Type": "Color",
  "Description": "Border color when disabled"
},
{
  "Property": "HoverFill",
  "Category": "Design",
  "Type": "Color",
  "Description": "Background on hover"
},
{
  "Property": "HoverColor",
  "Category": "Design",
  "Type": "Color",
  "Description": "Text color on hover"
},
{
  "Property": "HoverBorderColor",
  "Category": "Design",
  "Type": "Color",
  "Description": "Border color on hover"
},
{
  "Property": "PressedFill",
  "Category": "Design",
  "Type": "Color",
  "Description": "Background when pressed"
},
{
  "Property": "PressedColor",
  "Category": "Design",
  "Type": "Color",
  "Description": "Text color when pressed"
},
{
  "Property": "PressedBorderColor",
  "Category": "Design",
  "Type": "Color",
  "Description": "Border color when pressed"
},
{
  "Property": "FocusedBorderColor",
  "Category": "Design",
  "Type": "Color",
  "Description": "Border color when focused"
},
{
  "Property": "FocusedBorderThickness",
  "Category": "Design",
  "Type": "Number",
  "Description": "Border width when focused"
}
```

---

## Font Properties

Used by text-based controls (Label, Button, Dropdown, etc.):

```json
{
  "Property": "Font",
  "Category": "Design",
  "Type": "Font",
  "Format": "Font.'FontName'",
  "Examples": ["Font.'Open Sans'", "Font.'Segoe UI'"],
  "Description": "Font family"
},
{
  "Property": "Size",
  "Category": "Design",
  "Type": "Number",
  "Unit": "Points",
  "Description": "Font size"
},
{
  "Property": "FontWeight",
  "Category": "Design",
  "Type": "Enum",
  "Values": [
    "FontWeight.Normal",
    "FontWeight.Semibold",
    "FontWeight.Bold"
  ],
  "Description": "Font weight"
},
{
  "Property": "Italic",
  "Category": "Design",
  "Type": "Boolean",
  "Description": "Italic text"
},
{
  "Property": "Underline",
  "Category": "Design",
  "Type": "Boolean",
  "Description": "Underlined text"
},
{
  "Property": "Strikethrough",
  "Category": "Design",
  "Type": "Boolean",
  "Description": "Strikethrough text"
},
{
  "Property": "Align",
  "Category": "Design",
  "Type": "Enum",
  "Values": [
    "Align.Left",
    "Align.Center",
    "Align.Right",
    "Align.Justify"
  ],
  "Description": "Horizontal text alignment"
},
{
  "Property": "VerticalAlign",
  "Category": "Design",
  "Type": "Enum",
  "Values": [
    "VerticalAlign.Top",
    "VerticalAlign.Middle",
    "VerticalAlign.Bottom"
  ],
  "Description": "Vertical text alignment"
}
```

---

## Control-Specific Properties by Type

### SCREEN

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `Fill` | Design | Color | Screen background |
| `Height` | Design | Number | Screen height |
| `Width` | Design | Number | Screen width |
| `OnVisible` | Behavior | Formula | Fires when screen becomes visible |
| `Orientation` | Design | Enum | Portrait/Landscape |
| `Size` | Design | Enum | Screen size category |
| `LoadingSpinner` | Design | Enum | Loading indicator type |
| `LoadingSpinnerColor` | Design | Color | Spinner color |
| `ImagePosition` | Design | Enum | Background image position |

### LABEL

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `Text` | Data | String/Formula | Display text |
| `AutoHeight` | Design | Boolean | Auto-expand height |
| `LineHeight` | Design | Number | Line spacing |
| `Wrap` | Design | Boolean | Text wrapping |
| `Overflow` | Design | Enum | Overflow behavior |
| `Live` | Design | Enum | ARIA live region |
| `Role` | Design | Enum | ARIA role |
| `PaddingLeft` | Design | Number | Left padding |
| `PaddingRight` | Design | Number | Right padding |
| `PaddingTop` | Design | Number | Top padding |
| `PaddingBottom` | Design | Number | Bottom padding |

### BUTTON

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `Text` | Data | String | Button label |
| `OnSelect` | Behavior | Formula | Click handler |
| `RadiusTopLeft` | Design | Number | Top-left corner radius |
| `RadiusTopRight` | Design | Number | Top-right corner radius |
| `RadiusBottomLeft` | Design | Number | Bottom-left corner radius |
| `RadiusBottomRight` | Design | Number | Bottom-right corner radius |
| All common color properties | Design | Color | Fill, Color, Border, Hover states |

### DROPDOWN

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `Items` | Data | Array | Option list |
| `Default` | Data | Any | Default selection |
| `OnChange` | Behavior | Formula | Selection change handler |
| `ChevronFill` | Design | Color | Dropdown arrow color |
| `ChevronBackground` | Design | Color | Arrow background |
| `ChevronHoverFill` | Design | Color | Arrow color on hover |
| `ChevronDisabledFill` | Design | Color | Arrow color when disabled |
| `SelectionColor` | Design | Color | Selected text color |
| `SelectionFill` | Design | Color | Selected background color |
| `PaddingLeft` | Design | Number | Left padding |
| `PaddingRight` | Design | Number | Right padding |
| `PaddingTop` | Design | Number | Top padding |
| `PaddingBottom` | Design | Number | Bottom padding |

### COMBOBOX

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `Items` | Data | Array | Data source array |
| `SearchItems` | Data | Formula | Search results formula |
| `SearchFields` | Data | Array | Fields to search |
| `DisplayFields` | Data | Array | Fields to display |
| `NavigateFields` | Data | Object | Field navigation mappings |
| `DefaultSelectedItems` | Data | Array | Pre-selected items |
| `SelectMultiple` | Data | Boolean | Allow multiple selection |
| `IsSearchable` | Data | Boolean | Allow search input |
| `SelectionColor` | Design | Color | Selected text color |
| `SelectionFill` | Design | Color | Selected background |
| `SelectionTagColor` | Design | Color | Tag text color |
| `SelectionTagFill` | Design | Color | Tag background |
| `MoreItemsButtonColor` | Design | Color | "More items" button color |
| `Template` | Data | Object | Item template |
| `Tooltip` | Design | String | Tooltip text |
| All padding/chevron properties | Design | Number/Color | Styling |

### ICON

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `Icon` | Data | Enum | Icon name (e.g., Icon.ChevronLeft) |
| `OnSelect` | Behavior | Formula | Click handler |
| `AccessibleLabel` | Design | String | Screen reader label |
| `Tooltip` | Design | String | Tooltip text |
| `TabIndex` | Design | Number | Tab order |
| `PaddingLeft` | Design | Number | Left padding |
| `PaddingRight` | Design | Number | Right padding |
| `PaddingTop` | Design | Number | Top padding |
| `PaddingBottom` | Design | Number | Bottom padding |
| All common color properties | Design | Color | Fill, Color, Border states |

### RECTANGLE

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `Fill` | Design | Color | Background color |
| `BorderColor` | Design | Color | Border color |
| `BorderStyle` | Design | Enum | Border style |
| `BorderThickness` | Design | Number | Border width |
| `DisabledFill` | Design | Color | Background when disabled |
| `HoverFill` | Design | Color | Background on hover |
| `PressedFill` | Design | Color | Background when pressed |
| `Visible` | Design | Boolean | Visibility |

### FORM

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `DataSource` | Data | DataSource | Connected data source |
| `Item` | Data | Record | Current record |
| `DefaultMode` | Data | Enum | FormMode.New, Edit, View |
| `NumberOfColumns` | Design | Number | Column layout (1-3) |
| `UseFluentV9Cards` | Design | Boolean | Use new design cards |
| `OnSuccess` | Behavior | Formula | Success handler |
| `Fill` | Design | Color | Background |
| `BorderColor` | Design | Color | Border color |
| `BorderStyle` | Design | Enum | Border style |
| `BorderThickness` | Design | Number | Border width |
| `AcceptsFocus` | Design | Boolean | Can accept focus |
| `TabIndex` | Design | Number | Tab order |

### TYPEDDATACARD

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `DataField` | Data | String | Field name from source |
| `DisplayName` | Data | String | Human-readable field name |
| `Default` | Data | Formula | Default value |
| `Update` | Data | Formula | Update formula |
| `Required` | Data | Boolean | Field is required |
| `BorderColor` | Design | Color | Border color |
| `BorderStyle` | Design | Enum | Border style |
| `DisplayMode` | Design | Enum | Edit or View (usually Parent.DisplayMode) |
| `Fill` | Design | Color | Background |

### GALLERY

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `Items` | Data | Array | Data source |
| `Layout` | Design | Enum | Layout.Vertical, Horizontal |
| `TemplateSize` | Design | Number | Item height/width |
| `TemplatePadding` | Design | Number | Spacing between items |
| `WrapCount` | Design | Number | Items per row |
| `LoadingSpinner` | Design | Enum | Spinner type |
| `LoadingSpinnerColor` | Design | Color | Spinner color |
| `Transition` | Design | Enum | Transition effect |
| `Fill` | Design | Color | Background |
| `BorderColor` | Design | Color | Border color |
| `BorderStyle` | Design | Enum | Border style |
| All state color properties | Design | Color | Disabled, Hover, Pressed |

### GALLERYTEMPLATE

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `TemplateFill` | Design | Color | Template background |

**Note**: Inside galleryTemplate, use `ThisItem` to reference current gallery item.

### RATING

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `Default` | Data | Number | Default rating value |
| `RatingFill` | Design | Color | Filled stars/items color |
| `Fill` | Design | Color | Background |
| `BorderColor` | Design | Color | Border color |
| `BorderStyle` | Design | Enum | Border style |
| `BorderThickness` | Design | Number | Border width |
| `Tooltip` | Design | String | Tooltip text |
| `TabIndex` | Design | Number | Tab order |
| All state color properties | Design | Color | Disabled, Hover, Pressed |

### TIMER

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `Start` | Data | Boolean | Start condition |
| `Duration` | Data | Number | Duration in milliseconds |
| `OnTimerEnd` | Behavior | Formula | End handler |
| `Repeat` | Data | Boolean | Repeat timer |
| `Text` | Data | String | Display text |
| All font properties | Design | Font | Font family, size, weight |
| All common color/border properties | Design | Color | Styling |

### DATACARD

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `BorderColor` | Design | Color | Border color |
| `BorderStyle` | Design | Enum | Border style |
| `BorderThickness` | Design | Number | Border width |
| `DisplayMode` | Design | Enum | Edit or View |
| `Fill` | Design | Color | Background |

### FLUIDGRID

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `BorderColor` | Design | Color | Border color |
| `BorderStyle` | Design | Enum | Border style |
| `BorderThickness` | Design | Number | Border width |
| `DisplayMode` | Design | Enum | Edit or View |
| `Fill` | Design | Color | Background |
| `FocusedBorderColor` | Design | Color | Border when focused |
| `FocusedBorderThickness` | Design | Number | Border width when focused |
| `TabIndex` | Design | Number | Tab order |

### GROUP

| Property | Category | Type | Description |
|----------|----------|------|-------------|
| `X` | Design | Number | Horizontal position |
| `Y` | Design | Number | Vertical position |
| `Width` | Design | Number | Width |
| `Height` | Design | Number | Height |
| `ZIndex` | Design | Number | Stacking order |

---

## Formula Value Examples

### Color Values
```
RGBA(56, 96, 178, 1)           // Direct RGB with alpha (0-1)
Color.White                     // Named color
Self.Fill                       // Reference another property
ColorFade(RGBA(56, 96, 178, 1), -20%)  // Lighten/darken (%)
Parent.Fill                     // Parent property
Theme.PrimaryColor1             // Theme reference
```

### Data References
```
[@'Task Tracker']           // Named data source
Filter([@'Table'], 'Field' = Value)  // Filtered array
Sort(Items, Title)              // Sorted items
Search(Items, SearchTerm, "Title")   // Search results
ThisItem.FieldName              // Gallery item field
Parent.Default                  // Parent property
```

### Control References
```
Button1.OnSelect                // Control property
EditForm1.Mode                  // Form mode
Dropdown1.Selected              // Selected value
Gallery1.AllItems               // All gallery items
DataCardValue.Value             // Card value
```

### Event Handlers
```
Navigate(Screen2, ScreenTransition.Fade)     // Navigate
SubmitForm(EditForm1)                         // Submit form
ResetForm(EditForm1)                          // Reset form
Back()                                        // Back navigation
SubmitForm(EditForm1); UpdateContext({go:true})  // Multiple actions
If(condition, action1, action2)              // Conditional
```

### Display Modes
```
DisplayMode.Edit                // Edit mode
DisplayMode.View                // View mode
FormMode.New                    // New record
FormMode.Edit                   // Edit record
FormMode.View                   // View record
```

---

## Property Value Formats

### Boolean
```json
true
false
```

### Number
```json
10
150.5
0
```

### String (quoted)
```json
"Submit"
"Enter your name"
```

### Array
```json
["Option1", "Option2", "Option3"]
[@'DataSource']
```

### Enum
```json
DisplayMode.Edit
Align.Center
BorderStyle.Solid
Layout.Vertical
```

### Formula
```json
Filter([@'Table'], Field = Value)
If(Condition, TrueValue, FalseValue)
Concatenate(Str1, Str2)
```

---

## Common Pattern: Data Card Structure

Form DataCards typically have this structure:

```
TypedDataCard (parent)
├── Label (star indicator) - marks required fields
├── Label (field name display) - shows DisplayName
├── ComboBox/Rating/etc (the actual input control)
└── Label (error message) - shows validation errors
```

Each dataCard has:
- `DataField`: SharePoint column name (URL-encoded)
- `DisplayName`: Human-readable label
- `Default`: = ThisItem.'FieldName'
- `Update`: = ChildControl.Selected (or .Value)
- `Required`: false or true
- `DisplayMode`: Parent.DisplayMode (inherits from form)

---

## Navigation Patterns

### Simple Navigation
```
Navigate(DetailScreen1)
Navigate(BrowseScreen1, ScreenTransition.Fade)
Back()
```

### Navigate with Context
```
Navigate(DetailScreen1, ScreenTransition.Fade, {selectedItem: ThisItem})
```

### Conditional Navigation
```
If(EditForm1.Mode = FormMode.New, 
   Navigate(Screen1),
   Navigate(DetailScreen1)
)
```

---

## This document provides the complete property reference for building a Power Apps code generator.

