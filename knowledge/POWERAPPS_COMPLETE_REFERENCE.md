# Power Apps Comprehensive Knowledge Base

## Purpose
This document serves as a comprehensive reference for building an MCP server that generates Power Apps .msapp files programmatically from natural language descriptions.

---

## 1. CANVAS APP ARCHITECTURE

### App Structure (from YAML schema and tooling)
A Power Apps canvas app (.msapp file) is a ZIP archive containing:
- **Controls**: Defined hierarchically (Screens > child controls)
- **Properties**: Key-value pairs on each control (formulas or static values)
- **Data Sources**: Connection references to external data
- **Components**: Reusable control groups with custom properties
- **Resources**: Images, media, and other assets

### YAML Schema Structure (from microsoft/PowerApps-Tooling)
Each control in the YAML representation has:
```yaml
ControlName:
  Control: <ControlType>     # Required - e.g., "Classic/Button"
  Variant: <string>          # Optional variant
  Layout: <string>           # Optional layout mode
  Properties:                # Key-value property definitions
    PropertyName: =<formula> # Formula prefixed with =
    PropertyName: "value"    # Static value
  Children:                  # Array of child ControlDefs
    - ChildControl:
        Control: <type>
        Properties: ...
  ComponentName: <string>    # For component instances
  ComponentLibraryUniqueName: <string>
  CustomProperties: []       # For component definitions
  Settings: {}
  Style: <string>
```

### Power Fx Language
- **Declarative, functional language** inspired by Excel formulas
- **Strong typing** with type inference
- **No equals prefix** (unlike Excel, formulas don't start with =)
- **Semicolon chaining** for behavior formulas: `Action1(); Action2()`
- **Dot notation** for property access: `Control.Property`
- **String interpolation**: `$"Hello {Name}"`
- **Locale-sensitive**: decimal separator affects list separator and chaining operator

---

## 2. ALL CONTROL TYPES

### Display Controls
| Control Type | Internal Name | Description |
|---|---|---|
| **Label** | `text-box` / `Classic/Label` | Shows text, numbers, dates, currency |
| **HTML text** | `htmlViewer` | Renders HTML content |
| **Rich text editor** | `richTextEditor` | Rich text formatting input |
| **Image** | `image` | Shows image from file, URL, or data source |
| **Shape** | `shape` | Arrows and geometric shapes (rectangles, etc.) |
| **Icon** | `icon` | Graphic icons from built-in library |

### Input Controls
| Control Type | Internal Name | Description |
|---|---|---|
| **Button** | `button` / `Classic/Button` | Clickable/tappable action trigger |
| **Text input** | `textInput` / `Classic/TextInput` | Single/multi-line text entry (also Password mode) |
| **Drop down** | `dropDown` | Single-select list (collapsed by default) |
| **Combo box** | `comboBox` | Searchable, multi-select dropdown |
| **Date picker** | `datePicker` | Calendar-based date selection |
| **Check box** | `checkbox` | Boolean true/false toggle |
| **Toggle** | `toggle` | On/off switch (same as checkbox, different UI) |
| **Slider** | `slider` | Drag handle between min/max values |
| **Rating** | `rating` | Star rating (1 to Max) |
| **Radio** | `radio` | Mutually exclusive option buttons |
| **List box** | `listBox` | Visible multi-select list |
| **Pen input** | `penInput` | Draw/handwrite input |

### Data Controls
| Control Type | Internal Name | Description |
|---|---|---|
| **Gallery** | `gallery` | Repeating template showing list of records |
| **Data table** | `dataTable` | Tabular data display (read-only) |
| **Edit form** | `formViewer` (Edit) | Edit/create records from data source |
| **Display form** | `formViewer` (View) | Read-only record display |
| **Card** | `card` | Individual field in a form |

### Media Controls
| Control Type | Internal Name | Description |
|---|---|---|
| **Audio** | `audioPlayback` | Play audio clips |
| **Video** | `videoPlayback` | Play video (local, data source, YouTube) |
| **Camera** | `camera` | Capture photos |
| **Microphone** | `microphone` | Record audio |
| **Add picture** | `addPicture` | Upload images from device |
| **Stream Video** | `streamVideo` | Microsoft Stream video playback |
| **Barcode reader** | `barcodeReader` | Scan barcodes/QR codes |

### Layout Controls
| Control Type | Internal Name | Description |
|---|---|---|
| **Screen** | `screen` | Top-level container, one per page |
| **Horizontal container** | `horizontalAutoLayout` | Auto-layout horizontal (flexbox-like) |
| **Vertical container** | `verticalAutoLayout` | Auto-layout vertical (flexbox-like) |
| **Container** | `container` | Manual-layout nested container |
| **Grid container** | `gridContainer` | CSS Grid-like layout |

### Chart Controls
| Control Type | Internal Name | Description |
|---|---|---|
| **Column chart** | `columnChart` | Vertical bar chart |
| **Line chart** | `lineChart` | Line/trend chart |
| **Pie chart** | `pieChart` | Pie/donut chart |

### Integration Controls
| Control Type | Internal Name | Description |
|---|---|---|
| **Power BI tile** | `powerBiTile` | Embed Power BI visual |
| **PDF viewer** | `pdfViewer` | Display PDF documents |
| **Map** | `map` | Display geographic map with markers |
| **Export** | `export` | Export data to file |
| **Import** | `import` | Import data from file |

### Mixed Reality Controls
| Control Type | Internal Name | Description |
|---|---|---|
| **3D object** | `3dObject` | View/rotate 3D models |
| **Measuring Camera** | `measuringCamera` | Measure distance/area in MR |
| **View in MR** | `viewInMR` | Place items in physical space |
| **View shape in MR** | `viewShapeInMR` | Place shapes in physical space |

### Other Controls
| Control Type | Description |
|---|---|
| **Timer** | Trigger actions after time passes |
| **Attachments** | Download/upload files to data source |
| **Address input** | Dynamic address suggestions |
| **Column** | Display field in Data table |
| **Web barcode scanner** | Legacy browser-based scanner |

---

## 3. ALL CONTROL PROPERTIES

### Universal Properties (apply to nearly all controls)
```
X, Y                    - Position (pixels from parent left/top edge)
Width, Height           - Size in pixels
Visible                 - Boolean, show/hide
DisplayMode             - Edit | View | Disabled
Fill                    - Background color (RGBA)
BorderColor             - Border color
BorderStyle             - Solid | Dashed | Dotted | None
BorderThickness         - Border width in pixels
Tooltip                 - Hover text
TabIndex                - Keyboard navigation order
```

### Text Properties (Label, Button, TextInput, etc.)
```
Text                    - Display text or formula
Color                   - Text color
Font                    - Font family name
FontWeight              - Bold | Semibold | Normal | Lighter
Size                    - Font size (points)
Align                   - Left | Center | Right (horizontal)
VerticalAlign           - Top | Middle | Bottom
Italic                  - Boolean
Underline               - Boolean
Strikethrough           - Boolean
LineHeight              - Line spacing
```

### Interactive State Properties
```
HoverBorderColor        - Border on mouse hover
HoverColor              - Text on mouse hover
HoverFill               - Background on mouse hover
PressedBorderColor      - Border when pressed
PressedColor            - Text when pressed
PressedFill             - Background when pressed
DisabledBorderColor     - Border when disabled
DisabledColor           - Text when disabled
DisabledFill            - Background when disabled
FocusedBorderColor      - Border when focused
FocusedBorderThickness  - Border thickness when focused
```

### Spacing Properties
```
PaddingTop              - Inner top spacing
PaddingBottom           - Inner bottom spacing
PaddingLeft             - Inner left spacing
PaddingRight            - Inner right spacing
RadiusTopLeft           - Corner rounding (top-left)
RadiusTopRight          - Corner rounding (top-right)
RadiusBottomLeft        - Corner rounding (bottom-left)
RadiusBottomRight       - Corner rounding (bottom-right)
```

### Behavior Properties
```
OnSelect                - Action on click/tap
OnChange                - Action when value changes
OnVisible               - Action when screen shown (Screen only)
OnHidden                - Action when leaving screen (Screen only)
OnCheck                 - Action when checkbox/toggle turns true
OnUncheck               - Action when checkbox/toggle turns false
OnTimerStart            - Action when timer starts
OnTimerEnd              - Action when timer completes
OnSuccess               - Action when form submit succeeds (EditForm)
OnFailure               - Action when form submit fails (EditForm)
OnReset                 - Action when form resets (EditForm)
```

### Screen-Specific Properties
```
BackgroundImage         - Background image
ImagePosition           - Fill | Fit | Stretch | Tile | Center
OnVisible               - Run when screen appears
OnHidden                - Run when leaving screen
Orientation             - Layout.Horizontal | Layout.Vertical
Size                    - ScreenSize enum (1-4)
LoadingSpinner          - None | Controls | Data
LoadingSpinnerColor     - Spinner fill color
```

### Gallery-Specific Properties
```
Items                   - Data source or collection
Selected                - Currently selected record
Default                 - Initially selected item
AllItems                - All loaded items (includes control values)
AllItemsCount           - Count of loaded items
TemplateFill            - Template background color
TemplatePadding         - Space between items
TemplateSize            - Item height (vertical) or width (horizontal)
Layout                  - Vertical | Horizontal
Direction               - Left-to-right or right-to-left
ShowNavigation          - Show navigation arrows
ShowScrollbar           - Show scrollbar on hover
NavigationStep          - Scroll distance
WrapCount               - Items per row/column
Transition              - Pop | Push | None (hover effect)
Selectable              - Whether items can be selected
DelayItemLoading        - Defer loading until after screen loads
LoadingSpinner          - None | Controls | Data
```

### Form-Specific Properties
```
DataSource              - Connected data table
Item                    - Record to display/edit
DefaultMode             - FormMode.Edit | FormMode.New | FormMode.View
Mode                    - Current mode (Edit/New/View)
Valid                   - Whether all fields pass validation
Unsaved                 - Whether user has unsaved changes
Error                   - Error message from last submit
ErrorKind               - ErrorKind enum value
LastSubmit              - Last successfully submitted record
Updates                 - Record of current field values
```

### Container Properties (Horizontal/Vertical)
```
Direction               - Horizontal | Vertical
Justify (primary axis)  - Start | End | Center | Space Between
Align (cross axis)      - Start | Center | End | Stretch
Gap                     - Space between children (pixels)
Wrap                    - Whether content wraps
Horizontal Overflow     - Scroll | Hide
Vertical Overflow       - Scroll | Hide
Drop shadow             - Shadow effects
Fill portions           - Proportional space distribution (child property)
Minimum width           - Minimum child size in fill direction (child property)
Align in container      - Set by container | Start | End | Center | Stretch (child property)
```

### Text Input-Specific Properties
```
Default                 - Initial value
HintText                - Placeholder text (grayed out)
Mode                    - SingleLine | MultiLine | Password
MaxLength               - Character limit
Format                  - Text | Number
Clear                   - Show X button to clear
DelayOutput             - Delay OnChange by 500ms
EnableSpellCheck        - Browser spell check
VirtualKeyboardMode     - text | numeric
```

### Drop Down / Combo Box Properties
```
Items                   - Data source for options
Default / DefaultSelectedItems - Initial selection
Selected / SelectedItems - Current selection
Value                   - Which column to display
AllowEmptySelection     - Allow no selection (Drop down)
SelectMultiple          - Multi-select mode (Combo box)
IsSearchable            - Enable search (Combo box)
SearchFields            - Columns to search (Combo box)
DisplayFields           - Columns to display (Combo box)
InputTextPlaceholder    - Placeholder text (Combo box)
ChevronBackground       - Arrow background color
ChevronFill             - Arrow color
SelectionColor          - Selected text color
SelectionFill           - Selected background color
```

### Slider Properties
```
Default                 - Initial value
Min                     - Minimum value
Max                     - Maximum value
Value                   - Current value (output)
Layout                  - Horizontal | Vertical
ShowValue               - Display current value
HandleActiveFill        - Handle color while dragging
HandleFill              - Handle default color
HandleHoverFill         - Handle color on hover
HandleSize              - Handle diameter
RailFill                - Track color (unfilled)
ValueFill               - Track color (filled)
ReadOnly                - Prevent user changes
```

### Date Picker Properties
```
DefaultDate             - Initial date
SelectedDate            - Currently selected date (output)
Format                  - ShortDate | LongDate | custom format string
Language                - Locale (e.g., "en-us", "fr-fr")
StartYear               - Earliest selectable year
EndYear                 - Latest selectable year
StartOfWeek             - First day of week
DateTimeZone            - UTC | Local
IsEditable              - Allow text editing of date
IconFill                - Calendar icon foreground color
IconBackground          - Calendar icon background color
InputTextPlaceholder    - Placeholder text
```

### Image Properties
```
Image                   - Image source (URL, resource name, data URI)
ImagePosition           - Fill | Fit | Stretch | Tile | Center
ImageRotation           - None | CW90 | CCW90 | CW180
Transparency            - 0 (opaque) to 1 (transparent)
FlipHorizontal          - Boolean
FlipVertical            - Boolean
AutoDisableOnSelect     - Disable during OnSelect execution
ApplyEXIFOrientation    - Auto-rotate per EXIF data
CalculateOriginalDimensions - Enable OriginalHeight/OriginalWidth
```

### Timer Properties
```
Duration                - Milliseconds (max 24 hours, default 60000)
AutoStart               - Start when screen loads
AutoPause               - Pause on screen change
Repeat                  - Restart after completion
Start                   - Begin running
```

### Data Table Properties
```
Items                   - Data source
Selected                - Selected row
NoDataText              - Message when empty
HeadingColor            - Header text color
HeadingFill             - Header background
HeadingFont             - Header font
HeadingFontWeight       - Header font weight
HeadingSize             - Header font size
HoverColor              - Row hover text color
HoverFill               - Row hover background
SelectedColor           - Selected row text color
SelectedFill            - Selected row background
```

### Check Box Properties
```
Default                 - Initial boolean value
Value                   - Current boolean (output)
Text                    - Label text
CheckboxBackgroundFill  - Box background color
CheckboxBorderColor     - Box border color
CheckboxSize            - Box width/height
CheckmarkFill           - Checkmark color
```

### Toggle Properties
```
Default                 - Initial boolean value
Value                   - Current boolean (output)
FalseText               - Label when off
TrueText                - Label when on
FalseFill               - Fill when off
TrueFill                - Fill when on
FalseHoverFill          - Hover fill when off
TrueHoverFill           - Hover fill when on
HandleFill              - Handle color
ShowLabel               - Show text label
TextPosition            - Left | Right
RailFill                - Background when false
ValueFill               - Background when true
```

---

## 4. ALL POWER FX FUNCTIONS

### Mathematical Functions
```
Abs(Number)                    - Absolute value
Exp(Number)                    - e raised to power
Int(Number)                    - Round down to integer
Ln(Number)                     - Natural logarithm
Log(Number, Base)              - Logarithm in any base
Mod(Number, Divisor)           - Remainder after division
Pi()                           - Pi constant (3.14159...)
Power(Base, Exponent)          - Raise to power (also ^ operator)
Rand()                         - Random number 0-1
RandBetween(Low, High)         - Random integer in range
Round(Number, Decimals)        - Round to nearest
RoundDown(Number, Decimals)    - Round toward zero
RoundUp(Number, Decimals)      - Round away from zero
Sqrt(Number)                   - Square root
Trunc(Number)                  - Remove decimal portion
```

### Trigonometric Functions
```
Acos(Number)                   - Arccosine (radians)
Acot(Number)                   - Arccotangent (radians)
Asin(Number)                   - Arcsine (radians)
Atan(Number)                   - Arctangent (radians)
Atan2(X, Y)                    - Arctangent from coordinates
Cos(Radians)                   - Cosine
Cot(Radians)                   - Cotangent
Degrees(Radians)               - Convert to degrees
Radians(Degrees)               - Convert to radians
Sin(Radians)                   - Sine
Tan(Radians)                   - Tangent
```

### Text Functions
```
Char(CharCode)                 - Character from code
Concat(Table, Formula)         - Concatenate column values
Concatenate(S1, S2, ...)       - Join strings (also & operator)
EncodeHTML(Text)                - HTML entity encoding
EncodeUrl(Text)                - URL encoding
EndsWith(Text, EndText)        - Check string ending
Find(FindText, WithinText)     - Find position (case-sensitive)
HashTags(Text)                 - Extract #hashtags
Left(Text, Count)              - Left substring
Len(Text)                      - String length
Lower(Text)                    - Convert to lowercase
Mid(Text, Start, Count)        - Middle substring
PlainText(HTML)                - Strip HTML/XML tags
Proper(Text)                   - Title case
Replace(Text, Start, Count, New) - Replace by position
Right(Text, Count)             - Right substring
Search(Table, SearchString, Column) - Find records containing string
Split(Text, Separator)         - Split to table of substrings
StartsWith(Text, StartText)    - Check string beginning
Substitute(Text, Old, New)     - Replace by matching text
Text(Value, Format)            - Format as text
Trim(Text)                     - Remove extra spaces (all)
TrimEnds(Text)                 - Remove leading/trailing spaces
UniChar(Code)                  - Unicode character from code
Upper(Text)                    - Convert to uppercase
Value(Text)                    - Parse text to number
```

### Logical Functions
```
And(A, B, ...)                 - Logical AND (also && operator)
Coalesce(V1, V2, ...)         - First non-blank value
If(Condition, Then, Else)      - Conditional
IfError(Value, Fallback)       - Error handler
Not(Value)                     - Logical NOT (also ! operator)
Or(A, B, ...)                  - Logical OR (also || operator)
Switch(Value, Match1, R1, ...) - Multi-way conditional
```

### Table Functions
```
AddColumns(Table, Col, Formula)  - Add calculated columns
Clear(Collection)                - Remove all records
ClearCollect(Collection, ...)    - Clear then add records
Collect(Collection, Records)     - Add records to collection
Count(Table, Column)             - Count numeric values
CountA(Table, Column)            - Count non-blank values
CountIf(Table, Condition)        - Count matching records
CountRows(Table)                 - Total record count
Distinct(Table, Column)          - Unique values
DropColumns(Table, Col1, ...)    - Remove columns
Filter(Table, Condition)         - Filter records
First(Table)                     - First record
FirstN(Table, Count)             - First N records
ForAll(Table, Formula)           - Execute for each record
GroupBy(Table, Col, GroupCol)     - Group records
Index(Table, Position)           - Record by position
Last(Table)                      - Last record
LastN(Table, Count)              - Last N records
LookUp(Table, Condition, Result) - Find single record
Patch(DataSource, Record, Changes) - Create/update record
Remove(DataSource, Record)       - Delete specific record
RemoveIf(DataSource, Condition)  - Delete matching records
RenameColumns(Table, Old, New)   - Rename columns
Sequence(Count, Start, Step)     - Generate number table
ShowColumns(Table, Col1, ...)    - Select columns
Shuffle(Table)                   - Randomize order
Sort(Table, Formula, Order)      - Sort by formula
SortByColumns(Table, Col, Order) - Sort by column name
Table({...}, {...})              - Create inline table
Ungroup(Table, GroupCol)         - Flatten groups
Update(DataSource, Old, New)     - Replace record
UpdateIf(DataSource, Cond, Changes) - Update matching records
```

### Aggregate Functions
```
Average(Table, Column)           - Mean value
Max(Table, Column)               - Maximum value
Min(Table, Column)               - Minimum value
StdevP(Values...)                - Standard deviation
Sum(Table, Column)               - Total sum
VarP(Values...)                  - Variance
```

### Date/Time Functions
```
Calendar()                       - Locale calendar info
Clock()                          - Locale clock info
Date(Year, Month, Day)           - Create date
DateAdd(DateTime, Amount, Units) - Add to date
DateDiff(Start, End, Units)      - Difference between dates
DateTime(Y, M, D, H, Min, S)    - Create datetime
DateTimeValue(Text)              - Parse datetime string
DateValue(Text)                  - Parse date string
Day(DateTime)                    - Extract day (1-31)
EDate(Date, Months)              - Add months (same day)
EOMonth(Date, Months)            - Add months (last day)
Hour(DateTime)                   - Extract hour (0-23)
ISOWeekNum(DateTime)             - ISO week number
IsToday(DateTime)                - Check if today
Minute(DateTime)                 - Extract minute (0-59)
Month(DateTime)                  - Extract month (1-12)
Now()                            - Current date/time
Second(DateTime)                 - Extract second (0-59)
Time(Hour, Minute, Second)       - Create time
TimeValue(Text)                  - Parse time string
TimeZoneOffset()                 - UTC offset in minutes
Today()                          - Current date (no time)
Weekday(DateTime)                - Day of week (1-7)
WeekNum(DateTime)                - Week number
Year(DateTime)                   - Extract year
```

### Color Functions
```
Color.<ColorName>                - Built-in color constants
ColorFade(Color, Amount)         - Lighten/darken a color
ColorValue(CSSString)            - Parse CSS color / hex code
RGBA(R, G, B, A)                - Create color from components
```

### Navigation / App Functions
```
Back()                           - Return to previous screen
Exit()                           - Close app (optionally sign out)
Launch(URL)                      - Open URL or canvas app
Navigate(Screen, Transition)     - Go to screen
Param(Name)                      - Get launch parameter
```

### Form Functions
```
EditForm(FormControl)            - Switch to edit mode
NewForm(FormControl)             - Switch to new record mode
ResetForm(FormControl)           - Reset to defaults
SubmitForm(FormControl)          - Save to data source
ViewForm(FormControl)            - Switch to view mode
Defaults(DataSource)             - Default values for new record
```

### Variable Functions
```
Set(Variable, Value)             - Set global variable
UpdateContext({Var: Value})       - Set screen context variable
```

### Data Functions
```
DataSourceInfo(DS, Info)         - Metadata about data source
Errors(DataSource, Record)       - Error info for record
LoadData(Collection, Key, NonVolatile) - Load from local storage
Refresh(DataSource)              - Reload data source
Relate(Table1, Record1, Record2) - Link records (relationships)
SaveData(Collection, Key)        - Save to local storage
Unrelate(Table1, Record1, Rec2)  - Unlink records
Validate(DataSource, Column, Value) - Validate field value
RecordInfo(Record, Info)         - Record metadata
```

### Type & Conversion Functions
```
AsType(Record, TableType)        - Cast record type
Boolean(Value)                   - Convert to boolean
Float(Value)                     - Convert to float
GUID()                           - Generate new GUID
Hex2Dec(HexText)                 - Hex to decimal
Dec2Hex(Number)                  - Decimal to hex
IsBlank(Value)                   - Check for blank
IsBlankOrError(Value)            - Check for blank or error
IsEmpty(Table)                   - Check for empty table
IsError(Value)                   - Check for error
IsMatch(Text, Pattern)           - Regex match test
IsNumeric(Value)                 - Check if numeric
IsType(Record, TableType)        - Check record type
JSON(Value, Format)              - Convert to JSON string
ParseJSON(Text)                  - Parse JSON to untyped object
Type()                           - Define user-defined type
```

### Regex Functions
```
Match(Text, Pattern)             - First regex match
MatchAll(Text, Pattern)          - All regex matches
IsMatch(Text, Pattern)           - Test regex match
```

### Signal Functions (read-only environment data)
```
Acceleration                     - Device accelerometer
Compass                          - Device compass heading
Connection                       - Network connection info
Location                         - GPS coordinates
App                              - Current app info
Host                             - Host environment info
User()                           - Current user info
Language()                       - User's language tag
```

### AI Functions (Copilot/AI Builder)
```
AIClassify(Text, Categories)     - Classify text
AIExtract(Text, Entities)        - Extract entities
AIReply(Message)                 - Draft reply
AISentiment(Text)                - Sentiment analysis
AISummarize(Text)                - Summarize text
AITranslate(Text, Language)      - Translate text
```

### Other Functions
```
Blank()                          - Returns blank/null
ClearData(Key)                   - Clear local storage
Collect(Collection, Records)     - Add to collection
Concurrent(F1, F2, ...)         - Run formulas in parallel
Confirm(Message, Title)          - Show confirmation dialog
Copy(Text)                       - Copy to clipboard
Disable(Signal)                  - Disable signal (e.g., GPS)
Download(URL)                    - Download file to device
Enable(Signal)                   - Enable signal
Error(Message)                   - Create custom error
Notify(Message, NotificationType) - Show banner notification
PDF(Screen)                      - Export screen to PDF object
Print()                          - Open browser print dialog
ReadNFC()                        - Read NFC tag
Reset(Control)                   - Reset to default value
Select(Control)                  - Simulate selection
Self                             - Current control reference
SetFocus(Control)                - Move focus to control
SetProperty(Control, Prop, Value) - Set property (testing)
ShowHostInfo(Info)               - Display host info
Trace(Message)                   - Write to test log
With({Var: Value}, Formula)      - Inline record scope
```

---

## 5. OPERATORS AND IDENTIFIERS

### Arithmetic Operators
```
+    Addition
-    Subtraction / negation
*    Multiplication
/    Division
^    Exponentiation (Power)
%    Percentage (* 1/100)
```

### Comparison Operators
```
=    Equal to
<>   Not equal to
>    Greater than
>=   Greater than or equal
<    Less than
<=   Less than or equal
```

### Logical Operators
```
&&   Logical AND (also: And)
||   Logical OR (also: Or)
!    Logical NOT (also: Not)
```

### String Operators
```
&    String concatenation
```

### Membership Operators
```
in       - Case-insensitive contains / table membership
exactin  - Case-sensitive contains / table membership
```

### Special Operators
```
.        Property selector (Control.Property, Record.Field)
@        Disambiguation operator (Table[@Field], [@Global])
As       Name current record in gallery/ForAll
Self     Current control
Parent   Parent container control
ThisItem Current gallery/form item
ThisRecord Current record in ForAll/Sum/With/Filter
```

### Identifier Rules
- Single quotes for names with spaces: `'My Column Name'`
- Double quotes for text strings: `"Hello"`
- `$"..."` for string interpolation
- Display names vs. logical names (Dataverse): display names are preferred in formulas
- `;` chains behavior formulas (dot-locale uses `;;`)

---

## 6. DATA TYPES

| Type | Description | Example |
|---|---|---|
| **Boolean** | true/false | `true`, `false` |
| **Number** (Float in Canvas) | IEEE 754 double | `123`, `1.23e4` |
| **Decimal** | High-precision base-10 | `Decimal("1.234")` |
| **Text** | Unicode string | `"Hello"` |
| **Date** | Date only (user timezone) | `Date(2024, 1, 15)` |
| **Time** | Time only | `Time(14, 30, 0)` |
| **DateTime** | Date + Time | `DateTimeValue("...")` |
| **Color** | RGBA color | `RGBA(255,0,0,1)`, `Color.Red` |
| **GUID** | Globally unique ID | `GUID()` |
| **Hyperlink** | URL text string | `"https://..."` |
| **Image** | URI to image | Resource name or URL |
| **Media** | URI to audio/video | Resource name or URL |
| **Record** | Single data record | `{Name: "John", Age: 30}` |
| **Table** | Collection of records | `Table({A:1}, {A:2})` |
| **Choice** | Enumeration option | `Status.Active` |
| **Yes/No** | Two-option boolean | `Taxable` |
| **Currency** | Number with currency format | `123.45` |
| **Dynamic** | Runtime-typed (UntypedObject) | `ParseJSON(text)` |
| **Void** | No return value | Behavior functions |
| **Blank** | Null/empty (all types support) | `Blank()` |

---

## 7. CONNECTORS & DATA SOURCES

### First-Party Microsoft Connectors (Popular)
| Connector | Type | Description |
|---|---|---|
| **Microsoft Dataverse** | Tabular | Primary Power Platform database |
| **SharePoint** | Tabular | Lists and document libraries |
| **SQL Server** | Tabular | On-premises or Azure SQL |
| **Excel** | Tabular | Excel tables in cloud storage |
| **Office 365 Outlook** | Actions | Email, calendar, contacts |
| **Office 365 Users** | Actions | User profiles |
| **Power BI** | Actions | Embed dashboards/tiles |
| **Microsoft Teams** | Actions | Channels, messages |
| **OneDrive for Business** | Tabular + Actions | File storage |
| **Azure Blob Storage** | Actions | Cloud file storage |

### Third-Party Connectors (Popular)
| Connector | Type |
|---|---|
| **Salesforce** | Tabular + Actions |
| **Twitter** | Actions |
| **Google Drive** | Actions |
| **Dropbox** | Actions |
| **Oracle** | Tabular |
| **SAP** | Tabular + Actions |
| **Dynamics 365** | Tabular |
| **Dynamics AX** | Tabular |

### Connector Categories
- **Standard connectors**: Included with all Power Apps licenses
- **Premium connectors**: Require premium license (Dataverse, SQL Server, etc.)
- **Custom connectors**: User-built REST API connectors (OpenAPI/Swagger)
- **On-premises data gateway**: Bridge to on-premises data sources

### Data Source Types
1. **Tabular**: Provides tables of data (SharePoint, SQL, Dataverse, Excel)
   - Set `Items` property of Gallery/Form to table name
   - Support delegation for server-side filtering/sorting
2. **Action-based**: Provides function calls (Twitter, Outlook)
   - Call actions in formulas: `Twitter.SearchTweet("query")`
   - No automatic paging
3. **Collections**: In-memory tables (local to app)
   - Created via `Collect()`, `ClearCollect()`
   - Full formula language support (no delegation needed)
4. **Local storage**: Persist between sessions
   - `SaveData(Collection, "key")` / `LoadData(Collection, "key")`

### Delegation
- Default limit: **500 records** (configurable up to 2,000)
- **Delegable functions**: Filter, Search, Sort, SortByColumns, LookUp, First, Sum, Average, Min, Max, CountRows
- **Delegable filter operators**: =, <>, <, >, <=, >=, And, Or, Not, In, StartsWith, EndsWith, IsBlank, TrimEnds
- **Non-delegable functions**: FirstN, LastN, Choices, Concat, Collect, GroupBy, Ungroup, Distinct
- **Non-delegable in filters**: If, *, /, Mod, Concatenate, ExactIn, Mid, Left, Lower, Upper, Len, Rand
- Delegation support varies by data source (Dataverse > SharePoint > SQL > Excel)
- Collections and imported data: always local, no delegation needed

---

## 8. COMPONENTS

### Component Structure
- Reusable building blocks within or across apps
- Created in Components tab or Component Libraries
- Instance = copy on a screen; changes to definition update all instances
- Can be shared via **Component Libraries** (publish/update mechanism)

### Custom Properties
| Property Type | Direction | Purpose |
|---|---|---|
| **Input** | Into component | Pass data to component |
| **Output** | Out of component | Emit data/state from component |

### Property Data Types for Custom Properties
- Text, Number, Boolean, Date, Time, DateTime
- Table, Record
- Screen, Color, Image, Media

### Component Scope
- **Default**: Encapsulated (no access to app variables/collections/controls)
- **Access app scope ON**: Can access global variables, collections, screen controls, tabular data sources
- Component Library components cannot access app scope

### Known Limitations
- Cannot insert component inside a Gallery or Form
- No UpdateContext inside components (use Set instead)
- Cannot have two instances reference each other's custom output properties
- Cannot save data sources or data-bound controls inside components
- Power Automate flows not supported in component libraries

---

## 9. SCREEN TEMPLATES

### Available Layout Templates (for responsive apps)
| Template | Description |
|---|---|
| **Blank** | Empty screen |
| **Split-screen** | Two 50% sections (stack vertically on mobile) |
| **Sidebar** | Fixed sidebar + fluid main content |
| **Scrollable** | Full-width scrollable content |

### Responsive Design Configuration
1. Disable: Scale to fit, Lock aspect ratio, Lock orientation
2. Use containers (Horizontal/Vertical) instead of fixed X/Y positioning
3. Set `Width = Parent.Width`, `Height = Parent.Height` for full-screen containers
4. Use `Fill portions` to distribute space proportionally between children
5. Screen properties: `Size` (1-4), `Orientation`, `Width`, `Height`
6. App.SizeBreakpoints for responsive breakpoint values

---

## 10. .MSAPP FILE FORMAT

### File Structure
The `.msapp` file is a **ZIP archive** containing:
```
├── Header.json              - App metadata and version
├── Properties.json          - App-level properties
├── Themes.json              - Theme definitions
├── DataSources/             - Data source connection configs
├── Resources/               - Embedded images, media, etc.
├── Controls/                - Screen and control definitions
│   ├── Screen1.json         - Each screen as JSON
│   └── Screen2.json
├── Entropy/                 - Non-deterministic metadata
├── ComponentDefinitions/    - Custom component definitions
├── pkgs/                    - Package references
└── References/              - Resource references
```

### Key Tools for .msapp Manipulation
1. **microsoft/PowerApps-Tooling** (GitHub): C#/.NET library
   - PASopa tool: Pack/unpack .msapp to/from YAML source files
   - `Microsoft.PowerPlatform.PowerApps.Persistence` NuGet library
   - Now legacy; replaced by Power Platform CLI `pac` tool
2. **Power Platform CLI**: `pac canvas pack/unpack`
   - Converts .msapp to source-controlled YAML format
3. **Power Platform Git Integration**: Recommended path forward
4. **YAML Schema**: Available at `schemas/pa-yaml/` in the tooling repo

### YAML Representation (pa.yaml format)
```yaml
# Screen definition
Screen1:
  Control: GroupContainer
  Variant: ManualLayout    # or AutoLayout
  Properties:
    Fill: =RGBA(255, 255, 255, 1)
    Width: =Max(App.Width, App.DesignWidth)
    Height: =Max(App.Height, App.DesignHeight)
  Children:
    - Header_Label:
        Control: Label
        Properties:
          Text: ="Welcome"
          X: =20
          Y: =20
          Width: =400
          Height: =60
          Size: =24
          FontWeight: =FontWeight.Bold
          Color: =RGBA(0, 0, 0, 1)
    - Submit_Button:
        Control: Classic/Button
        Properties:
          Text: ="Submit"
          OnSelect: =SubmitForm(Form1)
          X: =20
          Y: =100
          Width: =200
          Height: =50
```

### Internal Control Type Names (from YAML/JSON)
```
Screen types:    screen, GroupContainer (ManualLayout/AutoLayout)
Button:          Classic/Button
Label:           Classic/Label, text
TextInput:       Classic/TextInput
Gallery:         gallery (Vertical/Horizontal/Flexible)
DropDown:        Classic/DropDown
ComboBox:        Classic/ComboBox
DatePicker:      Classic/DatePicker
CheckBox:        Classic/CheckBox
Toggle:          Classic/Toggle
Slider:          Classic/Slider
Rating:          Classic/Rating
Radio:           Classic/Radio
ListBox:         Classic/ListBox
Image:           Classic/Image
Icon:            Classic/Icon
Shape:           Classic/Rectangle, Classic/Circle, Classic/Triangle
Timer:           Classic/Timer
Form:            Classic/FormViewer (Edit/Display)
DataTable:       Classic/DataTable
HContainer:      LayoutContainer (Horizontal)
VContainer:      LayoutContainer (Vertical)
HTMLText:        Classic/HtmlViewer
RichTextEditor:  Classic/RichTextEditor
Camera:          Classic/Camera
Audio:           Classic/Audio
Video:           Classic/Video
Microphone:      Classic/Microphone
PDFViewer:       Classic/PdfViewer
PenInput:        Classic/PenInput
AddPicture:      Classic/AddPicture
Chart:           Classic/ColumnChart, Classic/LineChart, Classic/PieChart
PowerBITile:     Classic/PowerBiTile
Barcode:         Classic/BarcodeReader
Map:             Classic/Map
Attachments:     Classic/Attachments
```

---

## 11. COMMON APP PATTERNS

### Browse-Detail-Edit (3-Screen Pattern)
1. **Browse Screen**: Gallery + SearchBox + sort
2. **Detail Screen**: Display form showing selected record
3. **Edit Screen**: Edit form for create/update

### Master-Detail
- Gallery on left, Form/Detail on right
- `Gallery.Selected` drives form `Item` property

### Navigation Pattern
```
Navigate(ScreenName, ScreenTransition.Fade)
Navigate(ScreenName, ScreenTransition.Cover)
Navigate(ScreenName, ScreenTransition.None)
Back()
```

### Screen Transitions
```
ScreenTransition.None
ScreenTransition.Fade
ScreenTransition.Cover
ScreenTransition.CoverRight
ScreenTransition.UnCover
ScreenTransition.UnCoverRight
```

### Common Formula Patterns
```
// Filter gallery items
Filter(DataSource, SearchText in ColumnName)

// Sort gallery
SortByColumns(Filter(DataSource, ...), "Column", SortOrder.Ascending)

// Conditional visibility
If(SomeCondition, true, false)

// Navigate with context
Navigate(DetailScreen, ScreenTransition.None, {SelectedRecord: Gallery1.Selected})

// Submit form and navigate
SubmitForm(EditForm1); Back()

// Collect data
ClearCollect(MyCollection, DataSource)

// Update context variable
UpdateContext({showPopup: true})

// Global variable
Set(currentUser, User().Email)
```

---

## 12. ENUMERATIONS

### Common Enumerations
```
Color.*                 - Color.Red, Color.Blue, Color.Green, ...
SortOrder.*             - SortOrder.Ascending, SortOrder.Descending
FormMode.*              - FormMode.Edit, FormMode.New, FormMode.View
DisplayMode.*           - DisplayMode.Edit, DisplayMode.View, DisplayMode.Disabled
ScreenTransition.*      - None, Fade, Cover, CoverRight, UnCover, UnCoverRight
Layout.*                - Layout.Horizontal, Layout.Vertical
ErrorKind.*             - None, Sync, Conflict, Validation, ...
NotificationType.*      - Information, Warning, Error, Success
FontWeight.*            - FontWeight.Normal, Bold, Semibold, Lighter
Align.*                 - Align.Left, Align.Center, Align.Right
VerticalAlign.*         - VerticalAlign.Top, VerticalAlign.Middle, VerticalAlign.Bottom
ImagePosition.*         - ImagePosition.Fill, Fit, Stretch, Tile, Center
BorderStyle.*           - BorderStyle.Solid, Dashed, Dotted, None
Match.*                 - Match.Email, Match.Digit, Match.Letter, ... (regex patterns)
DateTimeFormat.*        - ShortDate, LongDate, ShortTime, LongTime, ShortDateTime, LongDateTime, UTC
TimeUnit.*              - Days, Hours, Minutes, Seconds, Months, Quarters, Years
Icon.*                  - Icon.Add, Icon.Edit, Icon.Delete, Icon.Search, Icon.Cancel, ...
ScreenSize.*            - ScreenSize.Small(1), Medium(2), Large(3), ExtraLarge(4)
```

---

## 13. MCP SERVER IMPLEMENTATION NOTES

### Key Considerations for Programmatic Generation
1. **Control naming**: Must be unique within the app. Convention: `TypeName_N` (e.g., `Button1`, `Label2`)
2. **Property formulas**: Prefix with `=` in YAML format for formulas; static values are unquoted or quoted strings
3. **Coordinate system**: Origin (0,0) is top-left of parent. X increases right, Y increases down.
4. **Default app size**: Phone (640x1136), Tablet (1366x768)
5. **Z-order**: Later children render on top of earlier siblings
6. **Container nesting**: Max 2 levels of gallery nesting. No forms inside galleries.
7. **Theme**: Controls inherit from theme; explicit properties override theme defaults
8. **Data source references**: Must match connection configuration in DataSources/ folder
9. **Resource references**: Images use `appres://blobmanager/<hash>` URIs
10. **Component instances**: Reference `ComponentName` and `ComponentLibraryUniqueName`

### Recommended Generation Strategy
1. Parse natural language to identify: screens, controls, data sources, navigation
2. Generate YAML structure per screen
3. Auto-assign names and positions using layout algorithms
4. For responsive layouts, prefer containers over absolute positioning
5. Use `pac canvas pack` or PowerApps-Tooling library to assemble .msapp
6. Validate formulas reference existing controls and data sources

### App Settings to Generate
```yaml
App:
  Properties:
    Theme: =PowerAppsTheme  # or custom theme
    StartScreen: =Screen1
    OnStart: =<initialization formulas>
    SizeBreakpoints: =[600, 900, 1200]  # responsive breakpoints
  Settings:
    ScreenWidth: 1366       # or 640 for phone
    ScreenHeight: 768       # or 1136 for phone
    ScaleToFit: true/false
    LockAspectRatio: true/false
    LockOrientation: true/false
```
