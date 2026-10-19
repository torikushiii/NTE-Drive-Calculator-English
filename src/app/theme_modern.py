# 定义“现代”主题：统一的中性色阶、单一强调色、Inter 字体与控件样式。
"""Modern theme: neutral surfaces, one accent colour, Inter, consistent controls.

Inline styles across the app are written against the GitHub-dark palette
(`#0d1117`, `#161b22`, `#1f6feb`, ...). `map_modern_colors` re-maps those
literals in a single regex pass, so mapping is idempotent: no output colour is
also a key. Eight-digit literals such as `#1f6feb33` were authored as CSS
`#RRGGBBAA`, but Qt reads them as `#AARRGGBB`; the mapper emits `rgba()` so the
intended translucent tint is what actually renders.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from PySide6.QtGui import QColor, QFontDatabase, QPalette
from PySide6.QtWidgets import QApplication

if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    ASSET_DIR = Path(sys._MEIPASS) / "assets"
else:
    ASSET_DIR = Path(__file__).resolve().parents[2] / "assets"

# Neutral scale (cool zinc), one indigo accent, calmer status colours.
BG = "#0e0f13"
BG_SIDE = "#121318"
SURFACE = "#16171c"
RAISED = "#1d1f25"
BORDER = "#24262d"
BORDER_CONTROL = "#2e3139"
BORDER_STRONG = "#454954"
TEXT = "#e3e5ea"
TEXT_STRONG = "#f6f7f9"
TEXT_MUTED = "#9599a4"
TEXT_FAINT = "#6c707b"
ACCENT = "#6366f1"
ACCENT_HOVER = "#7b7ef4"
ACCENT_TEXT = "#a5a8ff"
DANGER = "#e5484d"
DANGER_TEXT = "#ff8a8f"
SUCCESS_TEXT = "#4cc38a"
WARNING_TEXT = "#e2a336"

MODERN_COLOR_MAP = {
    "#0d1117": BG,
    "#10151c": "#121318",
    "#161b22": SURFACE,
    "#1c2128": RAISED,
    "#21262d": BORDER,
    "#30363d": BORDER_CONTROL,
    "#484f58": BORDER_STRONG,
    "#c9d1d9": TEXT,
    "#f0f6fc": TEXT_STRONG,
    "#8b949e": TEXT_MUTED,
    "#6e7681": TEXT_FAINT,
    # Blue family becomes the single indigo accent.
    "#1f6feb": ACCENT,
    "#2f81f7": "#6c6ff2",
    "#388bfd": ACCENT_HOVER,
    "#58a6ff": ACCENT_TEXT,
    "#79c0ff": "#c3c5ff",
    "#10243f": "#1c1d33",
    "#0d1f35": "#19192d",
    "#13233a": "#1d1e35",
    "#172a45": "#202140",
    # Filled green call-to-action buttons become the accent; green stays
    # for success text so status meaning survives.
    "#238636": ACCENT,
    "#2ea043": ACCENT_HOVER,
    "#1b3a24": "#1f2033",
    "#3fb950": SUCCESS_TEXT,
    "#56d364": "#5fd39a",
    "#7ee787": "#86e0b0",
    "#da3633": DANGER,
    "#f85149": "#f2555a",
    "#ff7b72": DANGER_TEXT,
    "#2d1117": "#2a1618",
    "#3c151c": "#361a1e",
    "#5b2026": "#4a2025",
    "#d2991d": WARNING_TEXT,
    "#d29922": "#e2a33a",
    "#e3b341": "#eab54a",
    "#3a2f13": "#33291a",
    "#4dd0e1": "#5cc8e0",
    # Toolbox entry buttons are light-blue chips with navy text in every
    # other theme; render them as indigo tonal buttons instead.
    "#d6f0ff": "#2a2b52",
    "#b6e3ff": "#34356a",
    "#9ed5f5": "#24254a",
    "#a5d6ff": "#8f92ff",
    "#0b3150": "#e0e1ff",
}
assert not set(MODERN_COLOR_MAP.values()) & set(MODERN_COLOR_MAP), "modern map must be idempotent"

_HEX = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6})(?![0-9a-fA-F])")


def _rgba(rgb: str, alpha_hex: str) -> str:
    color = QColor(rgb)
    return f"rgba({color.red()},{color.green()},{color.blue()},{int(alpha_hex, 16)})"


def _replace(match: re.Match[str]) -> str:
    literal = match.group(0)
    key = literal.lower()
    if len(key) == 7:
        return MODERN_COLOR_MAP.get(key, literal)
    rgb = key[:7]
    if rgb not in MODERN_COLOR_MAP:
        return literal
    return _rgba(MODERN_COLOR_MAP[rgb], key[7:])


def map_modern_colors(style: str) -> str:
    return _HEX.sub(_replace, style)


def modern_color(dark_color: str) -> str:
    """Single colour for QColor/painter use; alpha literals come back as #AARRGGBB."""
    key = dark_color.lower()
    if len(key) == 9 and key[:7] in MODERN_COLOR_MAP:
        return "#" + key[7:] + MODERN_COLOR_MAP[key[:7]][1:]
    return MODERN_COLOR_MAP.get(key, dark_color)


_FONTS_LOADED = False


def load_modern_fonts() -> None:
    global _FONTS_LOADED
    if _FONTS_LOADED:
        return
    _FONTS_LOADED = True
    for path in sorted((ASSET_DIR / "fonts" / "inter").glob("*.ttf")):
        QFontDatabase.addApplicationFont(str(path))


def _url(name: str) -> str:
    return (ASSET_DIR / "icons" / "ui" / name).as_posix()


def _build_style() -> str:
    chevron, check = _url("chevron-down.svg"), _url("check.svg")
    return f"""
QMainWindow{{background:{BG};border:1px solid {BORDER};border-radius:10px}}
QDialog{{background:{BG};border:1px solid {BORDER};border-radius:10px}}
QWidget{{color:{TEXT};font-family:"Inter","Segoe UI","Microsoft YaHei UI",sans-serif;font-size:13px}}

#card{{background:{SURFACE};border:1px solid {BORDER};border-radius:12px}}
#cardTitle{{font-size:14px;font-weight:600;color:{TEXT_STRONG}}}

QFrame#dashboardMetricCard{{background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:4px}}
QLabel#dashboardMetricTitle{{color:{TEXT_MUTED};font-size:12px;font-weight:500}}
QLabel#dashboardMetricValue{{color:{TEXT_STRONG};font-size:26px;font-weight:600}}
QLabel#dashboardMetricSubtitle{{color:{TEXT_FAINT};font-size:11px}}
QLabel#statusBadge{{border-radius:10px;padding:3px 10px;font-size:11px;font-weight:600}}
QLabel#statusBadge[tone="success"]{{color:{SUCCESS_TEXT};background:rgba(76,195,138,28);border:1px solid rgba(76,195,138,90)}}
QLabel#statusBadge[tone="warning"]{{color:{WARNING_TEXT};background:rgba(226,163,54,28);border:1px solid rgba(226,163,54,90)}}
QLabel#statusBadge[tone="error"]{{color:{DANGER_TEXT};background:rgba(229,72,77,28);border:1px solid rgba(229,72,77,90)}}
QLabel#statusBadge[tone="active"]{{color:{ACCENT_TEXT};background:rgba(99,102,241,36);border:1px solid rgba(99,102,241,110)}}
QLabel#statusBadge[tone="neutral"]{{color:{TEXT_MUTED};background:{RAISED};border:1px solid {BORDER_CONTROL}}}

#sidebar{{background:{BG_SIDE};border-right:1px solid {BORDER};min-width:200px;max-width:200px;border-bottom-left-radius:10px}}
#sidebar QPushButton{{background:transparent;color:{TEXT_MUTED};border:none;border-radius:8px;padding:9px 12px;text-align:left;font-size:13px;font-weight:500;margin:1px 10px}}
#sidebar QPushButton:hover{{background:{RAISED};color:{TEXT}}}
#sidebar QPushButton:checked{{background:rgba(99,102,241,40);color:{TEXT_STRONG}}}
#sidebar QPushButton#workModeButton{{color:{TEXT_FAINT};font-size:12px;margin-top:10px}}
#sidebar QLabel#sidebarSection{{color:{TEXT_FAINT};font-size:11px;font-weight:600;padding:14px 22px 4px 22px}}

#titleBar{{background:{BG_SIDE};border-bottom:1px solid {BORDER};border-top-left-radius:10px;border-top-right-radius:10px}}
#titleBar QLabel{{font-size:12px;font-weight:600;color:{TEXT_MUTED}}}
#titleBar QPushButton{{background:transparent;border:none;border-radius:6px;color:{TEXT_MUTED};font-size:13px;padding:4px 10px;font-weight:500;min-height:0}}
#titleBar QPushButton:hover{{background:{RAISED};color:{TEXT}}}
#titleBar #btnClose:hover{{background:{DANGER};color:#fff}}

#topbar{{background:{BG};border-bottom:1px solid {BORDER};padding:10px 20px}}
#topbar QLabel{{font-size:16px;font-weight:600;color:{TEXT_STRONG}}}
#topbar QLabel#topbarStatus{{font-size:12px;font-weight:500;padding:5px 10px;background:{SURFACE};border:1px solid {BORDER_CONTROL};border-radius:13px;margin-left:4px}}

QPushButton{{background:{RAISED};color:{TEXT};border:1px solid {BORDER_CONTROL};border-radius:8px;padding:6px 14px;font-weight:500;min-height:20px}}
QPushButton:hover{{background:#25272e;border-color:#3a3d46}}
QPushButton:pressed{{background:{SURFACE}}}
QPushButton:focus{{outline:none}}
QPushButton:disabled{{background:{SURFACE};color:{TEXT_FAINT};border-color:{BORDER}}}
QPushButton#btnPrimary{{background:{ACCENT};color:#fff;border:1px solid {ACCENT};font-weight:600}}
QPushButton#btnPrimary:hover{{background:{ACCENT_HOVER};border-color:{ACCENT_HOVER}}}
QPushButton#btnPrimary:disabled{{background:#1f2033;color:{TEXT_FAINT};border-color:#1f2033}}
QPushButton#btnNew{{background:rgba(99,102,241,36);color:#c3c5ff;border:1px solid rgba(99,102,241,100);font-weight:600}}
QPushButton#btnNew:hover{{background:rgba(99,102,241,64)}}
QPushButton#allocationFilterSettingsButton{{background:rgba(99,102,241,36);color:#c3c5ff;border:1px solid rgba(99,102,241,100);border-radius:6px;font-size:12px;font-weight:600;padding:0 8px;min-height:0}}
QPushButton#allocationFilterSettingsButton:hover{{background:rgba(99,102,241,64)}}
QPushButton#allocationFilterHelp{{background:transparent;border:1px solid {BORDER_CONTROL};border-radius:10px;color:{TEXT_FAINT};font-size:11px;font-weight:600;padding:0;min-width:20px;max-width:20px;min-height:20px;max-height:20px}}
QPushButton#allocationFilterHelp:hover{{background:rgba(99,102,241,40);color:{ACCENT_TEXT};border-color:rgba(99,102,241,140)}}
QPushButton#btnDanger{{background:rgba(229,72,77,26);color:{DANGER_TEXT};border:1px solid rgba(229,72,77,90)}}
QPushButton#btnDanger:hover{{background:rgba(229,72,77,52)}}
QPushButton#btnAction{{background:transparent;color:{TEXT};border:1px solid {BORDER_CONTROL};font-size:12px;padding:5px 12px}}
QPushButton#btnAction:hover{{background:{RAISED}}}
QPushButton#btnSm{{font-size:11px;padding:3px 8px;min-width:28px;min-height:18px}}
QPushButton#btnHelp{{background:transparent;border:1px solid {BORDER_CONTROL};border-radius:10px;color:{TEXT_FAINT};font-size:11px;font-weight:600;padding:0;min-width:20px;max-width:20px;min-height:20px;max-height:20px}}
QPushButton#btnHelp:hover{{background:rgba(99,102,241,40);color:{ACCENT_TEXT};border-color:rgba(99,102,241,140)}}

QLineEdit,QTextEdit,QPlainTextEdit,QSpinBox,QDoubleSpinBox,QComboBox{{background:{BG};color:{TEXT};border:1px solid {BORDER_CONTROL};border-radius:8px;padding:6px 10px;selection-background-color:rgba(99,102,241,110)}}
QLineEdit:hover,QSpinBox:hover,QDoubleSpinBox:hover,QComboBox:hover{{border-color:#3a3d46}}
QLineEdit:focus,QTextEdit:focus,QPlainTextEdit:focus,QSpinBox:focus,QDoubleSpinBox:focus,QComboBox:focus{{border:1px solid {ACCENT}}}
QLineEdit:disabled,QSpinBox:disabled,QDoubleSpinBox:disabled,QComboBox:disabled{{color:{TEXT_FAINT};background:{SURFACE}}}
QDoubleSpinBox#rewindCustomPercent:enabled{{background:rgba(99,102,241,36);border-color:{ACCENT}}}
QToolButton#rewindPercentStepUp,QToolButton#rewindPercentStepDown{{background:rgba(99,102,241,36);color:{ACCENT_TEXT};border:1px solid rgba(99,102,241,140);border-radius:4px;padding:0;min-width:20px;max-width:20px;min-height:15px;max-height:15px;font-size:10px;font-weight:700}}
QToolButton#rewindPercentStepUp:hover,QToolButton#rewindPercentStepDown:hover{{background:rgba(99,102,241,72)}}
QToolButton#rewindPercentStepUp:pressed,QToolButton#rewindPercentStepDown:pressed{{background:rgba(99,102,241,72)}}
QToolButton#rewindPercentStepUp:disabled,QToolButton#rewindPercentStepDown:disabled{{background:transparent;color:{TEXT_FAINT};border-color:{BORDER_CONTROL}}}
QComboBox{{padding-right:26px}}
QComboBox::drop-down{{border:none;width:24px;subcontrol-origin:padding;subcontrol-position:center right}}
QComboBox::down-arrow{{image:url("{chevron}");width:14px;height:14px}}
QComboBox QAbstractItemView{{background:{SURFACE};border:1px solid {BORDER_CONTROL};border-radius:8px;padding:4px;outline:none;selection-background-color:rgba(99,102,241,48);selection-color:{TEXT_STRONG}}}

QRadioButton{{spacing:8px;padding:5px 0}}
QRadioButton::indicator{{width:16px;height:16px;border-radius:9px;border:1px solid {BORDER_STRONG};background:{BG}}}
QRadioButton::indicator:hover{{border-color:{ACCENT}}}
QRadioButton::indicator:checked{{border:1px solid {ACCENT};background:qradialgradient(cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0 #ffffff,stop:0.34 #ffffff,stop:0.42 {ACCENT},stop:1 {ACCENT})}}
QCheckBox{{spacing:8px}}
QCheckBox::indicator{{width:16px;height:16px;border-radius:5px;border:1px solid {BORDER_STRONG};background:{BG}}}
QCheckBox::indicator:hover{{border-color:{ACCENT}}}
QCheckBox::indicator:checked{{background:{ACCENT};border-color:{ACCENT};image:url("{check}")}}
QCheckBox::indicator:disabled{{background:{SURFACE};border-color:{BORDER}}}
QCheckBox#autoDiscardToggle{{spacing:8px;padding:5px 0}}
QCheckBox#autoDiscardToggle::indicator{{width:16px;height:16px;border-radius:9px;border:1px solid {BORDER_STRONG};background:{BG};image:none}}
QCheckBox#autoDiscardToggle::indicator:checked{{border:1px solid {ACCENT};background:qradialgradient(cx:0.5,cy:0.5,radius:0.5,fx:0.5,fy:0.5,stop:0 #ffffff,stop:0.34 #ffffff,stop:0.42 {ACCENT},stop:1 {ACCENT})}}
QCheckBox#autoDiscardToggle::indicator:hover{{border-color:{ACCENT}}}

QScrollArea{{border:none;background:transparent}}
QScrollBar:vertical{{background:transparent;width:10px;margin:2px}}
QScrollBar::handle:vertical{{background:{BORDER_CONTROL};border-radius:3px;min-height:32px}}
QScrollBar::handle:vertical:hover{{background:{BORDER_STRONG}}}
QScrollBar:horizontal{{background:transparent;height:10px;margin:2px}}
QScrollBar::handle:horizontal{{background:{BORDER_CONTROL};border-radius:3px;min-width:32px}}
QScrollBar::handle:horizontal:hover{{background:{BORDER_STRONG}}}
QScrollBar::add-line,QScrollBar::sub-line{{width:0;height:0}}
QScrollBar::add-page,QScrollBar::sub-page{{background:transparent}}

QTabWidget::pane{{border:1px solid {BORDER};background:{BG};border-radius:10px;top:-1px}}
QTabBar::tab{{background:transparent;color:{TEXT_MUTED};padding:8px 14px;border:none;border-bottom:2px solid transparent;margin-right:2px;font-weight:500}}
QTabBar::tab:hover{{color:{TEXT}}}
QTabBar::tab:selected{{color:{TEXT_STRONG};border-bottom:2px solid {ACCENT}}}
QTabBar QToolButton{{background:{RAISED};border:1px solid {BORDER_CONTROL};border-radius:6px;margin:4px 1px}}

QHeaderView::section{{background:{SURFACE};color:{TEXT_MUTED};border:none;border-bottom:1px solid {BORDER};padding:5px 6px;font-weight:600;font-size:12px}}
QTableView,QTableWidget,QListView,QListWidget,QTreeView,QTreeWidget{{background:{BG};border:1px solid {BORDER};border-radius:10px;gridline-color:{BORDER};selection-background-color:rgba(99,102,241,48);selection-color:{TEXT_STRONG};alternate-background-color:{SURFACE}}}
QTableCornerButton::section{{background:{SURFACE};border:none}}

QMenu{{background:{SURFACE};border:1px solid {BORDER_CONTROL};border-radius:8px;padding:4px}}
QMenu::item{{padding:6px 14px;border-radius:6px}}
QMenu::item:selected{{background:rgba(99,102,241,48)}}
QMenu::separator{{height:1px;background:{BORDER};margin:4px 6px}}

QProgressBar{{background:{RAISED};border:none;border-radius:4px;text-align:center;color:{TEXT};min-height:8px}}
QProgressBar::chunk{{background:{ACCENT};border-radius:4px}}
QSlider::groove:horizontal{{height:4px;background:{BORDER_CONTROL};border-radius:2px}}
QSlider::sub-page:horizontal{{background:{ACCENT};border-radius:2px}}
QSlider::handle:horizontal{{background:{TEXT_STRONG};width:14px;height:14px;margin:-5px 0;border-radius:7px}}

QToolTip{{background-color:{RAISED};color:{TEXT};border:1px solid {BORDER_CONTROL};border-radius:8px;padding:6px 10px;font-size:12px;opacity:255}}

QGroupBox{{background:{SURFACE};border:1px solid {BORDER};border-radius:12px;margin-top:30px;padding:20px;font-size:14px;font-weight:600;color:{TEXT_STRONG}}}
QGroupBox::title{{subcontrol-origin:margin;subcontrol-position:top left;left:4px;top:4px;padding:0}}

#logPanel{{background:{BG_SIDE};border-top:1px solid {BORDER}}}
#logPanel QTextEdit{{background:{BG_SIDE};border:none;color:{TEXT_MUTED};font-family:'Cascadia Code','Consolas',monospace;font-size:11px}}

QKeySequenceEdit{{background:{BG};color:{TEXT};border:1px solid {BORDER_CONTROL};border-radius:8px;padding:6px 8px;font-family:'Cascadia Code','Consolas',monospace;font-size:12px}}
"""


MODERN_STYLE = _build_style()


def apply_modern_palette(app: QApplication) -> None:
    palette = QPalette()
    for role, color in (
        (QPalette.Window, BG),
        (QPalette.WindowText, TEXT),
        (QPalette.Base, BG),
        (QPalette.AlternateBase, SURFACE),
        (QPalette.ToolTipBase, RAISED),
        (QPalette.ToolTipText, TEXT),
        (QPalette.Text, TEXT),
        (QPalette.PlaceholderText, TEXT_FAINT),
        (QPalette.Button, RAISED),
        (QPalette.ButtonText, TEXT),
        (QPalette.BrightText, "#ffffff"),
        (QPalette.Highlight, ACCENT),
        (QPalette.HighlightedText, "#ffffff"),
        (QPalette.Link, ACCENT_TEXT),
    ):
        palette.setColor(role, QColor(color))
    app.setPalette(palette)
