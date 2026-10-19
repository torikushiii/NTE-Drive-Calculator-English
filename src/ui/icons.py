# 加载 Lucide 线性图标并按主题着色，供侧边栏和顶栏使用。
"""Tinted Lucide line icons (ISC, see assets/icons/LICENSE-lucide.txt)."""

from __future__ import annotations

from functools import lru_cache

from PySide6.QtCore import QByteArray, QRectF, Qt
from PySide6.QtGui import QIcon, QPainter, QPixmap
from PySide6.QtSvg import QSvgRenderer

from src.app.theme_modern import ASSET_DIR

NAV_ICONS = {
    "home": "layout-dashboard",
    "execute": "calculator",
    "equipment": "layers",
    "my_role": "users",
    "warehouse": "package",
    "identify": "scan-search",
    "battle_report": "chart-column",
    "toolbox": "wrench",
    "plugins": "puzzle",
    "settings": "settings",
}


@lru_cache(maxsize=None)
def _svg(name: str) -> str:
    return (ASSET_DIR / "icons" / f"{name}.svg").read_text(encoding="utf-8")


def _pixmap(name: str, color: str, size: int, ratio: float) -> QPixmap:
    pixels = max(size, round(size * ratio))
    pixmap = QPixmap(pixels, pixels)
    pixmap.fill(Qt.transparent)
    renderer = QSvgRenderer(QByteArray(_svg(name).replace("currentColor", color).encode("utf-8")))
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    renderer.render(painter, QRectF(0, 0, pixels, pixels))
    painter.end()
    pixmap.setDevicePixelRatio(pixels / size)
    return pixmap


def tinted_icon(name: str, color: str, active_color: str | None = None, size: int = 18, ratio: float = 2.0) -> QIcon:
    """Icon drawn in `color`; checkable buttons switch to `active_color` when checked."""
    icon = QIcon()
    if not (ASSET_DIR / "icons" / f"{name}.svg").is_file():
        return icon
    normal = _pixmap(name, color, size, ratio)
    icon.addPixmap(normal, QIcon.Normal, QIcon.Off)
    icon.addPixmap(_pixmap(name, active_color or color, size, ratio), QIcon.Normal, QIcon.On)
    icon.addPixmap(normal, QIcon.Disabled, QIcon.Off)
    return icon


def strip_leading_symbols(text: str) -> str:
    """Drop emoji/symbol prefixes such as "⚡  " from a navigation label."""
    index = 0
    while index < len(text) and not text[index].isalnum():
        index += 1
    return text[index:] if index < len(text) else text
