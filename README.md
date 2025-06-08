# proPAL AI Voice Agent - Backend Engineering Internship

## 🎯 Project Overview

This is a complete AI voice agent implementation using LiveKit for proPAL AI's backend engineering internship. The agent provides real-time voice conversation capabilities with comprehensive metrics tracking and latency optimization.

## 🚀 Features

### Core Pipeline
- **Speech-to-Text (STT)**: Deepgram (free tier) or OpenAI Whisper
- **Language Model (LLM)**: Groq API for fast inference or OpenAI GPT-3.5
- **Text-to-Speech (TTS)**: ElevenLabs or Cartesia
- **Voice Activity Detection (VAD)**: Real-time speech detection
- **Interruption Handling**: Graceful handling of user interruptions

### Metrics Tracking
- **EOU Delay**: End-of-utterance processing delay
- **TTFT**: Time to First Token from LLM
- **TTFD**: Time to Final Decision
- **Total Latency**: End-to-end conversation latency
- **Interruption Count**: Number of user interruptions
- **Session Statistics**: Messages, errors, duration

### Performance Optimization
- Target latency: < 2 seconds
- Optimized model selection (Groq's Llama3-8B for speed)
- Efficient event handling and async processing
- Real-time metrics monitoring

## 📋 Prerequisites

- Python 3.8+
- LiveKit Server (local or cloud)
- API keys for chosen services

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/KartikVermaIIT/Backend-Developer-Internship-Assignment
   cd propal-voice-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

## 🔧 Configuration

### Required API Keys

1. **LiveKit**: 
   - Sign up at [LiveKit Cloud](https://cloud.livekit.io/)
   - Or run locally: `livekit-server --dev`

2. **Speech-to-Text** (choose one):
   - **Deepgram**: Free tier available at [Deepgram](https://deepgram.com/)
   - **OpenAI**: For Whisper API

3. **Language Model** (choose one):
   - **Groq**: Free tier at [Groq](https://groq.com/) (Recommended for speed)
   - **OpenAI**: GPT-3.5 Turbo

4. **Text-to-Speech** (choose one):
   - **ElevenLabs**: Free trial at [ElevenLabs](https://elevenlabs.io/)
   - **Cartesia**: Free trial at [Cartesia](https://cartesia.ai/)

### Environment Variables

```bash
# LiveKit
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret

# Services
DEEPGRAM_API_KEY=your_deepgram_key
GROQ_API_KEY=your_groq_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

## 🚀 Running the Agent

1. **Start LiveKit server** (if running locally):
   ```bash
   livekit-server --dev
   ```

2. **Run the voice agent**:
   ```bash
   python main.py start
   ```

3. **Test the agent**:
   - Open [LiveKit Agent Playground](https://agents-playground.livekit.io/)
   - Connect to your LiveKit server
   - Start a conversation

## 📊 Metrics and Monitoring

The agent automatically tracks and logs comprehensive metrics:

### Tracked Metrics
- **Session Duration**: Total conversation time
- **STT Delays**: Speech-to-text processing times
- **TTFT**: Time to first token from LLM
- **TTFD**: Time to final decision
- **Total Latency**: End-to-end response time
- **Interruption Count**: User interruptions handled
- **Message Counts**: User messages vs agent responses
- **Error Count**: System errors encountered

### Excel Export
Metrics are automatically saved to `voice_agent_metrics.xlsx` with:
- Session summaries
- Performance averages
- Latency analysis
- Target achievement tracking

## 🏗️ Architecture

### Pipeline Flow
```
User Speech → VAD → STT → LLM → TTS → Audio Output
     ↓         ↓     ↓     ↓     ↓
   Metrics Tracking Throughout Pipeline
```

### Key Components
- **VoiceAgent**: Main orchestrator
- **MetricsTracker**: Performance monitoring
- **Event Handlers**: Real-time event processing
- **Service Factories**: Modular service creation

## 🎯 Performance Optimization

### Latency Reduction Strategies
1. **Fast LLM**: Groq's Llama3-8B (< 1s inference)
2. **Streaming STT**: Real-time transcription
3. **Efficient TTS**: Optimized voice synthesis
4. **Async Processing**: Non-blocking operations
5. **Smart Caching**: Reduced redundant API calls

### Monitoring
- Real-time latency tracking
- Automatic Excel reporting
- Performance threshold alerts
- Bottleneck identification

## 🔧 Troubleshooting

### Common Issues
1. **High Latency**:
   - Check API response times
   - Verify network connectivity
   - Consider switching to faster models

2. **Connection Issues**:
   - Verify LiveKit server status
   - Check API key validity
   - Ensure proper environment setup

3. **Audio Quality**:
   - Adjust VAD sensitivity
   - Check microphone permissions
   - Verify TTS settings

## 📈 Usage Statistics

The agent tracks:
- Conversation quality metrics
- System performance data
- User interaction patterns
- Error rates and types

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

This project is created for proPAL AI's backend engineering internship evaluation.


---

**Built with ❤️ for proPAL AI's mission to revolutionize SMB customer interactions in India**
