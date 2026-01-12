"""LLM Vision Analysis Module for WebSpector.

This module uses local vision LLMs (LLaVA 1.6) via Ollama to analyze screenshots
and generate detailed QA reports.
"""

import base64
import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import ollama
except ImportError:
    ollama = None
    print("WARNING: ollama-python not installed. Run: pip install ollama")

import config


class LocalVisionLLM:
    """Local vision LLM analyzer using Ollama (LLaVA 1.6)."""
    
    def __init__(
        self,
        vision_model: Optional[str] = None,
        text_model: Optional[str] = None,
        temperature: float = 0.2,
        timeout: int = 30
    ):
        """Initialize LLM vision analyzer.
        
        Args:
            vision_model: Vision model name (e.g., 'llava:13b'). Defaults to config.
            text_model: Text model for report generation. Defaults to config.
            temperature: LLM temperature (0-1). Lower = more consistent.
            timeout: Request timeout in seconds.
        """
        if ollama is None:
            raise ImportError(
                "ollama-python is required. Install it with: pip install ollama\n"
                "Then install a vision model with: ollama pull llava:13b"
            )
        
        models = config.get_current_models()
        self.vision_model = vision_model or models["vision"]
        self.text_model = text_model or models["text"]
        self.temperature = temperature
        self.timeout = timeout
        
        print(f"Initialized LocalVisionLLM:")
        print(f"  Vision Model: {self.vision_model}")
        print(f"  Text Model: {self.text_model}")
        
        # Verify models are available
        self._check_models()
    
    def _check_models(self):
        """Check if required models are installed."""
        try:
            available_models = ollama.list()
            model_names = [m['name'] for m in available_models.get('models', [])]
            
            if not any(self.vision_model in m for m in model_names):
                print(f"\nWARNING: Vision model '{self.vision_model}' not found!")
                print(f"Install it with: ollama pull {self.vision_model}")
                print(f"Available models: {', '.join(model_names)}\n")
        except Exception as e:
            print(f"Could not check available models: {e}")
    
    def analyze_screenshot(
        self,
        screenshot_path: Path,
        action_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Analyze a single screenshot with optional action context.
        
        Args:
            screenshot_path: Path to screenshot image
            action_context: Optional dict with action details (type, target, etc)
        
        Returns:
            Dict with analysis results:
            {
                'summary': str,
                'findings': List[str],
                'status': 'PASS' | 'FAIL' | 'WARNING',
                'issues': List[Dict],
                'raw_response': str
            }
        """
        context_str = ""
        if action_context:
            context_str = f"""
Action performed: {action_context.get('action', 'unknown')}
Target element: {action_context.get('target', 'N/A')}
Expected result: {action_context.get('expected', 'N/A')}
"""
        
        prompt = f"""You are a senior QA engineer analyzing a website screenshot.

{context_str}

Analyze this screenshot and provide a detailed QA assessment:

1. **What is visible?**
   - Describe the page layout, main elements, and content

2. **Visual Issues:**
   - Any errors, broken layouts, missing images?
   - Any overlapping elements or misaligned content?
   - Any color contrast or accessibility issues?

3. **Functional Assessment:**
   - Does it look like the page loaded correctly?
   - Are interactive elements (buttons, forms) visible and properly styled?
   - Any error messages or warnings visible?

4. **UX Concerns:**
   - Is the layout user-friendly?
   - Are call-to-action buttons prominent?
   - Any confusing or unclear UI elements?

5. **Overall Assessment:**
   - Status: PASS, FAIL, or WARNING
   - Brief summary of findings

Be specific and detailed. Focus on actual issues, not theoretical concerns."""

        try:
            start_time = time.time()
            
            response = ollama.chat(
                model=self.vision_model,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [str(screenshot_path)]
                }],
                options={
                    'temperature': self.temperature,
                },
            )
            
            elapsed = time.time() - start_time
            raw_text = response['message']['content']
            
            # Parse response
            analysis = self._parse_analysis(raw_text)
            analysis['elapsed_seconds'] = round(elapsed, 2)
            analysis['model'] = self.vision_model
            
            return analysis
            
        except Exception as e:
            return {
                'summary': f"Analysis failed: {str(e)}",
                'findings': [],
                'status': 'ERROR',
                'issues': [],
                'raw_response': '',
                'error': str(e)
            }
    
    def compare_before_after(
        self,
        before_screenshot: Path,
        after_screenshot: Path,
        action: str,
        expected_change: Optional[str] = None
    ) -> Dict[str, Any]:
        """Compare two screenshots (before/after an action).
        
        Args:
            before_screenshot: Screenshot before action
            after_screenshot: Screenshot after action
            action: Description of action performed
            expected_change: What should have changed
        
        Returns:
            Dict with comparison results
        """
        expected_str = f"\nExpected change: {expected_change}" if expected_change else ""
        
        prompt = f"""You are a senior QA engineer comparing before/after screenshots of a website interaction.

Action performed: {action}{expected_str}

Compare these two screenshots (BEFORE on left, AFTER on right) and report:

1. **What Changed:**
   - List all visible changes between the screenshots
   - New elements that appeared
   - Elements that disappeared
   - Changes in layout, colors, or styling

2. **Was the Change Expected?**
   - Did the action produce the expected result?
   - Any unexpected changes or side effects?

3. **Issues Found:**
   - Any errors that appeared in the AFTER screenshot?
   - Any broken layouts or visual regressions?
   - Any elements that should have changed but didn't?

4. **Assessment:**
   - Status: PASS (worked as expected), FAIL (didn't work), or WARNING (worked but has issues)
   - Brief explanation

Be specific about differences. If you don't see any meaningful changes, say so clearly."""

        try:
            start_time = time.time()
            
            response = ollama.chat(
                model=self.vision_model,
                messages=[{
                    'role': 'user',
                    'content': prompt,
                    'images': [str(before_screenshot), str(after_screenshot)]
                }],
                options={
                    'temperature': self.temperature,
                }
            )
            
            elapsed = time.time() - start_time
            raw_text = response['message']['content']
            
            # Parse response
            analysis = self._parse_comparison(raw_text)
            analysis['elapsed_seconds'] = round(elapsed, 2)
            analysis['model'] = self.vision_model
            
            return analysis
            
        except Exception as e:
            return {
                'changes_detected': [],
                'expected_change_occurred': False,
                'status': 'ERROR',
                'issues': [],
                'raw_response': '',
                'error': str(e)
            }
    
    def generate_report_section(
        self,
        findings: List[Dict[str, Any]],
        section_type: str = "comprehensive"
    ) -> str:
        """Generate a section of the QA report from findings.
        
        Args:
            findings: List of findings from screenshot analyses
            section_type: Type of report (quick, standard, comprehensive)
        
        Returns:
            Formatted report section as markdown
        """
        findings_summary = "\n\n".join([
            f"Finding {i+1}:\n{json.dumps(f, indent=2)}"
            for i, f in enumerate(findings[:20])  # Limit to avoid token limits
        ])
        
        detail_instructions = {
            "quick": "Write a brief 2-3 paragraph summary of key findings.",
            "standard": "Write a standard QA report with sections for each major finding.",
            "comprehensive": "Write a comprehensive, detailed QA report with full analysis."
        }
        
        prompt = f"""You are a senior QA engineer writing a professional test report.

Based on these findings from the automated visual QA test:

{findings_summary}

{detail_instructions.get(section_type, detail_instructions['comprehensive'])}

Structure your report as:

## Test Execution Summary
- Overview of what was tested
- Number of issues found by severity

## Detailed Findings
For each significant issue:
- Description
- Severity (Critical, High, Medium, Low)
- Impact on users
- Steps to reproduce
- Recommended fix

## Recommendations
- Priority fixes
- UX improvements
- Any patterns or recurring issues

Write in clear, professional language. Be specific and actionable.
Use markdown formatting for better readability."""

        try:
            response = ollama.generate(
                model=self.text_model,
                prompt=prompt,
                options={
                    'temperature': self.temperature,
                }
            )
            
            return response['response']
            
        except Exception as e:
            return f"# Report Generation Failed\n\nError: {str(e)}"
    
    def _parse_analysis(self, raw_text: str) -> Dict[str, Any]:
        """Parse LLM analysis response into structured format."""
        # Simple parsing - extract status
        status = "WARNING"
        if "PASS" in raw_text.upper():
            status = "PASS"
        elif "FAIL" in raw_text.upper():
            status = "FAIL"
        
        # Extract issues (lines that mention problems)
        issues = []
        for line in raw_text.split('\n'):
            line_lower = line.lower()
            if any(word in line_lower for word in ['error', 'issue', 'problem', 'broken', 'missing']):
                issues.append({'description': line.strip(), 'severity': 'medium'})
        
        return {
            'summary': raw_text.split('\n\n')[0] if '\n\n' in raw_text else raw_text[:200],
            'findings': raw_text.split('\n\n'),
            'status': status,
            'issues': issues,
            'raw_response': raw_text
        }
    
    def _parse_comparison(self, raw_text: str) -> Dict[str, Any]:
        """Parse LLM comparison response into structured format."""
        status = "WARNING"
        if "PASS" in raw_text.upper():
            status = "PASS"
        elif "FAIL" in raw_text.upper():
            status = "FAIL"
        
        # Extract changes mentioned
        changes = []
        in_changes_section = False
        for line in raw_text.split('\n'):
            if 'what changed' in line.lower() or 'changes' in line.lower():
                in_changes_section = True
            elif in_changes_section and line.strip().startswith(('-', '*', '•')):
                changes.append(line.strip().lstrip('-*• '))
        
        return {
            'changes_detected': changes,
            'expected_change_occurred': status == "PASS",
            'status': status,
            'issues': [],
            'raw_response': raw_text
        }


# Convenience function
def analyze_screenshot(screenshot_path: Path, action_context: Optional[Dict] = None) -> Dict[str, Any]:
    """Quick function to analyze a screenshot."""
    llm = LocalVisionLLM()
    return llm.analyze_screenshot(screenshot_path, action_context)


if __name__ == "__main__":
    # Test the LLM vision analyzer
    print("Testing LocalVisionLLM...")
    
    try:
        llm = LocalVisionLLM()
        print("\n✅ LLM initialized successfully!")
        print(f"Vision Model: {llm.vision_model}")
        print(f"Text Model: {llm.text_model}")
        
        # Check if Ollama is running
        models = ollama.list()
        print(f"\nAvailable models: {[m['name'] for m in models.get('models', [])]}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. Ollama is installed and running")
        print("2. You've pulled the model: ollama pull llava:13b")
        print("3. ollama-python is installed: pip install ollama")
