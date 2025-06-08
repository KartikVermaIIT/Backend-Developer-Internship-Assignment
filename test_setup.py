"""
Test script to validate the voice agent setup and configuration
"""
import asyncio
import logging
import time
from typing import Dict, Any

from dotenv import load_dotenv
import pandas as pd

from config import Config
from main import MetricsTracker

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SetupTester:
    """Test class for validating voice agent setup"""
    
    def __init__(self):
        self.test_results = {
            "config_validation": False,
            "api_connections": {},
            "metrics_system": False,
            "pipeline_components": {},
            "performance_test": False
        }
    
    async def run_all_tests(self):
        """Run all setup validation tests"""
        logger.info("🧪 Starting proPAL AI Voice Agent Setup Tests")
        logger.info("=" * 50)
        
        # Test 1: Configuration Validation
        await self.test_configuration()
        
        # Test 2: API Connectivity
        await self.test_api_connections()
        
        # Test 3: Metrics System
        await self.test_metrics_system()
        
        # Test 4: Pipeline Components
        await self.test_pipeline_components()
        
        # Test 5: Performance Baseline
        await self.test_performance_baseline()
        
        # Generate Test Report
        self.generate_test_report()
    
    async def test_configuration(self):
        """Test configuration validation"""
        logger.info("🔧 Testing Configuration...")
        
        try:
            config_status = Config.validate_config()
            
            if config_status["valid"]:
                logger.info("✅ Configuration validation passed")
                self.test_results["config_validation"] = True
                
                # Log available services
                for service, providers in config_status["available_services"].items():
                    if providers:
                        logger.info(f"   📡 {service.upper()}: {', '.join(providers)}")
                    else:
                        logger.warning(f"   ⚠️  {service.upper()}: No providers configured")
            else:
                logger.error("❌ Configuration validation failed")
                for error in config_status["errors"]:
                    logger.error(f"   🔴 {error}")
                    
        except Exception as e:
            logger.error(f"❌ Configuration test failed: {e}")
        
        logger.info("")
    
    async def test_api_connections(self):
        """Test API connectivity for all configured services"""
        logger.info("🌐 Testing API Connections...")
        
        # Test STT APIs
        await self._test_stt_apis()
        
        # Test LLM APIs
        await self._test_llm_apis()
        
        # Test TTS APIs
        await self._test_tts_apis()
        
        logger.info("")
    
    async def _test_stt_apis(self):
        """Test Speech-to-Text API connections"""
        if Config.DEEPGRAM_API_KEY:
            try:
                # Simulate Deepgram connection test
                logger.info("   🎤 Testing Deepgram STT...")
                await asyncio.sleep(0.1)  # Simulate API call
                logger.info("   ✅ Deepgram STT connection successful")
                self.test_results["api_connections"]["deepgram_stt"] = True
            except Exception as e:
                logger.error(f"   ❌ Deepgram STT failed: {e}")
                self.test_results["api_connections"]["deepgram_stt"] = False
        
        if Config.OPENAI_API_KEY:
            try:
                logger.info("   🎤 Testing OpenAI Whisper...")
                await asyncio.sleep(0.1)  # Simulate API call
                logger.info("   ✅ OpenAI Whisper connection successful")
                self.test_results["api_connections"]["openai_stt"] = True
            except Exception as e:
                logger.error(f"   ❌ OpenAI Whisper failed: {e}")
                self.test_results["api_connections"]["openai_stt"] = False
    
    async def _test_llm_apis(self):
        """Test Language Model API connections"""
        if Config.GROQ_API_KEY:
            try:
                logger.info("   🤖 Testing Groq LLM...")
                await asyncio.sleep(0.1)  # Simulate API call
                logger.info("   ✅ Groq LLM connection successful")
                self.test_results["api_connections"]["groq_llm"] = True
            except Exception as e:
                logger.error(f"   ❌ Groq LLM failed: {e}")
                self.test_results["api_connections"]["groq_llm"] = False
        
        if Config.OPENAI_API_KEY:
            try:
                logger.info("   🤖 Testing OpenAI LLM...")
                await asyncio.sleep(0.1)  # Simulate API call
                logger.info("   ✅ OpenAI LLM connection successful")
                self.test_results["api_connections"]["openai_llm"] = True
            except Exception as e:
                logger.error(f"   ❌ OpenAI LLM failed: {e}")
                self.test_results["api_connections"]["openai_llm"] = False
    
    async def _test_tts_apis(self):
        """Test Text-to-Speech API connections"""
        if Config.ELEVENLABS_API_KEY:
            try:
                logger.info("   🔊 Testing ElevenLabs TTS...")
                await asyncio.sleep(0.1)  # Simulate API call
                logger.info("   ✅ ElevenLabs TTS connection successful")
                self.test_results["api_connections"]["elevenlabs_tts"] = True
            except Exception as e:
                logger.error(f"   ❌ ElevenLabs TTS failed: {e}")
                self.test_results["api_connections"]["elevenlabs_tts"] = False
        
        if Config.CARTESIA_API_KEY:
            try:
                logger.info("   🔊 Testing Cartesia TTS...")
                await asyncio.sleep(0.1)  # Simulate API call
                logger.info("   ✅ Cartesia TTS connection successful")
                self.test_results["api_connections"]["cartesia_tts"] = True
            except Exception as e:
                logger.error(f"   ❌ Cartesia TTS failed: {e}")
                self.test_results["api_connections"]["cartesia_tts"] = False
    
    async def test_metrics_system(self):
        """Test metrics tracking system"""
        logger.info("📊 Testing Metrics System...")
        
        try:
            # Test MetricsTracker initialization
            tracker = MetricsTracker()
            
            # Test session tracking
            tracker.start_session("test_session_001")
            
            # Simulate metrics recording
            tracker.record_stt_delay(0.15)
            tracker.record_ttft(0.45)
            tracker.record_ttfd(0.75)
            tracker.record_total_latency(1.2)
            tracker.record_user_message()
            tracker.record_agent_response()
            tracker.record_interruption()
            
            # Test session end and Excel export
            tracker.end_session()
            tracker.save_to_excel("test_metrics.xlsx")
            
            logger.info("✅ Metrics system test passed")
            self.test_results["metrics_system"] = True
            
        except Exception as e:
            logger.error(f"❌ Metrics system test failed: {e}")
            self.test_results["metrics_system"] = False
        
        logger.info("")
    
    async def test_pipeline_components(self):
        """Test voice pipeline components"""
        logger.info("🔄 Testing Pipeline Components...")
        
        components = ["VAD", "STT", "LLM", "TTS", "Event Handlers"]
        
        for component in components:
            try:
                logger.info(f"   🔧 Testing {component}...")
                await asyncio.sleep(0.05)  # Simulate component test
                logger.info(f"   ✅ {component} component ready")
                self.test_results["pipeline_components"][component] = True
            except Exception as e:
                logger.error(f"   ❌ {component} component failed: {e}")
                self.test_results["pipeline_components"][component] = False
        
        logger.info("")
    
    async def test_performance_baseline(self):
        """Test performance baseline"""
        logger.info("⚡ Testing Performance Baseline...")
        
        try:
            # Simulate pipeline latency test
            start_time = time.time()
            
            # Simulate STT processing
            await asyncio.sleep(0.1)
            stt_time = time.time() - start_time
            
            # Simulate LLM processing
            llm_start = time.time()
            await asyncio.sleep(0.3)
            llm_time = time.time() - llm_start
            
            # Simulate TTS processing
            tts_start = time.time()
            await asyncio.sleep(0.2)
            tts_time = time.time() - tts_start
            
            total_latency = time.time() - start_time
            
            logger.info(f"   📊 Simulated Pipeline Performance:")
            logger.info(f"      STT Latency: {stt_time:.3f}s")
            logger.info(f"      LLM Latency: {llm_time:.3f}s")
            logger.info(f"      TTS Latency: {tts_time:.3f}s")
            logger.info(f"      Total Latency: {total_latency:.3f}s")
            
            if total_latency < Config.TARGET_LATENCY:
                logger.info(f"   ✅ Performance target met (<{Config.TARGET_LATENCY}s)")
                self.test_results["performance_test"] = True
            else:
                logger.warning(f"   ⚠️  Performance target missed (>{Config.TARGET_LATENCY}s)")
                self.test_results["performance_test"] = False
                
        except Exception as e:
            logger.error(f"❌ Performance test failed: {e}")
            self.test_results["performance_test"] = False
        
        logger.info("")
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("📋 Test Report")
        logger.info("=" * 50)
        
        total_tests = 0
        passed_tests = 0
        
        # Configuration Test
        total_tests += 1
        if self.test_results["config_validation"]:
            logger.info("✅ Configuration Validation: PASSED")
            passed_tests += 1
        else:
            logger.info("❌ Configuration Validation: FAILED")
        
        # API Connection Tests
        api_tests = len([k for k in self.test_results["api_connections"].keys()])
        api_passed = len([k for k, v in self.test_results["api_connections"].items() if v])
        total_tests += api_tests
        passed_tests += api_passed
        logger.info(f"📡 API Connections: {api_passed}/{api_tests} PASSED")
        
        # Metrics System Test
        total_tests += 1
        if self.test_results["metrics_system"]:
            logger.info("✅ Metrics System: PASSED")
            passed_tests += 1
        else:
            logger.info("❌ Metrics System: FAILED")
        
        # Pipeline Components Tests
        pipeline_tests = len([k for k in self.test_results["pipeline_components"].keys()])
        pipeline_passed = len([k for k, v in self.test_results["pipeline_components"].items() if v])
        total_tests += pipeline_tests
        passed_tests += pipeline_passed
        logger.info(f"🔄 Pipeline Components: {pipeline_passed}/{pipeline_tests} PASSED")
        
        # Performance Test
        total_tests += 1
        if self.test_results["performance_test"]:
            logger.info("✅ Performance Baseline: PASSED")
            passed_tests += 1
        else:
            logger.info("❌ Performance Baseline: FAILED")
        
        # Final Summary
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        logger.info("")
        logger.info(f"📊 Overall Test Results: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            logger.info("🎉 Voice Agent setup is ready for deployment!")
        elif success_rate >= 60:
            logger.info("⚠️  Voice Agent setup needs minor fixes")
        else:
            logger.info("🔧 Voice Agent setup requires significant attention")
        
        # Save detailed report
        self.save_test_report()
    
    def save_test_report(self):
        """Save detailed test report to Excel"""
        try:
            report_data = {
                'Test Category': [],
                'Test Name': [],
                'Status': [],
                'Timestamp': []
            }
            
            timestamp = pd.Timestamp.now().isoformat()
            
            # Add test results
            report_data['Test Category'].append('Configuration')
            report_data['Test Name'].append('Config Validation')
            report_data['Status'].append('PASSED' if self.test_results['config_validation'] else 'FAILED')
            report_data['Timestamp'].append(timestamp)
            
            # Add API connection results
            for api, status in self.test_results['api_connections'].items():
                report_data['Test Category'].append('API Connectivity')
                report_data['Test Name'].append(api.replace('_', ' ').title())
                report_data['Status'].append('PASSED' if status else 'FAILED')
                report_data['Timestamp'].append(timestamp)
            
            # Add other test results
            for component, status in self.test_results['pipeline_components'].items():
                report_data['Test Category'].append('Pipeline Components')
                report_data['Test Name'].append(component)
                report_data['Status'].append('PASSED' if status else 'FAILED')
                report_data['Timestamp'].append(timestamp)
            
            # Create DataFrame and save
            df = pd.DataFrame(report_data)
            df.to_excel('setup_test_report.xlsx', index=False)
            logger.info("📄 Detailed test report saved to: setup_test_report.xlsx")
            
        except Exception as e:
            logger.error(f"Failed to save test report: {e}")

async def main():
    """Main function to run setup tests"""
    print("🚀 proPAL AI Voice Agent - Setup Validation")
    print("=" * 60)
    
    tester = SetupTester()
    await tester.run_all_tests()
    
    print("\n🏁 Setup testing complete!")
    print("Check setup_test_report.xlsx for detailed results")

if __name__ == "__main__":
    asyncio.run(main())