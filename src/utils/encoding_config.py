#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive encoding configuration for Windows compatibility.
Handles UTF-8 console setup and provides robust fallback mechanisms.
"""

import sys
import os
import platform
import codecs
from typing import Optional


def configure_console_encoding() -> bool:
    """
    Configure console for UTF-8 output on Windows.
    Returns True if UTF-8 was successfully configured, False otherwise.
    """
    if platform.system() != "Windows":
        return True  # Non-Windows systems typically handle UTF-8 well
    
    try:
        # Method 1: Reconfigure stdout to use UTF-8
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8', errors='replace')
            sys.stderr.reconfigure(encoding='utf-8', errors='replace')
        
        # Method 2: Set Windows console code page to UTF-8 (65001)
        if hasattr(os, 'system'):
            os.system('chcp 65001 >nul 2>&1')
        
        # Method 3: Set environment variable for Python IO encoding
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        # Test if UTF-8 works by trying to encode a Unicode character
        test_char = "🔑"
        test_char.encode(sys.stdout.encoding or 'utf-8')
        
        return True
        
    except (UnicodeEncodeError, AttributeError, OSError):
        return False


def detect_console_encoding() -> str:
    """
    Detect the current console encoding.
    Returns the encoding name or 'ascii' as fallback.
    """
    try:
        if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding:
            return sys.stdout.encoding.lower()
        return 'utf-8'  # Default assumption
    except:
        return 'ascii'  # Safe fallback


def safe_encode_text(text: str, target_encoding: Optional[str] = None) -> str:
    """
    Safely encode text with multiple fallback levels.
    
    Args:
        text: The text to encode
        target_encoding: Target encoding (auto-detected if None)
    
    Returns:
        Safely encoded text that won't cause UnicodeEncodeError
    """
    if not text:
        return text
    
    if target_encoding is None:
        target_encoding = detect_console_encoding()
    
    # Level 1: Try original text if UTF-8 is supported
    if target_encoding in ['utf-8', 'utf8']:
        try:
            # Test if the text can be encoded
            text.encode('utf-8')
            return text
        except UnicodeEncodeError:
            pass
    
    # Level 2: Replace common Unicode characters with ASCII equivalents
    ascii_text = replace_unicode_chars(text)
    
    # Level 3: Force ASCII encoding with replacement characters
    try:
        # This will replace any remaining non-ASCII characters with '?'
        ascii_safe = ascii_text.encode('ascii', 'replace').decode('ascii')
        return ascii_safe
    except:
        # Level 4: Ultimate fallback - strip all non-ASCII characters
        return ''.join(char for char in ascii_text if ord(char) < 128)


def replace_unicode_chars(text: str) -> str:
    """
    Replace Unicode characters with ASCII equivalents.
    This is more comprehensive than the previous version.
    """
    # Emoji and symbol replacements
    replacements = {
        # Status indicators
        "✅": "[OK]",
        "❌": "[ERROR]", 
        "⚠️": "[WARNING]",
        "ℹ️": "[INFO]",
        "🔄": "[REFRESH]",
        "⭐": "*",
        "💡": "[TIP]",
        "📝": "[NOTE]",
        "🎯": "[TARGET]",
        
        # Application icons
        "🌐": "[WEB]",
        "🤖": "[AI]",
        "🔍": "[SEARCH]",
        "💻": "[CODE]",
        "📁": "[FOLDER]",
        "🏥": "[HEALTH]",
        "❓": "?",
        "⚙️": "[CONFIG]",
        "🚪": "[EXIT]",
        "🚀": "[LAUNCH]",
        "🔑": "[KEY]",
        "📊": "[CHART]",
        "🔧": "[TOOL]",
        "📦": "[PACKAGE]",
        "🎉": "[SUCCESS]",
        "💥": "[CRITICAL]",
        "🔥": "[HOT]",
        "⚡": "[FAST]",
        "🛠️": "[BUILD]",
        "📋": "[LIST]",
        "🎮": "[GAME]",
        "🌟": "[STAR]",
        "💎": "[GEM]",
        "🔒": "[LOCK]",
        "🔓": "[UNLOCK]",
        "📈": "[UP]",
        "📉": "[DOWN]",
        "🎨": "[ART]",
        "🧪": "[TEST]",
        "🔬": "[SCIENCE]",
        "📚": "[DOCS]",
        "💼": "[BUSINESS]",
        "🎪": "[CIRCUS]",
        "🎭": "[THEATER]",
        "🎵": "[MUSIC]",
        "🎬": "[MOVIE]",
        "📺": "[TV]",
        "📱": "[MOBILE]",
        "💾": "[DISK]",
        "🖥️": "[DESKTOP]",
        "⌨️": "[KEYBOARD]",
        "🖱️": "[MOUSE]",
        "🖨️": "[PRINTER]",
        "📷": "[CAMERA]",
        "🎥": "[VIDEO]",
        "🔊": "[SOUND]",
        "🔇": "[MUTE]",
        "📡": "[SIGNAL]",
        "🛰️": "[SATELLITE]",
        "🌍": "[EARTH]",
        "🌎": "[WORLD]",
        "🌏": "[GLOBE]",
        "🗺️": "[MAP]",
        "🧭": "[COMPASS]",
        "⏰": "[CLOCK]",
        "⏱️": "[TIMER]",
        "⏲️": "[STOPWATCH]",
        "🕐": "[1PM]",
        "📅": "[CALENDAR]",
        "📆": "[DATE]",
        "🗓️": "[SCHEDULE]",
        "📇": "[CARDS]",
        "🗃️": "[FILES]",
        "🗄️": "[CABINET]",
        "🗂️": "[DIVIDERS]",
        "📂": "[FOLDER]",
        "📃": "[PAGE]",
        "📄": "[DOCUMENT]",
        "📊": "[CHART]",
        "📈": "[TRENDING_UP]",
        "📉": "[TRENDING_DOWN]",
        "📋": "[CLIPBOARD]",
        "📌": "[PIN]",
        "📍": "[LOCATION]",
        "📎": "[PAPERCLIP]",
        "🖇️": "[CLIPS]",
        "📏": "[RULER]",
        "📐": "[TRIANGLE]",
        "✂️": "[SCISSORS]",
        "🖊️": "[PEN]",
        "🖋️": "[FOUNTAIN_PEN]",
        "✏️": "[PENCIL]",
        "🖍️": "[CRAYON]",
        "🖌️": "[BRUSH]",
        "🔍": "[MAGNIFY]",
        "🔎": "[SEARCH_RIGHT]",
        
        # Box drawing characters - comprehensive set
        "║": "|",
        "═": "=",
        "╔": "+",
        "╗": "+",
        "╚": "+",
        "╝": "+",
        "╠": "+",
        "╣": "+",
        "╦": "+",
        "╩": "+",
        "╬": "+",
        "│": "|",
        "─": "-",
        "┌": "+",
        "┐": "+",
        "└": "+",
        "┘": "+",
        "├": "+",
        "┤": "+",
        "┬": "+",
        "┴": "+",
        "┼": "+",
        "┏": "+",
        "┓": "+",
        "┗": "+",
        "┛": "+",
        "┣": "+",
        "┫": "+",
        "┳": "+",
        "┻": "+",
        "╋": "+",
        "▀": "^",
        "▄": "_",
        "█": "#",
        "▌": "|",
        "▐": "|",
        "░": ".",
        "▒": ":",
        "▓": "#",
        "■": "#",
        "□": "[]",
        "▪": "*",
        "▫": "o",
        "▬": "-",
        "▭": "-",
        "▮": "|",
        "▯": "[]",
        
        # Mathematical and technical symbols
        "∞": "infinity",
        "≈": "~=",
        "≠": "!=",
        "≤": "<=",
        "≥": ">=",
        "±": "+/-",
        "×": "x",
        "÷": "/",
        "√": "sqrt",
        "∑": "sum",
        "∏": "prod",
        "∫": "integral",
        "∂": "partial",
        "∆": "delta",
        "∇": "nabla",
        "∈": "in",
        "∉": "not_in",
        "∪": "union",
        "∩": "intersection",
        "⊂": "subset",
        "⊃": "superset",
        "⊆": "subset_eq",
        "⊇": "superset_eq",
        "∅": "empty_set",
        "∀": "for_all",
        "∃": "exists",
        "∄": "not_exists",
        "∧": "and",
        "∨": "or",
        "¬": "not",
        "→": "->",
        "←": "<-",
        "↔": "<->",
        "⇒": "=>",
        "⇐": "<=",
        "⇔": "<=>",
        "∴": "therefore",
        "∵": "because",
        "∝": "proportional",
        "∞": "infinity",
        "ℵ": "aleph",
        "ℶ": "beth",
        "ℷ": "gimel",
        "ℸ": "dalet",
        
        # Currency symbols
        "€": "EUR",
        "£": "GBP", 
        "¥": "JPY",
        "₹": "INR",
        "₽": "RUB",
        "₩": "KRW",
        "₪": "ILS",
        "₫": "VND",
        "₦": "NGN",
        "₡": "CRC",
        "₨": "Rs",
        "₱": "PHP",
        "₲": "PYG",
        "₴": "UAH",
        "₵": "GHS",
        "₶": "LVL",
        "₷": "SPL",
        "₸": "KZT",
        "₹": "INR",
        "₺": "TRY",
        "₻": "CE",
        "₼": "AZN",
        "₽": "RUB",
        "₾": "GEL",
        "₿": "BTC",
        
        # Arrows and directional indicators
        "↑": "^",
        "↓": "v", 
        "←": "<",
        "→": ">",
        "↖": "\\",
        "↗": "/",
        "↘": "\\",
        "↙": "/",
        "↕": "|",
        "↔": "<->",
        "⤴": "^",
        "⤵": "v",
        "⬆": "^",
        "⬇": "v",
        "⬅": "<",
        "➡": ">",
        "⬈": "/",
        "⬉": "\\",
        "⬊": "\\", 
        "⬋": "/",
        "⬌": "<->",
        "⬍": "<->",
        
        # Quotation marks and punctuation
        """: '"',
        """: '"',
        "'": "'",
        "'": "'",
        "«": "<<",
        "»": ">>",
        "‹": "<",
        "›": ">",
        "„": '"',
        "‚": "'",
        "‛": "'",
        "‟": '"',
        "…": "...",
        "–": "-",
        "—": "--",
        "‒": "-",
        "―": "---",
        "‖": "||",
        "‗": "_",
        "†": "+",
        "‡": "++",
        "•": "*",
        "‰": "o/oo",
        "′": "'",
        "″": '"',
        "‴": "'''",
        "‵": "`",
        "‶": "``",
        "‷": "```",
        "‸": "^",
        "‹": "<",
        "›": ">",
        "※": "*",
        "‼": "!!",
        "⁇": "??",
        "⁈": "?!",
        "⁉": "!?",
        "⁏": ";",
        "⁐": "*",
        "⁑": "**",
        "⁒": "%",
        "⁓": "~",
        "⁔": ".",
        "⁕": "*",
        "⁖": ".",
        "⁗": "''''",
        "⁘": "^",
        "⁙": ".....",
        "⁚": ":",
        "⁛": "***",
        "⁜": "-",
        "⁝": ":",
        "⁞": ":",
        
        # Miscellaneous symbols
        "©": "(C)",
        "®": "(R)",
        "™": "(TM)",
        "℠": "(SM)",
        "℗": "(P)",
        "№": "No.",
        "℃": "C",
        "℉": "F",
        "Ω": "Ohm",
        "℧": "Mho",
        "Å": "A",
        "℮": "e",
        "⅍": "A/S",
        "ℓ": "l",
        "℥": "oz",
        "Ⅎ": "F",
        "⅁": "G",
        "⅂": "L",
        "⅃": "L",
        "⅄": "Y",
        "ℇ": "E",
        "℈": "SCRUPLE",
        "ℊ": "g",
        "ℋ": "H",
        "ℌ": "H",
        "ℍ": "H",
        "ℎ": "h",
        "ℏ": "h",
        "ℐ": "I",
        "ℑ": "I",
        "ℒ": "L",
        "ℓ": "l",
        "℔": "lb",
        "ℕ": "N",
        "№": "N",
        "℗": "(P)",
        "℘": "P",
        "ℙ": "P",
        "ℚ": "Q",
        "ℛ": "R",
        "ℜ": "R",
        "ℝ": "R",
        "℞": "Rx",
        "℟": "RESPONSE",
        "℠": "(SM)",
        "℡": "TEL",
        "™": "(TM)",
        "℣": "V",
        "ℤ": "Z",
        "℥": "oz",
        "Ω": "Ohm",
        "℧": "Mho",
        "ℨ": "Z",
        "℩": "deg",
        "K": "K",
        "Å": "A",
        "ℬ": "B",
        "ℭ": "C",
        "℮": "e",
        "ℯ": "e",
        "ℰ": "E",
        "ℱ": "F",
        "Ⅎ": "F",
        "ℳ": "M",
        "ℴ": "o",
        "ℵ": "aleph",
        "ℶ": "beth",
        "ℷ": "gimel",
        "ℸ": "dalet",
        "ℹ": "i",
        "℺": "ROTATED_Q",
        "℻": "FAX",
        "ℼ": "pi",
        "ℽ": "gamma",
        "ℾ": "GAMMA",
        "ℿ": "PI",
        "⅀": "SUM",
        "⅁": "G",
        "⅂": "L",
        "⅃": "L",
        "⅄": "Y",
        "ⅅ": "D",
        "ⅆ": "d",
        "ⅇ": "e",
        "ⅈ": "i",
        "ⅉ": "j",
        "⅊": "PROPERTY_LINE",
        "⅋": "&",
        "⅌": "PER",
        "⅍": "A/S",
        "ⅎ": "TURNED_F",
        "⅏": "SYMBOL_FOR_SAMARITAN",
    }
    
    # Apply all replacements
    result = text
    for unicode_char, ascii_replacement in replacements.items():
        result = result.replace(unicode_char, ascii_replacement)
    
    return result


# Global flag to track if UTF-8 was successfully configured
_utf8_configured = None

def is_utf8_available() -> bool:
    """Check if UTF-8 encoding is available and working."""
    global _utf8_configured
    if _utf8_configured is None:
        _utf8_configured = configure_console_encoding()
    return _utf8_configured


def safe_print(text: str) -> None:
    """
    Print text with comprehensive encoding safety.
    This is the main function that should be used throughout the application.
    """
    if not text:
        print()
        return
    
    try:
        # Try direct print first (works if UTF-8 is properly configured)
        print(text)
    except UnicodeEncodeError:
        # Fall back to safe encoding
        safe_text = safe_encode_text(text)
        try:
            print(safe_text)
        except UnicodeEncodeError:
            # Ultimate fallback: strip all non-ASCII and print
            ascii_only = ''.join(char for char in safe_text if ord(char) < 128)
            print(ascii_only)
