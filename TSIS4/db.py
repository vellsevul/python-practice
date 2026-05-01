# db.py
import psycopg2
from datetime import datetime
from config import *

class Database:
    def __init__(self):
        """Initialize database connection"""
        self.conn = psycopg2.connect(
            host="localhost",
            database="snake_game",
            user="postgres",
            password="12345678", 
            port="5432"
        )
        self.cursor = self.conn.cursor()
        self.create_tables()
    
    def create_tables(self):
        """Create tables if they don't exist"""
        # Create players table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
        """)
        
        # Create game_sessions table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            )
        """)
        
        self.conn.commit()
    
    def get_or_create_player(self, username):
        """Get existing player or create new one"""
        self.cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
        result = self.cursor.fetchone()
        
        if result:
            return result[0]
        else:
            self.cursor.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id",
                (username,)
            )
            self.conn.commit()
            return self.cursor.fetchone()[0]
    
    def save_game_result(self, username, score, level):
        """Save game result to database"""
        player_id = self.get_or_create_player(username)
        self.cursor.execute("""
            INSERT INTO game_sessions (player_id, score, level_reached, played_at)
            VALUES (%s, %s, %s, %s)
        """, (player_id, score, level, datetime.now()))
        self.conn.commit()
    
    def get_leaderboard(self, limit=10):
        """Get top scores from database"""
        self.cursor.execute("""
            SELECT p.username, gs.score, gs.level_reached, gs.played_at
            FROM game_sessions gs
            JOIN players p ON gs.player_id = p.id
            ORDER BY gs.score DESC
            LIMIT %s
        """, (limit,))
        return self.cursor.fetchall()
    
    def get_personal_best(self, username):
        """Get player's best score"""
        player_id = self.get_or_create_player(username)
        self.cursor.execute("""
            SELECT MAX(score) FROM game_sessions 
            WHERE player_id = %s
        """, (player_id,))
        result = self.cursor.fetchone()
        return result[0] if result[0] else 0
    
    def close(self):
        """Close database connection"""
        self.cursor.close()
        self.conn.close()