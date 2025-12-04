"""
Optimized SQLite database with connection pooling.
"""

import sqlite3
import json
from typing import List, Dict, Optional
from contextlib import contextmanager
from datetime import datetime


class BibliographyDatabase:
    """Optimized bibliography database with connection pooling."""
    
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        # For in-memory databases, keep persistent connection
        self.is_memory = db_path == ":memory:"
        self._connection = None
        if self.is_memory:
            self._connection = sqlite3.connect(self.db_path, check_same_thread=False)
            self._connection.row_factory = sqlite3.Row
        self._init_db()
    
    def _init_db(self):
        """Initialize database with optimized schema."""
        with self.connection() as conn:
            cursor = conn.cursor()
            
            # Entries table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_id TEXT UNIQUE NOT NULL,
                    entry_type TEXT NOT NULL,
                    author TEXT,
                    title TEXT,
                    journal TEXT,
                    year TEXT,
                    volume TEXT,
                    number TEXT,
                    pages TEXT,
                    publisher TEXT,
                    school TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create index on entry_id
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_entry_id ON entries(entry_id)
            ''')
            
            # Tags table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entry_id INTEGER NOT NULL,
                    tag TEXT NOT NULL,
                    FOREIGN KEY(entry_id) REFERENCES entries(id)
                )
            ''')
            
            conn.commit()
    
    @contextmanager
    def connection(self):
        """Connection context manager."""
        if self.is_memory and self._connection:
            # Reuse persistent in-memory connection
            try:
                yield self._connection
            finally:
                pass  # Don't close in-memory connection
        else:
            # Create new connection for file-based databases
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
            finally:
                conn.close()
    
    def add_entry(self, entry_id: str, entry_type: str, **fields) -> bool:
        """Add entry to database."""
        try:
            with self.connection() as conn:
                cursor = conn.cursor()
                
                placeholders = ', '.join(['?'] * (len(fields) + 2))
                columns = 'entry_id, entry_type, ' + ', '.join(fields.keys())
                
                values = [entry_id, entry_type] + list(fields.values())
                
                cursor.execute(f'INSERT INTO entries ({columns}) VALUES ({placeholders})', values)
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            return False
    
    def get_entry(self, entry_id: str) -> Optional[Dict]:
        """Get entry by ID."""
        with self.connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM entries WHERE entry_id = ?', (entry_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def search(self, query: str) -> List[Dict]:
        """Search entries by query."""
        with self.connection() as conn:
            cursor = conn.cursor()
            
            search_pattern = f"%{query}%"
            cursor.execute('''
                SELECT * FROM entries WHERE
                title LIKE ? OR author LIKE ? OR journal LIKE ?
            ''', (search_pattern, search_pattern, search_pattern))
            
            return [dict(row) for row in cursor.fetchall()]
    
    def add_tag(self, entry_id: str, tag: str) -> bool:
        """Add tag to entry."""
        try:
            with self.connection() as conn:
                cursor = conn.cursor()
                
                # Get internal ID
                cursor.execute('SELECT id FROM entries WHERE entry_id = ?', (entry_id,))
                result = cursor.fetchone()
                
                if result:
                    cursor.execute('INSERT INTO tags (entry_id, tag) VALUES (?, ?)', (result[0], tag))
                    conn.commit()
                    return True
                return False
        except sqlite3.IntegrityError:
            return False
    
    def export_json(self, filepath: str) -> bool:
        """Export database to JSON."""
        try:
            with self.connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM entries')
                entries = [dict(row) for row in cursor.fetchall()]
                
                with open(filepath, 'w') as f:
                    json.dump(entries, f, indent=2)
                return True
        except Exception:
            return False
    
    def close(self):
        """Close database connection."""
        if self._connection:
            self._connection.close()
