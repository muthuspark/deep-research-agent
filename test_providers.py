#!/usr/bin/env python3
"""
Test script to verify AI provider setup and functionality.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from src.ai_providers import ai_provider

# Load environment variables
load_dotenv()

def test_provider_setup():
    """Test if AI provider is properly configured"""
    print("Testing AI Provider Setup...")
    print("-" * 40)
    
    try:
        provider = ai_provider.get_provider()
        model = ai_provider.get_model()
        
        print(f"✓ Provider: {provider.upper()}")
        print(f"✓ Model: {model}")
        
        # Test structured output generation
        print("\nTesting structured output generation...")
        
        schema = {
            "test_response": {
                "type": "string",
                "description": "A simple test response"
            },
            "provider_used": {
                "type": "string", 
                "description": "Which AI provider was used"
            }
        }
        
        result = ai_provider.generate_object(
            system="You are a helpful assistant that provides test responses.",
            prompt="Generate a test response confirming the AI provider is working correctly.",
            schema=schema
        )
        
        if result:
            print("✓ Structured output generation successful!")
            print(f"  Response: {result.get('test_response', 'No response')}")
            print(f"  Provider reported: {result.get('provider_used', 'Unknown')}")
        else:
            print("✗ Structured output generation failed!")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    
    return True

def check_environment():
    """Check environment variables"""
    print("\nChecking Environment Variables...")
    print("-" * 40)
    
    # Check required variables
    firecrawl_key = os.getenv("FIRECRAWL_KEY")
    print(f"FIRECRAWL_KEY: {'✓ Set' if firecrawl_key else '✗ Not set'}")
    
    # Check AI provider keys
    openai_key = os.getenv("OPENAI_KEY")
    gemini_key = os.getenv("GEMINI_KEY")
    
    print(f"OPENAI_KEY: {'✓ Set' if openai_key else '✗ Not set'}")
    print(f"GEMINI_KEY: {'✓ Set' if gemini_key else '✗ Not set'}")
    
    if not (openai_key or gemini_key):
        print("\n⚠️  Warning: No AI provider keys found!")
        print("   Please set either OPENAI_KEY or GEMINI_KEY in your .env file")
        return False
    
    # Check optional variables
    ai_provider_pref = os.getenv("AI_PROVIDER", "auto-detect")
    print(f"AI_PROVIDER: {ai_provider_pref}")
    
    custom_model = os.getenv("CUSTOM_MODEL")
    if custom_model:
        print(f"CUSTOM_MODEL: {custom_model}")
    
    return True

def main():
    """Run all tests"""
    print("Deep Research AI Provider Test")
    print("=" * 40)
    
    # Check environment
    env_ok = check_environment()
    
    if not env_ok:
        print("\n❌ Environment check failed!")
        return 1
    
    # Test provider setup
    provider_ok = test_provider_setup()
    
    if provider_ok:
        print("\n✅ All tests passed! Your AI provider is ready for research.")
        return 0
    else:
        print("\n❌ Provider test failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 