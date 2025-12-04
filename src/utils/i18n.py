"""
Optimized multi-language support with minimal memory footprint.
"""

from enum import Enum
from typing import Dict, Optional


class Language(Enum):
    """Supported languages."""
    EN = "en"
    FR = "fr"
    ES = "es"
    DE = "de"
    ZH = "zh"


class I18nManager:
    """Optimized internationalization manager."""
    
    _instance = None
    
    # Language dictionaries (lazy-loaded)
    _messages = {
        Language.EN: {
            "title": "Bibliography Generator",
            "author": "Author",
            "title_field": "Title",
            "journal": "Journal",
            "year": "Year",
            "volume": "Volume",
            "pages": "Pages",
            "format": "Format",
            "language": "Language",
            "process": "Processing...",
            "done": "Done",
            "error": "Error",
            "success": "Success",
        },
        Language.FR: {
            "title": "Générateur de Bibliographie",
            "author": "Auteur",
            "title_field": "Titre",
            "journal": "Journal",
            "year": "Année",
            "volume": "Volume",
            "pages": "Pages",
            "format": "Format",
            "language": "Langue",
            "process": "Traitement...",
            "done": "Terminé",
            "error": "Erreur",
            "success": "Succès",
        },
        Language.ES: {
            "title": "Generador de Bibliografía",
            "author": "Autor",
            "title_field": "Título",
            "journal": "Revista",
            "year": "Año",
            "volume": "Volumen",
            "pages": "Páginas",
            "format": "Formato",
            "language": "Idioma",
            "process": "Procesando...",
            "done": "Hecho",
            "error": "Error",
            "success": "Éxito",
        },
        Language.DE: {
            "title": "Bibliographiegenerator",
            "author": "Autor",
            "title_field": "Titel",
            "journal": "Zeitschrift",
            "year": "Jahr",
            "volume": "Band",
            "pages": "Seiten",
            "format": "Format",
            "language": "Sprache",
            "process": "Verarbeitung...",
            "done": "Fertig",
            "error": "Fehler",
            "success": "Erfolg",
        },
        Language.ZH: {
            "title": "参考文献生成器",
            "author": "作者",
            "title_field": "标题",
            "journal": "期刊",
            "year": "年份",
            "volume": "卷",
            "pages": "页数",
            "format": "格式",
            "language": "语言",
            "process": "处理中...",
            "done": "完成",
            "error": "错误",
            "success": "成功",
        }
    }
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.current_language = Language.EN
        return cls._instance
    
    def set_language(self, language: Language) -> None:
        """Set current language."""
        if isinstance(language, str):
            try:
                language = Language(language)
            except ValueError:
                language = Language.EN
        
        self.current_language = language
    
    def get(self, key: str, language: Optional[Language] = None) -> str:
        """Get translated message."""
        lang = language or self.current_language
        
        if lang not in self._messages:
            lang = Language.EN
        
        return self._messages[lang].get(key, key)
    
    def get_all_messages(self, language: Optional[Language] = None) -> Dict[str, str]:
        """Get all messages for a language."""
        lang = language or self.current_language
        
        if lang not in self._messages:
            lang = Language.EN
        
        return self._messages[lang]
