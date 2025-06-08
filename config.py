"""
Configuration settings for the proPAL AI Voice Agent
"""
import os
from typing import Dict, Any

class Config:
    """Configuration class for voice agent settings"""
    
    # LiveKit Configuration
    LIVEKIT_URL = os.getenv("LIVEKIT_URL", "ws://localhost:7880")

    LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
    LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
    
    # API Keys
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY")
    
    # Performance Settings
    TARGET_LATENCY = float(os.getenv("TARGET_LATENCY", "2.0"))  # seconds
    MAX_CONVERSATION_DURATION = int(os.getenv("MAX_CONVERSATION_DURATION", "1800"))  # 30 minutes
    
    # Audio Settings
    SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))
    CHANNELS = int(os.getenv("CHANNELS", "1"))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    METRICS_FILE = os.getenv("METRICS_FILE", "voice_agent_metrics.xlsx")
    
    # Model Configuration
    STT_MODELS = {
        "deepgram": {
            "model": "nova-2",
            "language": "en",
            "interim_results": True
        },
        "openai": {
            "model": "whisper-1"
        }
    }
    
    LLM_MODELS = {
        "groq": {
            "model": "llama3-8b-8192",
            "max_tokens": 150,
            "temperature": 0.7,
            "base_url": "https://api.groq.com/openai/v1"
        },
        "openai": {
            "model": "gpt-3.5-turbo",
            "max_tokens": 150,
            "temperature": 0.7
        }
    }
    
    TTS_MODELS = {
        "elevenlabs": {
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Default voice
            "model_id": "eleven_monolingual_v1"
        },
        "cartesia": {
            "voice_id": "a0e99841-438c-4a64-b679-ae501e7d6091",
            "model_id": "sonic-english"
        },
        "openai": {
            "voice": "alloy",
            "model": "tts-1"
        }
    }
    
    # System Prompts
    SYSTEM_PROMPT = """You are a helpful AI voice assistant for proPAL AI, designed to help small and medium businesses in India. 

Key Guidelines:
- Keep responses concise and conversational (2-3 sentences max)
- Be helpful and professional
- Handle business inquiries naturally
- Support customer service scenarios
- Gracefully handle interruptions
- Speak in a friendly, approachable tone
- Focus on practical solutions

You can help with:
- Customer support queries
- Business information
- General assistance
- Product inquiries

Remember to be efficient and keep latency low while maintaining quality."""

    @classmethod
    def get_service_priority(cls) -> Dict[str, list]:
        """Get service priority order based on available API keys"""
        priorities = {
            "stt": [],
            "llm": [],
            "tts": []
        }
        
        # STT Priority (based on performance and availability)
        if cls.DEEPGRAM_API_KEY:
            priorities["stt"].append("deepgram")
        if cls.OPENAI_API_KEY:
            priorities["stt"].append("openai")
        
        # LLM Priority (Groq for speed, OpenAI as fallback)
        if cls.GROQ_API_KEY:
            priorities["llm"].append("groq")
        if cls.OPENAI_API_KEY:
            priorities["llm"].append("openai")
        
        # TTS Priority
        if cls.ELEVENLABS_API_KEY:
            priorities["tts"].append("elevenlabs")
        if cls.CARTESIA_API_KEY:
            priorities["tts"].append("cartesia")
        if cls.OPENAI_API_KEY:
            priorities["tts"].append("openai")
        
        return priorities
    
    @classmethod
    def validate_config(cls) -> Dict[str, Any]:
        """Validate configuration and return status"""
        status = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "available_services": {}
        }
        
        # Check required LiveKit config
        if not cls.LIVEKIT_API_KEY or not cls.LIVEKIT_API_SECRET:
            status["errors"].append("LiveKit API key and secret are required")
            status["valid"] = False
        
        # Check service availability
        priorities = cls.get_service_priority()
        
        for service_type, providers in priorities.items():
            status["available_services"][service_type] = providers
            if not providers:
                status["errors"].append(f"No {service_type.upper()} service configured")
                status["valid"] = False
        
        # Performance warnings
        if cls.TARGET_LATENCY > 3.0:
            status["warnings"].append("Target latency > 3s may impact user experience")
        
        return status

# Validate configuration on import
config_status = Config.validate_config()
if not config_status["valid"]:
    print("⚠️  Configuration Issues Found:")
    for error in config_status["errors"]:
        print(f"   ❌ {error}")

if config_status["warnings"]:
    print("⚠️  Configuration Warnings:")
    for warning in config_status["warnings"]:
        print(f"   ⚠️  {warning}")

if config_status["valid"]:
    print("✅ Configuration validated successfully")
    print("📊 Available services:")
    for service, providers in config_status["available_services"].items():
        print(f"   {service.upper()}: {', '.join(providers) if providers else 'None'}")