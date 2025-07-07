#!/usr/bin/env python3

import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from dotenv import load_dotenv
from src.deep_research import deep_research, write_final_report, write_final_answer
from src.feedback import generate_feedback
from src.ai_providers import ai_provider

# Load environment variables
load_dotenv()

async def main():
    """Main research function"""
    
    # Check if topic is provided as command line argument
    if len(sys.argv) > 1:
        topic = " ".join(sys.argv[1:])
    else:
        topic = input("What would you like to research? ")
    
    if not topic.strip():
        print("Please provide a research topic.")
        return
    
    # Check if AI provider is available
    try:
        provider = ai_provider.get_provider()
        model = ai_provider.get_model()
        print(f"Using {provider.upper()} with model: {model}")
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("\n💡 Quick Setup:")
        print("1. Edit the .env file in this directory")
        print("2. Add your API key:")
        print("   - For OpenAI: OPENAI_KEY=your_key_here")
        print("   - For Gemini: GEMINI_KEY=your_key_here")
        print("3. Run the test: python test_providers.py")
        print("4. Then try again!")
        return
    
    # Get research parameters
    try:
        breadth_input = input("Enter research breadth (recommended 2-10, default 4): ").strip()
        breadth = int(breadth_input) if breadth_input else 4
    except ValueError:
        breadth = 4
    
    try:
        depth_input = input("Enter research depth (recommended 1-5, default 2): ").strip()
        depth = int(depth_input) if depth_input else 2
    except ValueError:
        depth = 2
    
    report_type = input("Generate report or answer? (report/answer, default report): ").strip().lower()
    is_report = report_type != "answer"
    
    combined_query = topic
    
    if is_report:
        print("Creating research plan...")
        
        # Generate follow-up questions
        try:
            follow_up_questions = await generate_feedback(topic)
            
            if follow_up_questions:
                print("\nTo better understand your research needs, please answer these follow-up questions:")
                
                answers = []
                for question in follow_up_questions:
                    answer = input(f"\n{question}\nYour answer: ")
                    answers.append(answer)
                
                # Combine all information
                qa_pairs = [f"Q: {q}\nA: {a}" for q, a in zip(follow_up_questions, answers)]
                combined_query = f"""
Initial Query: {topic}
Follow-up Questions and Answers:
{chr(10).join(qa_pairs)}
"""
        except Exception as e:
            print(f"Error generating follow-up questions: {e}")
            print("Continuing with original query...")
    
    print("\nStarting research...\n")
    
    try:
        # Perform deep research
        result = await deep_research(
            query=combined_query,
            breadth=breadth,
            depth=depth
        )
        
        print(f"\n\nLearnings:\n\n{chr(10).join(result.learnings)}")
        print(f"\n\nVisited URLs ({len(result.visited_urls)}):\n\n{chr(10).join(result.visited_urls)}")
        print("Writing final report...")
        
        # Create reports directory if it doesn't exist
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        # Generate timestamp for filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if is_report:
            # Generate and save report
            report = await write_final_report(
                prompt=combined_query,
                learnings=result.learnings,
                visited_urls=result.visited_urls
            )
            
            # Create filename with timestamp
            report_filename = reports_dir / f"report_{timestamp}.md"
            
            with open(report_filename, "w", encoding="utf-8") as f:
                f.write(report)
            
            print(f"\n\nFinal Report:\n\n{report}")
            print(f"\nReport has been saved to {report_filename}")
        else:
            # Generate and save answer
            answer = await write_final_answer(
                prompt=combined_query,
                learnings=result.learnings
            )
            
            # Create filename with timestamp
            answer_filename = reports_dir / f"answer_{timestamp}.md"
            
            with open(answer_filename, "w", encoding="utf-8") as f:
                f.write(answer)
            
            print(f"\n\nFinal Answer:\n\n{answer}")
            print(f"\nAnswer has been saved to {answer_filename}")
    
    except Exception as e:
        print(f"An error occurred during research: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nResearch interrupted by user.")
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()