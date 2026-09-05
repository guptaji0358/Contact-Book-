from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

ICON_EYE = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M1.5 12S5 5 12 5s10.5 7 10.5 7-3.5 7-10.5 7S1.5 12 1.5 12Z"
        stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>
  <circle cx="12" cy="12" r="3.2" stroke="{color}" stroke-width="1.8"/>
</svg>
"""

ICON_PLUS = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 5v14M5 12h14" stroke="{color}" stroke-width="2.2" stroke-linecap="round"/>
</svg>
"""

ICON_TRASH = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M4 7h16" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M9 7V4.8c0-.44.36-.8.8-.8h4.4c.44 0 .8.36.8.8V7"
        stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M6 7l1 12.2c.05.98.86 1.8 1.85 1.8h6.3c.99 0 1.8-.82 1.85-1.8L18 7"
        stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M10 11v6M14 11v6" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
</svg>
"""

ICON_PENCIL = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M4 20l.9-3.9L16.2 4.8a1.4 1.4 0 0 1 2 0l1 1a1.4 1.4 0 0 1 0 2L7.9 19.1 4 20Z"
        stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>
  <path d="M14.6 6.4l3 3" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
</svg>
"""

ICON_CLOUD_DOWN = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M7.5 17.5A4.5 4.5 0 0 1 8 8.6a5.5 5.5 0 0 1 10.6 1.9A3.9 3.9 0 0 1 18 17.5H7.5Z"
        stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>
  <path d="M12 11v6.5M9.2 15.2 12 18l2.8-2.8" stroke="{color}" stroke-width="1.8"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

ICON_PHONE = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M5.3 3.5h3.1c.5 0 .95.34 1.08.82l.9 3.3a1.13 1.13 0 0 1-.32 1.14l-1.7 1.55a13.7 13.7 0 0 0 5.83 5.83l1.55-1.7a1.13 1.13 0 0 1 1.14-.32l3.3.9c.48.13.82.58.82 1.08v3.1c0 .63-.53 1.13-1.16 1.09-8.02-.5-14.4-6.88-14.9-14.9-.04-.63.46-1.16 1.09-1.16Z"
        stroke="{color}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
</svg>
"""

ICON_CLOUD_UP = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M7.5 17.5A4.5 4.5 0 0 1 8 8.6a5.5 5.5 0 0 1 10.6 1.9A3.9 3.9 0 0 1 18 17.5H7.5Z"
        stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>
  <path d="M12 17.5V11M9.2 13.3 12 10.5l2.8 2.8" stroke="{color}" stroke-width="1.8"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


ICON_MIC = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="9" y="2.5" width="6" height="11" rx="3" stroke="{color}" stroke-width="1.8"/>
  <path d="M5.5 11.5a6.5 6.5 0 0 0 13 0" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M12 18v3.5M8.5 21.5h7" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
</svg>
"""

ICON_MIC_OFF = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="9" y="2.5" width="6" height="11" rx="3" stroke="{color}" stroke-width="1.8"/>
  <path d="M5.5 11.5a6.5 6.5 0 0 0 13 0" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M12 18v3.5M8.5 21.5h7" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
  <path d="M3 3l18 18" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
</svg>
"""

ICON_SPEAKER = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M4 9.5v5h3.6L13 19V5L7.6 9.5H4Z" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>
  <path d="M16.2 8.8a4.8 4.8 0 0 1 0 6.4M18.8 6.3a8.6 8.6 0 0 1 0 11.4" stroke="{color}" stroke-width="1.8" stroke-linecap="round"/>
</svg>
"""

ICON_END_CALL = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M2.5 13.8c4-3.4 15-3.4 19 0a1.1 1.1 0 0 1 .15 1.5l-1.9 2.4a1.1 1.1 0 0 1-1.4.28l-2.6-1.4a1.1 1.1 0 0 1-.55-1.1l.25-1.7c-2.2-.7-4.7-.7-6.9 0l.25 1.7a1.1 1.1 0 0 1-.55 1.1l-2.6 1.4a1.1 1.1 0 0 1-1.4-.28l-1.9-2.4a1.1 1.1 0 0 1 .15-1.5Z"
        stroke="{color}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
</svg>
"""


ICON_BOOK = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M4 4.5h6.5a2 2 0 0 1 2 2V20a1.6 1.6 0 0 0-1.6-1.6H4Z" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>
  <path d="M20 4.5h-6.5a2 2 0 0 0-2 2V20a1.6 1.6 0 0 1 1.6-1.6H20Z" stroke="{color}" stroke-width="1.8" stroke-linejoin="round"/>
</svg>
"""


def svg_icon(svg_template, color="#ffffff", size=28):
    svg_data = svg_template.format(color=color)
    renderer = QSvgRenderer(QByteArray(svg_data.encode("utf-8")))

    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    renderer.render(painter, QRectF(0, 0, size, size))
    painter.end()

    return QIcon(pixmap)
