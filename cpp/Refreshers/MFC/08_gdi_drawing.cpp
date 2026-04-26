// ============================================================================
// MFC GDI DRAWING
// File: 08_gdi_drawing.cpp
// Covers: CDC, CPaintDC, CClientDC, CWindowDC, CPen, CBrush, CFont, CRect
// ============================================================================

#ifdef _MFC_VER

// ============================================================================
// 1. DEVICE CONTEXTS
// ============================================================================

/*
A Device Context (DC) is a Windows data structure that defines the drawing
attributes for a device (screen, printer, etc.).

MFC DC classes:
- CDC - Base class for all device contexts
- CPaintDC - For WM_PAINT handling (auto BeginPaint/EndPaint)
- CClientDC - For drawing on client area (outside WM_PAINT)
- CWindowDC - For drawing on entire window (including non-client)
- CMetaFileDC - For creating metafiles
- CMemDC - For double buffering (memory DC)

Key CDC methods:
- SelectObject() - Select GDI object (pen, brush, font)
- MoveTo() / LineTo() - Draw lines
- Rectangle() / Ellipse() - Draw shapes
- TextOut() / DrawText() - Draw text
- SetPixel() / GetPixel() - Pixel operations
- BitBlt() / StretchBlt() - Bitmap operations
- SetBkColor() / SetTextColor() - Colors
- FillRect() / FrameRect() - Rectangle operations
- Polyline() / Polygon() - Complex shapes
- Arc() / Pie() - Arc and pie shapes
- RoundRect() - Rounded rectangle
- SetMapMode() - Coordinate mapping
- DPtoLP() / LPtoDP() - Coordinate conversion
*/

// ============================================================================
// 2. CPaintDC - WM_PAINT HANDLING
// ============================================================================

/*
CPaintDC should only be used in OnPaint() handlers.
It automatically calls BeginPaint() in constructor and EndPaint() in destructor.
*/

void CMyView::OnPaint()
{
    CPaintDC dc(this);  // Device context for painting
    
    // Get client area
    CRect rect;
    GetClientRect(&rect);
    
    // Draw text centered in client area
    dc.DrawText(_T("Hello, MFC!"), -1, &rect,
        DT_CENTER | DT_VCENTER | DT_SINGLELINE);
    
    // Draw a rectangle
    dc.Rectangle(10, 10, 100, 100);
    
    // Draw an ellipse
    dc.Ellipse(150, 10, 250, 100);
    
    // Draw a line
    dc.MoveTo(10, 150);
    dc.LineTo(200, 150);
    
    // CPaintDC destructor automatically calls EndPaint()
}

// ============================================================================
// 3. CClientDC - DRAWING OUTSIDE WM_PAINT
// ============================================================================

/*
CClientDC is used for drawing outside of WM_PAINT (e.g., in mouse handlers).
It gets the DC for the client area only.
*/

void CMyView::OnLButtonDown(UINT nFlags, CPoint point)
{
    CClientDC dc(this);
    
    // Draw a red pixel at click position
    dc.SetPixel(point, RGB(255, 0, 0));
    
    // Draw a small rectangle
    CRect rect(point.x - 5, point.y - 5, point.x + 5, point.y + 5);
    dc.Rectangle(rect);
    
    CView::OnLButtonDown(nFlags, point);
}

// ============================================================================
// 4. CPen - DRAWING LINES AND BORDERS
// ============================================================================

/*
CPen defines the style, width, and color of lines and borders.

Pen styles:
PS_SOLID       - Solid line
PS_DASH        - Dashed line (width must be 1)
PS_DOT         - Dotted line (width must be 1)
PS_DASHDOT     - Dash-dot (width must be 1)
PS_DASHDOTDOT  - Dash-dot-dot (width must be 1)
PS_NULL        - No line
PS_INSIDEFRAME - Line inside frame
PS_GEOMETRIC   - Geometric pen (for wide lines)
*/

void PenExample(CDC* pDC)
{
    // Create pens
    CPen redPen(PS_SOLID, 2, RGB(255, 0, 0));
    CPen bluePen(PS_DASH, 1, RGB(0, 0, 255));
    CPen greenPen(PS_DOT, 1, RGB(0, 255, 0));
    
    // Select pen into DC (save old pen)
    CPen* pOldPen = pDC->SelectObject(&redPen);
    
    // Draw with red pen
    pDC->Rectangle(10, 10, 100, 100);
    
    // Switch to blue pen
    pDC->SelectObject(&bluePen);
    pDC->Rectangle(120, 10, 210, 100);
    
    // Switch to green pen
    pDC->SelectObject(&greenPen);
    pDC->Ellipse(230, 10, 320, 100);
    
    // Restore old pen
    pDC->SelectObject(pOldPen);
}

// ============================================================================
// 5. CBrush - FILLING SHAPES
// ============================================================================

/*
CBrush defines the fill pattern for shapes.

Brush types:
- Solid color: CBrush(COLORREF color)
- Hatched: CBrush(HS_CROSS, color)
- Pattern: CBrush(CBitmap* pBitmap)
- Null: CBrush() - no fill (hollow)

Hatch styles:
HS_BDIAGONAL - Downward hatch (left to right)
HS_CROSS     - Horizontal and vertical crosshatch
HS_DIAGCROSS - Diagonal crosshatch
HS_FDIAGONAL - Upward hatch (left to right)
HS_HORIZONTAL - Horizontal hatch
HS_VERTICAL  - Vertical hatch
*/

void BrushExample(CDC* pDC)
{
    // Create brushes
    CBrush redBrush(RGB(255, 0, 0));
    CBrush blueBrush(RGB(0, 0, 255));
    CBrush hatchBrush(HS_CROSS, RGB(0, 255, 0));
    CBrush nullBrush;  // Hollow brush
    
    // Select brush into DC
    CBrush* pOldBrush = pDC->SelectObject(&redBrush);
    pDC->Ellipse(10, 10, 100, 100);
    
    pDC->SelectObject(&blueBrush);
    pDC->Rectangle(120, 10, 210, 100);
    
    pDC->SelectObject(&hatchBrush);
    pDC->Rectangle(230, 10, 320, 100);
    
    pDC->SelectObject(&nullBrush);
    pDC->Rectangle(340, 10, 430, 100);  // Outline only
    
    // Restore old brush
    pDC->SelectObject(pOldBrush);
}

// ============================================================================
// 6. CFont - TEXT DRAWING
// ============================================================================

/*
CFont encapsulates a Windows font. Create fonts using LOGFONT structure
or helper methods.

Key methods:
- CreateFont() - Create font with specified attributes
- CreateFontIndirect() - Create from LOGFONT structure
- CreatePointFont() - Create from point size
- GetLogFont() - Get LOGFONT structure

LOGFONT fields:
lfHeight         - Height in logical units
lfWidth          - Average character width
lfEscapement     - Text angle (0.1 degrees)
lfOrientation    - Character angle
lfWeight         - FW_NORMAL, FW_BOLD, etc.
lfItalic         - Italic
lfUnderline      - Underline
lfStrikeOut      - Strikeout
lfCharSet        - ANSI_CHARSET, DEFAULT_CHARSET, etc.
lfOutPrecision   - Output precision
lfClipPrecision  - Clipping precision
lfQuality        - DEFAULT_QUALITY, PROOF_QUALITY, etc.
lfPitchAndFamily - Pitch and family
lfFaceName       - Typeface name (e.g., "Arial")
*/

void FontExample(CDC* pDC)
{
    // Create fonts
    CFont fontArial;
    fontArial.CreateFont(
        36,                    // Height
        0,                     // Width (0 = default)
        0,                     // Escapement
        0,                     // Orientation
        FW_BOLD,               // Weight
        FALSE,                 // Italic
        TRUE,                  // Underline
        FALSE,                 // StrikeOut
        ANSI_CHARSET,          // CharSet
        OUT_DEFAULT_PRECIS,    // OutPrecision
        CLIP_DEFAULT_PRECIS,   // ClipPrecision
        DEFAULT_QUALITY,       // Quality
        DEFAULT_PITCH | FF_SWISS, // Pitch and Family
        _T("Arial"));          // Typeface
    
    CFont fontTimes;
    fontTimes.CreatePointFont(120, _T("Times New Roman"));
    
    CFont fontCourier;
    fontCourier.CreatePointFont(100, _T("Courier New"));
    
    // Select font
    CFont* pOldFont = pDC->SelectObject(&fontArial);
    pDC->TextOut(10, 10, _T("Arial Bold Underline"));
    
    pDC->SelectObject(&fontTimes);
    pDC->TextOut(10, 60, _T("Times New Roman"));
    
    pDC->SelectObject(&fontCourier);
    pDC->TextOut(10, 110, _T("Courier New"));
    
    // Restore old font
    pDC->SelectObject(pOldFont);
}

// ============================================================================
// 7. CRect AND COORDINATE OPERATIONS
// ============================================================================

/*
CRect is a rectangle class derived from RECT structure.

Key methods:
- Width() / Height() - Dimensions
- TopLeft() / BottomRight() - Points
- IsRectEmpty() / IsRectNull() - State checks
- PtInRect() - Point containment
- SetRect() / SetRectEmpty() - Set values
- OffsetRect() - Move rectangle
- InflateRect() / DeflateRect() - Resize
- IntersectRect() - Intersection
- UnionRect() - Union
- SubtractRect() - Difference
- NormalizeRect() - Ensure valid coordinates
- EqualRect() - Equality check
*/

void CRectExample(CDC* pDC)
{
    CRect rect1(10, 10, 200, 100);
    CRect rect2(100, 50, 300, 150);
    
    // Rectangle properties
    int width = rect1.Width();     // 190
    int height = rect1.Height();   // 90
    CPoint center = rect1.CenterPoint();
    
    // Point containment
    CPoint pt(50, 50);
    if (rect1.PtInRect(pt))
    {
        // Point is inside rectangle
    }
    
    // Rectangle operations
    CRect intersection;
    intersection.IntersectRect(rect1, rect2);  // Overlapping area
    
    CRect unionRect;
    unionRect.UnionRect(rect1, rect2);  // Combined area
    
    // Move rectangle
    rect1.OffsetRect(10, 10);  // Move right 10, down 10
    
    // Resize rectangle
    rect1.InflateRect(5, 5);   // Expand by 5 pixels each side
    rect1.DeflateRect(5, 5);   // Shrink by 5 pixels each side
    
    // Draw rectangles
    CPen bluePen(PS_SOLID, 2, RGB(0, 0, 255));
    CPen* pOldPen = pDC->SelectObject(&bluePen);
    
    pDC->Rectangle(rect1);
    pDC->Rectangle(rect2);
    
    pDC->SelectObject(pOldPen);
}

// ============================================================================
// 8. CPoint AND CSize
// ============================================================================

/*
CPoint - 2D point (x, y)
CSize - 2D size (cx, cy)

Operations:
CPoint + CSize = CPoint
CPoint - CSize = CPoint
CPoint - CPoint = CSize
CSize + CSize = CSize
CSize - CSize = CSize
*/

void PointSizeExample()
{
    CPoint pt1(10, 20);
    CPoint pt2(30, 40);
    CSize size(5, 10);
    
    CPoint pt3 = pt1 + size;     // (15, 30)
    CPoint pt4 = pt2 - size;     // (25, 30)
    CSize diff = pt2 - pt1;      // (20, 20)
    
    // Offset point
    pt1.Offset(5, 5);            // (15, 25)
    
    // Equality
    if (pt1 == pt2)
    {
        // Points are equal
    }
}

// ============================================================================
// 9. DOUBLE BUFFERING
// ============================================================================

/*
Double buffering eliminates flicker by drawing to a memory DC first,
then copying the result to the screen in one operation.
*/

void DoubleBufferExample(CDC* pDC, CRect& rect)
{
    // Create memory DC compatible with screen
    CDC memDC;
    memDC.CreateCompatibleDC(pDC);
    
    // Create bitmap
    CBitmap bitmap;
    bitmap.CreateCompatibleBitmap(pDC, rect.Width(), rect.Height());
    
    // Select bitmap into memory DC
    CBitmap* pOldBitmap = memDC.SelectObject(&bitmap);
    
    // Fill background
    memDC.FillSolidRect(rect, RGB(255, 255, 255));
    
    // Draw to memory DC
    memDC.Rectangle(10, 10, 100, 100);
    memDC.TextOut(10, 120, _T("Double buffered text"));
    
    // Copy memory DC to screen DC
    pDC->BitBlt(rect.left, rect.top, rect.Width(), rect.Height(),
        &memDC, 0, 0, SRCCOPY);
    
    // Cleanup
    memDC.SelectObject(pOldBitmap);
}

// ============================================================================
// 10. BEST PRACTICES
// ============================================================================

/*
1. Always save and restore GDI objects (SelectObject returns previous)
2. Use CPaintDC only in OnPaint(), CClientDC elsewhere
3. Use double buffering for complex drawing to avoid flicker
4. Always check return values from GDI functions
5. Use CRect for rectangle operations (not raw RECT)
6. Use CreatePointFont for font creation (easier than CreateFont)
7. Clean up GDI objects when done (they're limited resources)
8. Use RGB macro for color values
9. Use MM_TEXT mapping mode for pixel-based drawing
10. Override OnEraseBkgnd to prevent flicker (return TRUE)
*/

#endif // _MFC_VER
