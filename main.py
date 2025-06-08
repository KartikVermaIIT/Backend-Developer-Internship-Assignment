import asyncio
import logging
import os
import time
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

from livekit.agents import JobContext, WorkerOptions, cli
from livekit.plugins import deepgram, openai, elevenlabs, cartesia
from livekit import rtc

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricsTracker:
    def __init__(self):
        self.session_start = None
        self.metrics = {
            'session_id': None,
            'start_time': None,
            'end_time': None,
            'total_duration': 0,
            'interruptions_count': 0,
            'stt_delays': [],
            'ttft_delays': [],
            'ttfd_delays': [],
            'total_latencies': [],
            'user_messages': 0,
            'agent_responses': 0,
            'errors': 0
        }

    def start_session(self, session_id: str):
        self.session_start = time.time()
        self.metrics['session_id'] = session_id
        self.metrics['start_time'] = datetime.now().isoformat()
        logger.info(f"Started tracking session: {session_id}")

    def record_stt_delay(self, delay: float):
        self.metrics['stt_delays'].append(delay)

    def record_ttft(self, delay: float):
        self.metrics['ttft_delays'].append(delay)

    def record_ttfd(self, delay: float):
        self.metrics['ttfd_delays'].append(delay)

    def record_total_latency(self, latency: float):
        self.metrics['total_latencies'].append(latency)
        logger.info(f"Total latency: {latency:.3f}s")

    def record_interruption(self):
        self.metrics['interruptions_count'] += 1
        logger.info("User interruption detected")

    def record_user_message(self):
        self.metrics['user_messages'] += 1

    def record_agent_response(self):
        self.metrics['agent_responses'] += 1

    def record_error(self):
        self.metrics['errors'] += 1

    def end_session(self):
        if self.session_start:
            self.metrics['end_time'] = datetime.now().isoformat()
            self.metrics['total_duration'] = time.time() - self.session_start
            logger.info(f"Session ended. Duration: {self.metrics['total_duration']:.2f}s")

    def save_to_excel(self, filename: str = "voice_agent_metrics.xlsx"):
        try:
            avg_stt = sum(self.metrics['stt_delays']) / len(self.metrics['stt_delays']) if self.metrics['stt_delays'] else 0
            avg_ttft = sum(self.metrics['ttft_delays']) / len(self.metrics['ttft_delays']) if self.metrics['ttft_delays'] else 0
            avg_ttfd = sum(self.metrics['ttfd_delays']) / len(self.metrics['ttfd_delays']) if self.metrics['ttfd_delays'] else 0
            avg_latency = sum(self.metrics['total_latencies']) / len(self.metrics['total_latencies']) if self.metrics['total_latencies'] else 0

            summary_data = {
                'Session ID': [self.metrics['session_id']],
                'Start Time': [self.metrics['start_time']],
                'End Time': [self.metrics['end_time']],
                'Total Duration (s)': [self.metrics['total_duration']],
                'User Messages': [self.metrics['user_messages']],
                'Agent Responses': [self.metrics['agent_responses']],
                'Interruptions': [self.metrics['interruptions_count']],
                'Average STT Delay (s)': [avg_stt],
                'Average TTFT (s)': [avg_ttft],
                'Average TTFD (s)': [avg_ttfd],
                'Average Total Latency (s)': [avg_latency],
                'Max Latency (s)': [max(self.metrics['total_latencies']) if self.metrics['total_latencies'] else 0],
                'Min Latency (s)': [min(self.metrics['total_latencies']) if self.metrics['total_latencies'] else 0],
                'Errors': [self.metrics['errors']],
                'Latency Target Met (<2s)': [avg_latency < 2.0]
            }
            df = pd.DataFrame(summary_data)
            if os.path.exists(filename):
                existing_df = pd.read_excel(filename)
                df = pd.concat([existing_df, df], ignore_index=True)
            df.to_excel(filename, index=False)
            logger.info(f"Metrics saved to {filename}")
        except Exception as e:
            logger.error(f"Failed to save metrics: {e}")

class VoiceAgent:
    def __init__(self):
        self.metrics_tracker = MetricsTracker()
        self.conversation_active = False

    async def entrypoint(self, ctx: JobContext):
        logger.info("Voice agent starting...")
        session_id = f"session_{int(time.time())}"
        self.metrics_tracker.start_session(session_id)

        try:
            # Create STT
            if os.getenv("DEEPGRAM_API_KEY"):
                stt = deepgram.STT(
                    api_key=os.getenv("DEEPGRAM_API_KEY"),
                    model="nova-2",
                    language="en",
                    interim_results=True,
                )
            else:
                stt = openai.STT()

            # Create LLM
            if os.getenv("GROQ_API_KEY"):
                llm_service = openai.LLM(
                    api_key=os.getenv("GROQ_API_KEY"),
                    base_url="https://api.groq.com/openai/v1",
                    model="llama3-8b-8192",
                )
            else:
                llm_service = openai.LLM(model="gpt-3.5-turbo")

            # Create TTS
            if os.getenv("ELEVENLABS_API_KEY"):
                tts = elevenlabs.TTS(
                    api_key=os.getenv("ELEVENLABS_API_KEY"),
                    voice_id="21m00Tcm4TlvDq8ikWAM",
                )
            elif os.getenv("CARTESIA_API_KEY"):
                tts = cartesia.TTS(
                    api_key=os.getenv("CARTESIA_API_KEY"),
                    voice_id="a0e99841-438c-4a64-b679-ae501e7d6091",
                )
            else:
                tts = openai.TTS()

            # Your room (livekit) handling here:
            # e.g., subscribe to audio track, receive audio stream, convert to text (STT)
            # send text to LLM, get response, synthesize with TTS, play back audio

            # Pseudo-code flow:
            async for audio_chunk in ctx.audio_stream():
                # STT
                start_stt = time.time()
                user_text = await stt.transcribe(audio_chunk)
                stt_delay = time.time() - start_stt
                self.metrics_tracker.record_stt_delay(stt_delay)
                self.metrics_tracker.record_user_message()
                logger.info(f"User said: {user_text}")

                # LLM
                start_llm = time.time()
                response_text = await llm_service.chat(user_text)
                ttft = time.time() - start_llm
                self.metrics_tracker.record_ttft(ttft)
                logger.info(f"Agent response: {response_text}")

                # TTS
                start_tts = time.time()
                audio_response = await tts.synthesize(response_text)
                ttfd = time.time() - start_llm
                self.metrics_tracker.record_ttfd(ttfd)

                self.metrics_tracker.record_agent_response()

                # Send audio_response back via ctx to the user (depends on your livekit APIs)
                await ctx.send_audio(audio_response)

            # End session when done
        except Exception as e:
            logger.error(f"Error in voice agent: {e}")
            self.metrics_tracker.record_error()
        finally:
            self.metrics_tracker.end_session()
            self.metrics_tracker.save_to_excel()

def main():
    voice_agent = VoiceAgent()
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=voice_agent.entrypoint,
        )
    )

if __name__ == "__main__":
    main()
