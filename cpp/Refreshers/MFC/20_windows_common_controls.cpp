// ============================================================================
// MFC WINDOWS COMMON CONTROLS
// File: 20_windows_common_controls.cpp
// Covers: CProgressCtrl, CSliderCtrl, CSpinButtonCtrl, CAnimateCtrl,
//         CDateTimeCtrl, CMonthCalCtrl, CIPAddressCtrl, CHotKeyCtrl
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. CProgressCtrl - PROGRESS BAR
// ============================================================================

/*
CProgressCtrl displays a progress bar for long operations.

Key methods:
- SetRange() / SetRange32() - Set min/max range
- GetRange() - Get range
- SetPos() / GetPos() - Set/get position
- OffsetPos() - Increment position
- SetStep() / StepIt() - Step increment
- SetBarColor() - Set bar color
- SetBkColor() - Set background color
- SetMarquee() - Enable marquee mode (Vista+)

Styles:
PBS_SMOOTH - Smooth fill (not blocky)
PBS_VERTICAL - Vertical bar
PBS_MARQUEE - Marquee animation (Vista+)
*/

void CProgressCtrlExample(CProgressCtrl& progress)
{
    // Set range
    progress.SetRange(0, 100);
    
    // Set position
    progress.SetPos(50);
    
    // Step increment
    progress.SetStep(10);
    progress.StepIt();  // Increment by 10
    
    // Offset position
    progress.OffsetPos(5);
    
    // Get current position
    int pos = progress.GetPos();
    
    // Smooth progress bar
    progress.ModifyStyle(0, PBS_SMOOTH);
    
    // Marquee mode (Vista+)
    progress.SetMarquee(TRUE, 30);  // 30ms update rate
}

// ============================================================================
// 2. CSliderCtrl - SLIDER CONTROL
// ============================================================================

/*
CSliderCtrl (trackbar) allows selecting a value from a range.

Key methods:
- SetRange() / GetRange() - Min/max values
- SetPos() / GetPos() - Current position
- SetTic() / SetTicFreq() - Tick marks
- SetLineSize() / GetLineSize() - Arrow key increment
- SetPageSize() / GetPageSize() - Page up/down increment
- SetSelection() / GetSelection() - Selection range
- ClearSel() / ClearTics() - Clear selections/ticks
- SetBuddy() - Set buddy window
- GetBuddy() - Get buddy window
- SetTooltip() - Enable tooltip

Styles:
TBS_AUTOTICKS - Automatic tick marks
TBS_VERT - Vertical slider
TBS_BOTH - Ticks on both sides
TBS_NOTICKS - No ticks
TBS_TOOLTIPS - Enable tooltips
TBS_REVERSED - Reversed direction
TBS_DOWNISLEFT - Down/Left orientation
*/

void CSliderCtrlExample(CSliderCtrl& slider)
{
    // Set range
    slider.SetRange(0, 100);
    
    // Set position
    slider.SetPos(50);
    
    // Set tick frequency
    slider.SetTicFreq(10);  // Tick every 10 units
    
    // Set line and page size
    slider.SetLineSize(1);   // Arrow keys
    slider.SetPageSize(10);  // Page up/down
    
    // Set selection range
    slider.SetSelection(20, 80);
    
    // Enable tooltip
    slider.ModifyStyle(0, TBS_TOOLTIPS);
    
    // Get position
    int pos = slider.GetPos();
    
    // Handle scroll notifications
    // NM_RELEASEDCAPTURE - User released slider
    // WM_HSCROLL / WM_VSCROLL - Scroll events
}

// ============================================================================
// 3. CSpinButtonCtrl - SPIN CONTROL (UPDOWN)
// ============================================================================

/*
CSpinButtonCtrl (up-down control) increments/decrements a value.

Key methods:
- SetRange() / GetRange() - Min/max values
- SetPos() / GetPos() - Current position
- SetBase() - Base (10 or 16)
- SetAccel() / GetAccel() - Acceleration
- SetBuddy() / GetBuddy() - Buddy window
- SetAutoBuddy() - Auto-set buddy

Styles:
UDS_ALIGNLEFT / UDS_ALIGNRIGHT - Position relative to buddy
UDS_ARROWKEYS - Arrow key support
UDS_AUTOBUDDY - Auto buddy window
UDS_HORZ - Horizontal orientation
UDS_NOTHOUSANDS - No thousands separator
UDS_SETBUDDYINT - Auto-update buddy text
UDS_WRAP - Wrap around at range limits
*/

void CSpinButtonCtrlExample(CSpinButtonCtrl& spin)
{
    // Set range
    spin.SetRange(0, 100);
    
    // Set position
    spin.SetPos(50);
    
    // Set base (10 = decimal, 16 = hex)
    spin.SetBase(10);
    
    // Set acceleration
    UDACCEL accel[3];
    accel[0].nSec = 0;     // No delay
    accel[0].nInc = 1;     // Increment by 1
    accel[1].nSec = 1;     // After 1 second
    accel[1].nInc = 5;     // Increment by 5
    accel[2].nSec = 2;     // After 2 seconds
    accel[2].nInc = 10;    // Increment by 10
    spin.SetAccel(3, accel);
    
    // Auto buddy
    spin.SetAutoBuddy(TRUE);
    
    // Get position
    int pos = spin.GetPos();
}

// ============================================================================
// 4. CAnimateCtrl - ANIMATION CONTROL
// ============================================================================

/*
CAnimateCtrl plays AVI clips (without audio).

Key methods:
- Open() - Open AVI file/resource
- Play() / Stop() - Play/stop animation
- Close() - Close AVI
- Seek() - Seek to frame

Styles:
ACS_CENTER - Center in control
ACS_TRANSPARENT - Transparent background
ACS_AUTOPLAY - Auto-play when opened
ACS_TIMER - Use timer (not thread)
*/

void CAnimateCtrlExample(CAnimateCtrl& animate)
{
    // Open from resource
    animate.Open(IDR_AVI_SEARCH);
    
    // Play (from frame 0 to end, 3 times)
    animate.Play(0, (UINT)-1, 3);
    
    // Play indefinitely
    animate.Play(0, (UINT)-1, (UINT)-1);
    
    // Stop
    animate.Stop();
    
    // Seek to frame
    animate.Seek(5);
    
    // Close
    animate.Close();
}

// ============================================================================
// 5. CDateTimeCtrl - DATE/TIME PICKER
// ============================================================================

/*
CDateTimeCtrl provides date and time selection.

Key methods:
- SetTime() / GetTime() - Set/get time
- SetRange() / GetRange() - Valid date range
- SetFormat() - Display format
- GetMonthCalCtrl() - Get month calendar
- GetMonthCalFont() / SetMonthCalFont() - Calendar font
- SetCheck() / GetCheck() - Checkbox state

Formats:
d - Day (1-31)
dd - Day (01-31)
ddd - Day abbreviation (Mon)
dddd - Day full name (Monday)
M - Month (1-12)
MM - Month (01-12)
MMM - Month abbreviation (Jan)
MMMM - Month full name (January)
y - Year (last 2 digits)
yy - Year (last 2 digits)
yyy - Year (4 digits)
h - Hours (12-hour)
H - Hours (24-hour)
m - Minutes
s - Seconds
t - AM/PM

Styles:
DTS_LONGDATEFORMAT - Long date format
DTS_SHORTDATEFORMAT - Short date format
DTS_TIMEFORMAT - Time format
DTS_UPDOWN - Up-down control instead of calendar
DTS_SHOWNONE - Show checkbox (can be empty)
DTS_APPCANPARSE - Allow custom input
*/

void CDateTimeCtrlExample(CDateTimeCtrl& dtPicker)
{
    // Set format
    dtPicker.SetFormat(_T("MM/dd/yyyy hh:mm:ss tt"));
    
    // Set time
    CTime time(2024, 1, 15, 10, 30, 0);
    dtPicker.SetTime(&time);
    
    // Get time
    CTime currentTime;
    dtPicker.GetTime(currentTime);
    
    // Set valid range
    CTime minTime(2020, 1, 1, 0, 0, 0);
    CTime maxTime(2030, 12, 31, 23, 59, 59);
    dtPicker.SetRange(&minTime, &maxTime);
    
    // Enable checkbox (can be unchecked)
    dtPicker.ModifyStyle(0, DTS_SHOWNONE);
    
    // Check if set
    BOOL bChecked = dtPicker.GetCheck();
}

// ============================================================================
// 6. CMonthCalCtrl - MONTH CALENDAR
// ============================================================================

/*
CMonthCalCtrl displays a month calendar for date selection.

Key methods:
- SetToday() / GetToday() - Today's date
- SetCurSel() / GetCurSel() - Selected date
- SetRange() / GetRange() - Valid range
- SetDayState() - Custom day states
- SetMaxSelCount() / GetMaxSelCount() - Max selectable days
- SetFirstDayOfWeek() - First day of week
- GetMonthRange() - Visible month range
- GetMinReqRect() - Minimum required size
- SizeMinReq() - Size to minimum

Styles:
MCS_MULTISELECT - Allow multiple selection
MCS_WEEKNUMBERS - Show week numbers
MCS_NOTODAY - Hide today's date
MCS_NOTODAYCIRCLE - No circle around today
MCS_DAYSTATE - Custom day states
*/

void CMonthCalCtrlExample(CMonthCalCtrl& calendar)
{
    // Set today's date
    calendar.SetToday(CTime::GetCurrentTime());
    
    // Set selected date
    CTime selected(2024, 6, 15, 0, 0, 0);
    calendar.SetCurSel(selected);
    
    // Get selected date
    CTime curSel;
    calendar.GetCurSel(curSel);
    
    // Set range
    CTime minDate(2024, 1, 1, 0, 0, 0);
    CTime maxDate(2024, 12, 31, 0, 0, 0);
    calendar.SetRange(&minDate, &maxDate);
    
    // Enable multi-select
    calendar.ModifyStyle(0, MCS_MULTISELECT);
    calendar.SetMaxSelCount(7);  // Select up to 7 days
    
    // Show week numbers
    calendar.ModifyStyle(0, MCS_WEEKNUMBERS);
    
    // Get minimum required size
    CSize minSize = calendar.GetMinReqRect();
}

// ============================================================================
// 7. CIPAddressCtrl - IP ADDRESS CONTROL
// ============================================================================

/*
CIPAddressCtrl allows entering IPv4 addresses.

Key methods:
- SetAddress() - Set IP address
- GetAddress() - Get IP address
- SetFieldFocus() - Set focus to field
- SetFieldRange() - Set field range
- IsBlank() - Check if blank
- ClearAddress() - Clear address
*/

void CIPAddressCtrlExample(CIPAddressCtrl& ipCtrl)
{
    // Set address
    ipCtrl.SetAddress(192, 168, 1, 100);
    
    // Get address
    BYTE b1, b2, b3, b4;
    ipCtrl.GetAddress(b1, b2, b3, b4);
    
    // Get as DWORD
    DWORD dwAddress;
    ipCtrl.GetAddress(dwAddress);
    
    // Set field range (e.g., first field 10-20)
    ipCtrl.SetFieldRange(0, 10, 20);
    
    // Set focus to specific field
    ipCtrl.SetFieldFocus(2);
    
    // Check if blank
    if (ipCtrl.IsBlank())
    {
        // No address entered
    }
    
    // Clear
    ipCtrl.ClearAddress();
}

// ============================================================================
// 8. CHotKeyCtrl - HOT KEY CONTROL
// ============================================================================

/*
CHotKeyCtrl allows user to enter a keyboard shortcut.

Key methods:
- SetHotKey() / GetHotKey() - Set/get hotkey
- SetRules() - Set invalid combinations

Modifier flags:
HOTKEYF_ALT - Alt key
HOTKEYF_CONTROL - Ctrl key
HOTKEYF_SHIFT - Shift key
HOTKEYF_EXT - Extended key
*/

void CHotKeyCtrlExample(CHotKeyCtrl& hotKey)
{
    // Set hot key (Ctrl+Shift+A)
    hotKey.SetHotKey('A', HOTKEYF_CONTROL | HOTKEYF_SHIFT);
    
    // Get hot key
    WORD wVirtualKeyCode;
    WORD wModifiers;
    hotKey.GetHotKey(wVirtualKeyCode, wModifiers);
    
    // Set rules (invalid combinations)
    hotKey.SetRules(HKCOMB_A, HKCOMB_NONE);  // No Alt combos
    hotKey.SetRules(HKCOMB_C, HKCOMB_NONE);  // No Ctrl combos
    
    // Register hot key with Windows
    // ::RegisterHotKey(hWnd, ID_MY_HOTKEY, wModifiers, wVirtualKeyCode);
}

// ============================================================================
// 9. BEST PRACTICES
// ============================================================================

/*
1. Use SetRange() before SetPos() for progress/spin controls
2. Use SetTicFreq() for slider tick marks
3. Use SetAccel() for spin control acceleration
4. Use SetFormat() for custom date/time display
5. Use SetRange() to restrict date selection
6. Use SetFieldRange() for IP address validation
7. Use SetRules() to prevent invalid hotkey combinations
8. Use SetBuddy() to associate spin with edit control
9. Use SetMarquee() for indeterminate progress
10. Use SetDayState() for custom calendar day display
*/

#endif // _MFC_VER
