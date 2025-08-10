import time
import uuid
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class ChatMessage:
    id: str
    timestamp: datetime
    role: str
    content: str
    language: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ChatSession:
    session_id: str
    created_at: datetime
    last_activity: datetime
    messages: List[ChatMessage] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_message(self, role: str, content: str, language: str, **kwargs) -> str:
        message_id = str(uuid.uuid4())
        message = ChatMessage(
            id=message_id,
            timestamp=datetime.now(),
            role=role,
            content=content,
            language=language,
            metadata=kwargs
        )
        
        self.messages.append(message)
        self.last_activity = datetime.now()
        
        return message_id
    
    def get_recent_messages(self, count: int = 5) -> List[ChatMessage]:
        """
        Get the most recent messages from the session.
        
        Args:
            count: Number of recent messages to return
            
        Returns:
            List of recent messages
        """
        return self.messages[-count:] if self.messages else []
    
    def get_conversation_context(self, max_messages: int = 3) -> List[str]:
        """
        Get conversation context as a list of message contents.
        
        Args:
            max_messages: Maximum number of messages to include
            
        Returns:
            List of message contents for context
        """
        recent_messages = self.get_recent_messages(max_messages)
        return [msg.content for msg in recent_messages]
    
    def is_active(self, timeout_minutes: int = 30) -> bool:
        """
        Check if the session is still active.
        
        Args:
            timeout_minutes: Minutes of inactivity before session expires
            
        Returns:
            True if session is active, False otherwise
        """
        timeout = timedelta(minutes=timeout_minutes)
        return datetime.now() - self.last_activity < timeout
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the session.
        
        Returns:
            Dictionary with session summary information
        """
        return {
            'session_id': self.session_id,
            'created_at': self.created_at.isoformat(),
            'last_activity': self.last_activity.isoformat(),
            'total_messages': len(self.messages),
            'languages_used': list(set(msg.language for msg in self.messages)),
            'is_active': self.is_active()
        }

class SessionManager:
    """
    Manages chat sessions and provides conversation context.
    
    This class handles session creation, message storage, and context
    retrieval for the multilingual chatbot.
    """
    
    def __init__(self, session_timeout_minutes: int = 30, max_sessions: int = 100):
        """
        Initialize the session manager.
        
        Args:
            session_timeout_minutes: Minutes before inactive sessions expire
            max_sessions: Maximum number of sessions to keep in memory
        """
        self.sessions: Dict[str, ChatSession] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        self.max_sessions = max_sessions
    
    def create_session(self, **kwargs) -> str:
        """
        Create a new chat session.
        
        Args:
            **kwargs: Additional metadata for the session
            
        Returns:
            Session ID
        """
        # Clean up expired sessions
        self._cleanup_expired_sessions()
        
        # Check if we've reached the maximum number of sessions
        if len(self.sessions) >= self.max_sessions:
            self._remove_oldest_session()
        
        session_id = str(uuid.uuid4())
        session = ChatSession(
            session_id=session_id,
            created_at=datetime.now(),
            last_activity=datetime.now(),
            metadata=kwargs
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def get_session(self, session_id: str) -> Optional[ChatSession]:
        """
        Get a session by ID.
        
        Args:
            session_id: Session identifier
            
        Returns:
            ChatSession object or None if not found
        """
        session = self.sessions.get(session_id)
        if session and session.is_active():
            session.last_activity = datetime.now()
            return session
        elif session and not session.is_active():
            # Remove expired session
            del self.sessions[session_id]
        
        return None
    
    def add_user_message(self, session_id: str, content: str, language: str, **kwargs) -> bool:
        """
        Add a user message to a session.
        
        Args:
            session_id: Session identifier
            content: Message content
            language: Language code
            **kwargs: Additional metadata
            
        Returns:
            True if message was added, False otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.add_message('user', content, language, **kwargs)
        return True
    
    def add_assistant_message(self, session_id: str, content: str, language: str, **kwargs) -> bool:
        """
        Add an assistant message to a session.
        
        Args:
            session_id: Session identifier
            content: Message content
            language: Language code
            **kwargs: Additional metadata
            
        Returns:
            True if message was added, False otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.add_message('assistant', content, language, **kwargs)
        return True
    
    def add_message(self, session_id: str, user_content: str, assistant_content: str, **kwargs) -> bool:
        """
        Add both user and assistant messages to a session.
        This is a convenience method for adding a complete exchange.
        
        Args:
            session_id: Session identifier
            user_content: User message content
            assistant_content: Assistant message content
            **kwargs: Additional metadata (language will be inferred from user message)
            
        Returns:
            True if both messages were added, False otherwise
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        # Extract language from kwargs or use default
        language = kwargs.pop('language', 'en')
        
        # Add user message first
        user_success = self.add_user_message(session_id, user_content, language, **kwargs)
        if not user_success:
            return False
        
        # Add assistant message
        assistant_success = self.add_assistant_message(session_id, assistant_content, language, **kwargs)
        return assistant_success
    
    def get_session_history(self, session_id: str) -> List[ChatMessage]:
        """
        Get the complete message history for a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of all ChatMessage objects in the session
        """
        session = self.get_session(session_id)
        if not session:
            return []
        
        return session.messages
    
    def clear_session(self, session_id: str) -> bool:
        """
        Clear all messages from a session while keeping the session active.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session was cleared, False if not found
        """
        session = self.get_session(session_id)
        if not session:
            return False
        
        session.messages.clear()
        session.last_activity = datetime.now()
        return True
    
    def get_conversation_context(self, session_id: str, max_messages: int = 3) -> List[str]:
        """
        Get conversation context for a session.
        
        Args:
            session_id: Session identifier
            max_messages: Maximum number of messages to include
            
        Returns:
            List of message contents for context
        """
        session = self.get_session(session_id)
        if not session:
            return []
        
        return session.get_conversation_context(max_messages)
    
    def get_session_info(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            Session summary dictionary or None if not found
        """
        session = self.get_session(session_id)
        if not session:
            return None
        
        return session.get_session_summary()
    
    def end_session(self, session_id: str) -> bool:
        """
        End a session and remove it from memory.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session was ended, False if not found
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return True
        return False
    
    def list_active_sessions(self) -> List[Dict[str, Any]]:
        """
        Get a list of all active sessions.
        
        Returns:
            List of session summaries
        """
        self._cleanup_expired_sessions()
        return [session.get_session_summary() for session in self.sessions.values()]
    
    def _cleanup_expired_sessions(self):
        expired_sessions = [
            session_id for session_id, session in self.sessions.items()
            if not session.is_active()
        ]
        
        for session_id in expired_sessions:
            del self.sessions[session_id]
        
        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    def _remove_oldest_session(self):
        if not self.sessions:
            return
        
        oldest_session_id = min(
            self.sessions.keys(),
            key=lambda sid: self.sessions[sid].created_at
        )
        
        del self.sessions[oldest_session_id]
        logger.info(f"Removed oldest session {oldest_session_id} due to capacity limit")
    
    def get_session_stats(self) -> Dict[str, Any]:
        """
        Get statistics about all sessions.
        
        Returns:
            Dictionary with session statistics
        """
        self._cleanup_expired_sessions()
        
        total_messages = sum(len(session.messages) for session in self.sessions.values())
        languages_used = set()
        for session in self.sessions.values():
            languages_used.update(msg.language for msg in session.messages)
        
        return {
            'total_sessions': len(self.sessions),
            'total_messages': total_messages,
            'languages_used': list(languages_used),
            'avg_messages_per_session': total_messages / len(self.sessions) if self.sessions else 0
        }

# Global session manager instance
session_manager = SessionManager()

def get_session_manager() -> SessionManager:
    """
    Get the global session manager instance.
    
    Returns:
        Global SessionManager instance
    """
    return session_manager

def create_new_session(**kwargs) -> str:
    """
    Create a new chat session.
    
    Args:
        **kwargs: Additional metadata for the session
        
    Returns:
        Session ID
    """
    return session_manager.create_session(**kwargs)

def get_session_context(session_id: str, max_messages: int = 3) -> List[str]:
    """
    Get conversation context for a session.
    
    Args:
        session_id: Session identifier
        max_messages: Maximum number of messages to include
        
    Returns:
        List of message contents for context
    """
    return session_manager.get_conversation_context(session_id, max_messages)
