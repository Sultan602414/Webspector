"""Action processor that integrates browser actions with LLM vision analysis.

This module handles the callback from the browser driver, saves screenshots,
runs LLM analysis, and stores results in the database.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import config
from perception.llm_vision import LocalVisionLLM
from dashboard.db import Action, LLMAnalysis, get_session


class ActionProcessor:
    """Processes browser actions and analyzes them with LLM."""
    
    def __init__(
        self,
        session_id: int,
        output_dir: Path,
        enable_llm: bool = None
    ):
        """Initialize action processor.
        
        Args:
            session_id: Database test session ID
            output_dir: Directory to save screenshots
            enable_llm: Whether to use LLM analysis (defaults to config)
        """
        self.session_id = session_id
        self.output_dir = Path(output_dir)
        self.action_count = 0
        
        # Create subdirectories
        self.actions_dir = self.output_dir / "actions"
        self.actions_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize LLM if enabled
        self.enable_llm = enable_llm if enable_llm is not None else config.LLM_ANALYSIS_ENABLED
        self.llm = None
        if self.enable_llm:
            try:
                self.llm = LocalVisionLLM()
                print(f"[LLM] Initialized: {self.llm.vision_model}")
            except Exception as e:
                print(f"[LLM] Warning: Could not initialize LLM: {e}")
                print("[LLM] Continuing without LLM analysis...")
                self.enable_llm = False
    
    def process_action(self, action_data: Dict[str, Any]) -> Optional[int]:
        """Process a browser action: save screenshots, run LLM analysis, store in DB.
        
        Args:
            action_data: Dict with keys:
                - type: Action type (scroll, click_nav, etc)
                - target: What was interacted with
                - before_screenshot: Bytes of screenshot before action
                - after_screenshot: Bytes of screenshot after action
                - timestamp: ISO timestamp
        
        Returns:
            Action ID from database, or None if failed
        """
        self.action_count += 1
        action_type = action_data.get('type', 'unknown')
        target = action_data.get('target', '')
        
        print(f"\n[Action {self.action_count}] {action_type}: {target}")
        
        try:
            # Save screenshots to disk
            before_path = self._save_screenshot(
                action_data['before_screenshot'],
                f"action_{self.action_count:03d}_before.png"
            )
            after_path = self._save_screenshot(
                action_data['after_screenshot'],
                f"action_{self.action_count:03d}_after.png"
            )
            
            # Store action in database
            db = get_session()
            try:
                action = Action(
                    session_id=self.session_id,
                    sequence_number=self.action_count,
                    action_type=action_type,
                    target_element=target,
                    before_screenshot_path=str(before_path.relative_to(self.output_dir.parent)),
                    after_screenshot_path=str(after_path.relative_to(self.output_dir.parent)),
                    timestamp=datetime.fromisoformat(action_data['timestamp']),
                    metadata_json=json.dumps({
                        'original_data': {k: v for k, v in action_data.items() 
                                        if k not in ['before_screenshot', 'after_screenshot']}
                    })
                )
                db.add(action)
                db.flush()  # Get the action ID
                action_id = action.id
                
                # Run LLM analysis if enabled
                llm_analysis = None
                if self.enable_llm and self.llm:
                    print(f"[LLM] Analyzing action {self.action_count}...")
                    llm_analysis = self._analyze_action(
                        action_id=action_id,
                        before_path=before_path,
                        after_path=after_path,
                        action_context={
                            'action': action_type,
                            'target': target
                        }
                    )
                    if llm_analysis:
                        db.add(llm_analysis)
                
                db.commit()
                
                if llm_analysis:
                    print(f"[LLM] Status: {llm_analysis.status}")
                
                return action_id
                
            finally:
                db.close()
                
        except Exception as e:
            print(f"[Error] Failed to process action: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def _save_screenshot(self, screenshot_bytes: bytes, filename: str) -> Path:
        """Save screenshot bytes to disk."""
        filepath = self.actions_dir / filename
        filepath.write_bytes(screenshot_bytes)
        return filepath
    
    def _analyze_action(
        self,
        action_id: int,
        before_path: Path,
        after_path: Path,
        action_context: Dict[str, str]
    ) -> Optional[LLMAnalysis]:
        """Run LLM analysis on before/after screenshots.
        
        Args:
            action_id: Database action ID
            before_path: Path to before screenshot
            after_path: Path to after screenshot
            action_context: Dict with action type and target
        
        Returns:
            LLMAnalysis object or None if failed
        """
        try:
            # Compare before/after screenshots
            result = self.llm.compare_before_after(
                before_screenshot=before_path,
                after_screenshot=after_path,
                action=f"{action_context['action']} on {action_context['target']}",
                expected_change=None  # Could be enhanced later
            )
            
            # Create LLMAnalysis record
            analysis = LLMAnalysis(
                action_id=action_id,
                analysis_type='comparison',
                prompt_used=f"Compare before/after for {action_context['action']}",
                llm_response=result.get('raw_response', ''),
                status=result.get('status', 'UNKNOWN'),
                issues_found=json.dumps(result.get('issues', [])),
                model_used=result.get('model', self.llm.vision_model),
                elapsed_seconds=result.get('elapsed_seconds', 0.0)
            )
            
            return analysis
            
        except Exception as e:
            print(f"[LLM] Analysis failed: {e}")
            return None
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of processed actions."""
        return {
            'total_actions': self.action_count,
            'llm_enabled': self.enable_llm,
            'output_dir': str(self.actions_dir)
        }


# Convenience function to create callback
def create_action_callback(session_id: int, output_dir: Path) -> callable:
    """Create a callback function for browser driver.
    
    Args:
        session_id: Database test session ID
        output_dir: Directory to save screenshots
    
    Returns:
        Callback function that processes actions
    """
    processor = ActionProcessor(session_id, output_dir)
    return processor.process_action


if __name__ == "__main__":
    # Test the action processor
    print("Testing ActionProcessor...")
    
    # Create a test session
    from dashboard.db import init_engine, init_db, TestSession
    
    init_engine("sqlite:///test_actions.db")
    init_db()
    
    db = get_session()
    try:
        session = TestSession(url="https://example.com", depth=1, status="running")
        db.add(session)
        db.commit()
        db.refresh(session)
        
        print(f"Created test session: {session.id}")
        
        # Create processor
        processor = ActionProcessor(
            session_id=session.id,
            output_dir=Path("test_output"),
            enable_llm=False  # Disable for test
        )
        
        # Simulate an action (would normally come from browser)
        # For testing, create dummy screenshot data
        dummy_screenshot = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        
        action_data = {
            'type': 'scroll',
            'target': 'step 1/4',
            'before_screenshot': dummy_screenshot,
            'after_screenshot': dummy_screenshot,
            'timestamp': datetime.now().isoformat()
        }
        
        action_id = processor.process_action(action_data)
        print(f"Processed action ID: {action_id}")
        print(f"Summary: {processor.get_summary()}")
        
    finally:
        db.close()
    
    print("\n[OK] ActionProcessor test complete!")
