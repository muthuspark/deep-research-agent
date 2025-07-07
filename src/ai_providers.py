import os
import tiktoken
import json
from openai import OpenAI
from typing import Optional, Dict, Any
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    genai = None

class AIProvider:
    def __init__(self):
        self.openai_client = None
        self.gemini_model = None
        self.encoder = tiktoken.get_encoding("o200k_base")
        
        # Initialize OpenAI client
        if os.getenv("OPENAI_KEY"):
            self.openai_client = OpenAI(
                api_key=os.getenv("OPENAI_KEY"),
                base_url=os.getenv("OPENAI_ENDPOINT", "https://api.openai.com/v1")
            )
        
        # Initialize Gemini client
        if GEMINI_AVAILABLE and os.getenv("GEMINI_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_KEY"))
            self.gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    
    def get_provider(self) -> str:
        """Determine which AI provider to use"""
        # Check for explicit provider preference
        provider = os.getenv("AI_PROVIDER", "").lower()
        
        if provider == "gemini" and self.gemini_model:
            return "gemini"
        elif provider == "openai" and self.openai_client:
            return "openai"
        
        # Auto-detect based on available clients
        if self.gemini_model:
            return "gemini"
        elif self.openai_client:
            return "openai"
        
        raise ValueError("No AI provider available. Please set OPENAI_KEY or GEMINI_KEY environment variable.")
    
    def get_model(self) -> str:
        """Get the preferred model to use"""
        custom_model = os.getenv("CUSTOM_MODEL")
        if custom_model:
            return custom_model
        
        provider = self.get_provider()
        if provider == "gemini":
            return "gemini-1.5-flash"
        else:
            return "gpt-4o-mini"  # Default OpenAI model
    
    def trim_prompt(self, prompt: str, context_size: int = 128000) -> str:
        """Trim prompt to fit within context size"""
        if not prompt:
            return ""
        
        tokens = self.encoder.encode(prompt)
        if len(tokens) <= context_size:
            return prompt
        
        # Simple truncation - take first part of prompt
        overflow_tokens = len(tokens) - context_size
        # Rough estimate: 3 characters per token
        target_length = len(prompt) - (overflow_tokens * 3)
        
        if target_length < 140:  # Minimum chunk size
            return prompt[:140]
        
        return prompt[:target_length]
    
    def generate_object(self, system: str, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured output using the available AI provider"""
        provider = self.get_provider()
        
        if provider == "gemini":
            return self._generate_object_gemini(system, prompt, schema)
        else:
            return self._generate_object_openai(system, prompt, schema)
    
    def _generate_object_openai(self, system: str, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured output using OpenAI"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized. Please set OPENAI_KEY environment variable.")
        
        # Convert simple schema to OpenAI function format
        function_schema = {
            "name": "generate_response",
            "description": "Generate structured response",
            "parameters": {
                "type": "object",
                "properties": schema,
                "required": list(schema.keys())
            }
        }
        
        response = self.openai_client.chat.completions.create(
            model=self.get_model(),
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            functions=[function_schema],
            function_call={"name": "generate_response"},
            temperature=0.7
        )
        
        function_call = response.choices[0].message.function_call
        if function_call:
            return json.loads(function_call.arguments)
        
        return {}
    
    def _generate_object_gemini(self, system: str, prompt: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured output using Gemini"""
        if not self.gemini_model:
            raise ValueError("Gemini model not initialized. Please set GEMINI_KEY environment variable.")
        
        # Create a schema description for Gemini
        schema_description = self._describe_schema(schema)
        
        # Combine system and user prompts with schema instructions
        full_prompt = f"""System: {system}

You must respond with a valid JSON object that matches this exact schema:
{schema_description}

User: {prompt}

Please respond with ONLY the JSON object, no additional text or formatting."""
        
        try:
            response = self.gemini_model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    candidate_count=1,
                )
            )
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove any markdown formatting if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            response_text = response_text.strip()
            
            # Parse JSON
            return json.loads(response_text)
            
        except Exception as e:
            print(f"Error generating with Gemini: {e}")
            return {}
    
    def _describe_schema(self, schema: Dict[str, Any]) -> str:
        """Convert schema to human-readable description for Gemini"""
        def describe_property(prop_name: str, prop_def: Dict[str, Any]) -> str:
            if prop_def.get("type") == "array":
                if "items" in prop_def:
                    items_type = prop_def["items"].get("type", "object")
                    if items_type == "object" and "properties" in prop_def["items"]:
                        # Complex object array
                        object_props = []
                        for item_prop_name, item_prop_def in prop_def["items"]["properties"].items():
                            object_props.append(f'"{item_prop_name}": {describe_property(item_prop_name, item_prop_def)}')
                        return f'[{{{", ".join(object_props)}}}]'
                    else:
                        # Simple array
                        return f'["{items_type}"]'
                else:
                    return f'array'
            elif prop_def.get("type") == "string":
                return f'string'
            elif prop_def.get("type") == "number":
                return f'number'
            elif prop_def.get("type") == "boolean":
                return f'boolean'
            else:
                return f'object'
        
        props = []
        for prop_name, prop_def in schema.items():
            props.append(f'"{prop_name}": {describe_property(prop_name, prop_def)}')
        
        return f'{{{", ".join(props)}}}'

# Global instance
ai_provider = AIProvider()