"""
Database Module
Handles SQLite database operations for storing personality profiles
"""
import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path

class Database:
    """Manage personality twin database"""
    
    def __init__(self, db_path: str = "backend/db/personality_twin.db"):
        """Initialize database connection"""
        # Ensure directory exists
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_db(self) -> None:
        """Initialize database schema"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create profiles table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                text_input TEXT,
                personality_traits TEXT,
                emotion TEXT,
                sentiment_score REAL,
                avatar_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_profile(
        self,
        name: str,
        text_input: str,
        personality_traits: Dict[str, float],
        emotion: str,
        sentiment_score: float,
        avatar_url: str
    ) -> int:
        """
        Save personality profile to database
        
        Returns:
            Profile ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO profiles 
            (name, text_input, personality_traits, emotion, sentiment_score, avatar_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            name,
            text_input,
            json.dumps(personality_traits),
            emotion,
            sentiment_score,
            avatar_url
        ))
        
        profile_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Ensure we return an int, not None
        return int(profile_id) if profile_id is not None else 0
    
    def get_profile(self, profile_id: int) -> Optional[Dict[str, Any]]:
        """Get profile by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM profiles WHERE id = ?
        ''', (profile_id,))
        
        row: Optional[Tuple] = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'text_input': row[2],
                'personality_traits': json.loads(row[3]),
                'emotion': row[4],
                'sentiment_score': row[5],
                'avatar_url': row[6],
                'created_at': row[7]
            }
        return None
    
    def get_all_profiles(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent profiles"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM profiles 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows: List[Tuple] = cursor.fetchall()
        conn.close()
        
        profiles: List[Dict[str, Any]] = []
        for row in rows:
            profiles.append({
                'id': row[0],
                'name': row[1],
                'text_input': row[2],
                'personality_traits': json.loads(row[3]),
                'emotion': row[4],
                'sentiment_score': row[5],
                'avatar_url': row[6],
                'created_at': row[7]
            })
        
        return profiles
    
    def delete_profile(self, profile_id: int) -> bool:
        """Delete profile by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM profiles WHERE id = ?', (profile_id,))
        
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()
        
        return deleted
    
    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM profiles')
        count_result: Optional[Tuple] = cursor.fetchone()
        total = count_result[0] if count_result else 0
        
        # Get emotion distribution
        cursor.execute('''
            SELECT emotion, COUNT(*) as count 
            FROM profiles 
            GROUP BY emotion
        ''')
        emotion_rows: List[Tuple] = cursor.fetchall()
        emotions: Dict[str, int] = {}
        
        for row in emotion_rows:
            emotion_name = str(row[0])
            emotion_count = int(row[1])
            emotions[emotion_name] = emotion_count
        
        conn.close()
        
        return {
            'total_profiles': total,
            'emotion_distribution': emotions
        }