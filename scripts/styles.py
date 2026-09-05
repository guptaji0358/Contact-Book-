TABLE_STYLE = """
    QTableWidget {background-color: #2b2b2b;color: white;gridline-color: transparent;}
    QHeaderView::section {background-color: #1f1f1f;color: white;font-weight: bold;border: none;}
"""

INPUT_STYLE = """
    QLineEdit {border: 2px solid #cccccc;border-radius: 6px;padding: 6px;font-size: 14px;font-family: 'Segoe UI';font-weight:bold;}
    QLineEdit:focus {border: 2px solid #2563EB;}
"""

TEXT_BUTTON_STYLE = """
    QPushButton {{background-color: {bg};color: white;font-size: 16px;font-family: 'Segoe UI';border-radius: 8px;font-weight:bold;}}
    QPushButton:hover {{background-color: {hover};}}
    QPushButton:pressed {{background-color: {pressed};}}
"""

BLUE_BUTTON_STYLE = TEXT_BUTTON_STYLE.format(bg="#2563EB", hover="#3B82F6", pressed="#1E40AF")
GREY_BUTTON_STYLE = TEXT_BUTTON_STYLE.format(bg="#374151", hover="#2F3745", pressed="#1F2937")
RED_BUTTON_STYLE = TEXT_BUTTON_STYLE.format(bg="#EF4444", hover="#F87171", pressed="#B91C1C")

ICON_BUTTON_STYLE = """
    QPushButton {{
        background-color: {bg};
        border: 1px solid {border};
        border-radius: 14px;
    }}
    QPushButton:hover {{
        background-color: {hover};
        border: 1px solid {hover_border};
    }}
    QPushButton:pressed {{
        background-color: {pressed};
        border: 1px solid {pressed};
    }}
"""

ICON_BLUE_BUTTON_STYLE = ICON_BUTTON_STYLE.format(
    bg="#1F2A44", border="#2563EB", hover="#2563EB", hover_border="#3B82F6", pressed="#1E40AF"
)
ICON_GREY_BUTTON_STYLE = ICON_BUTTON_STYLE.format(
    bg="#262b33", border="#374151", hover="#374151", hover_border="#4B5563", pressed="#1F2937"
)
ICON_RED_BUTTON_STYLE = ICON_BUTTON_STYLE.format(
    bg="#3A1E1E", border="#EF4444", hover="#EF4444", hover_border="#F87171", pressed="#B91C1C"
)
ICON_GREEN_BUTTON_STYLE = ICON_BUTTON_STYLE.format(
    bg="#1B3A2A", border="#22C55E", hover="#22C55E", hover_border="#4ADE80", pressed="#15803D"
)

DIALOG_TITLE_STYLE = "font-size:24px; font-family:'Segoe UI'; font-weight:bold;"
DIALOG_LABEL_STYLE = "font-size:16px; font-family:'Segoe UI'; font-weight:bold;"

ROUND_BUTTON_STYLE = """
    QPushButton {{
        background-color: {bg};
        border: none;
        border-radius: {radius}px;
    }}
    QPushButton:hover {{background-color: {hover};}}
    QPushButton:pressed {{background-color: {pressed};}}
    QPushButton:checked {{background-color: {checked};}}
"""

CALL_TOGGLE_BUTTON_STYLE = ROUND_BUTTON_STYLE.format(
    bg="#374151", hover="#4B5563", pressed="#1F2937", checked="#2563EB", radius=30
)
CALL_END_BUTTON_STYLE = ROUND_BUTTON_STYLE.format(
    bg="#EF4444", hover="#F87171", pressed="#B91C1C", checked="#EF4444", radius=32
)
