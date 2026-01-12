"""LLM-powered comprehensive report generator.

Aggregates all findings from actions and LLM analyses to generate
detailed, human-quality QA reports.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from dashboard.db import Action, LLMAnalysis, TestSession, get_session
from perception.llm_vision import LocalVisionLLM
import config


class ComprehensiveReportGenerator:
    """Generates detailed QA reports from test sessions with LLM analysis."""
    
    def __init__(self):
        """Initialize report generator."""
        self.llm = None
        if config.LLM_ANALYSIS_ENABLED:
            try:
                self.llm = LocalVisionLLM()
            except Exception as e:
                print(f"[Report] Warning: Could not initialize LLM: {e}")
    
    def generate_report(self, session_id: int) -> Dict[str, Any]:
        """Generate comprehensive QA report for a test session.
        
        Args:
            session_id: Database test session ID
        
        Returns:
            Dict with report sections
        """
        db = get_session()
        try:
            # Get session data
            session = db.query(TestSession).get(session_id)
            if not session:
                raise ValueError(f"Session {session_id} not found")
            
            # Get all actions with LLM analyses
            actions = db.query(Action).filter(
                Action.session_id == session_id
            ).order_by(Action.sequence_number).all()
            
            # Aggregate findings
            findings = []
            for action in actions:
                if action.llm_analysis:
                    findings.append({
                        'action_number': action.sequence_number,
                        'action_type': action.action_type,
                        'target': action.target_element,
                        'status': action.llm_analysis.status,
                        'analysis': action.llm_analysis.llm_response,
                        'issues': json.loads(action.llm_analysis.issues_found or '[]'),
                        'timestamp': action.timestamp.isoformat()
                    })
            
            # Generate report sections
            report = {
                'session_id': session_id,
                'url': session.url,
                'generated_at': datetime.now().isoformat(),
                'executive_summary': self._generate_executive_summary(session, findings),
                'test_execution': self._generate_test_execution(actions, findings),
                'issues_breakdown': self._generate_issues_breakdown(findings),
                'recommendations': self._generate_recommendations(findings),
                'statistics': self._generate_statistics(session, actions, findings)
            }
            
            return report
            
        finally:
            db.close()
    
    def _generate_executive_summary(
        self,
        session: TestSession,
        findings: List[Dict]
    ) -> Dict[str, Any]:
        """Generate executive summary section."""
        total_actions = len(findings)
        failed_actions = sum(1 for f in findings if f['status'] == 'FAIL')
        warning_actions = sum(1 for f in findings if f['status'] == 'WARNING')
        passed_actions = sum(1 for f in findings if f['status'] == 'PASS')
        
        # Calculate quality score
        if total_actions > 0:
            quality_score = int((passed_actions / total_actions) * 100)
        else:
            quality_score = 100
        
        # Determine risk level
        if failed_actions > 0:
            risk_level = "HIGH"
        elif warning_actions > total_actions * 0.3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        summary_text = f"""
## Executive Summary

**Website:** {session.url}  
**Test Date:** {session.created_at.strftime('%Y-%m-%d %H:%M')}  
**Overall Quality Score:** {quality_score}/100  
**Risk Level:** {risk_level}

### Key Findings
- **Total Actions Tested:** {total_actions}
- **Passed:** {passed_actions} ({int(passed_actions/max(total_actions,1)*100)}%)
- **Failed:** {failed_actions}
- **Warnings:** {warning_actions}

### Assessment
{'✅ **PASS** - Website is functioning correctly with no critical issues.' if failed_actions == 0 and warning_actions == 0 else ''}
{'⚠️ **WARNING** - Website has some issues that should be reviewed.' if warning_actions > 0 and failed_actions == 0 else ''}
{'❌ **FAIL** - Website has critical issues that need immediate attention.' if failed_actions > 0 else ''}
"""
        
        return {
            'text': summary_text,
            'quality_score': quality_score,
            'risk_level': risk_level,
            'stats': {
                'total': total_actions,
                'passed': passed_actions,
                'failed': failed_actions,
                'warnings': warning_actions
            }
        }
    
    def _generate_test_execution(
        self,
        actions: List[Action],
        findings: List[Dict]
    ) -> Dict[str, Any]:
        """Generate test execution timeline."""
        timeline = []
        
        for i, action in enumerate(actions, 1):
            finding = next((f for f in findings if f['action_number'] == action.sequence_number), None)
            
            entry = {
                'step': i,
                'action': action.action_type,
                'target': action.target_element,
                'status': finding['status'] if finding else 'NO_LLM',
                'timestamp': action.timestamp.isoformat(),
                'before_screenshot': action.before_screenshot_path,
                'after_screenshot': action.after_screenshot_path
            }
            
            if finding:
                entry['analysis'] = finding['analysis'][:200] + '...' if len(finding['analysis']) > 200 else finding['analysis']
            
            timeline.append(entry)
        
        return {
            'timeline': timeline,
            'total_steps': len(timeline)
        }
    
    def _generate_issues_breakdown(self, findings: List[Dict]) -> Dict[str, Any]:
        """Generate detailed issues breakdown."""
        issues_by_severity = {
            'CRITICAL': [],
            'HIGH': [],
            'MEDIUM': [],
            'LOW': []
        }
        
        for finding in findings:
            if finding['status'] == 'FAIL':
                severity = 'CRITICAL' if 'error' in finding['analysis'].lower() else 'HIGH'
            elif finding['status'] == 'WARNING':
                severity = 'MEDIUM'
            else:
                continue
            
            issue = {
                'action_number': finding['action_number'],
                'description': f"{finding['action_type']} on {finding['target']}",
                'details': finding['analysis'][:300],
                'timestamp': finding['timestamp']
            }
            
            issues_by_severity[severity].append(issue)
        
        return issues_by_severity
    
    def _generate_recommendations(self, findings: List[Dict]) -> List[str]:
        """Generate recommendations."""
        recommendations = []
        
        failed_count = sum(1 for f in findings if f['status'] == 'FAIL')
        warning_count = sum(1 for f in findings if f['status'] == 'WARNING')
        
        if failed_count > 0:
            recommendations.append(f"**Priority 1:** Fix {failed_count} critical failures that prevent core functionality")
        
        if warning_count > 0:
            recommendations.append(f"**Priority 2:** Review and address {warning_count} warnings to improve user experience")
        
        # Add specific recommendations based on action types
        action_types = {}
        for f in findings:
            if f['status'] in ['FAIL', 'WARNING']:
                action_types[f['action_type']] = action_types.get(f['action_type'], 0) + 1
        
        for action_type, count in sorted(action_types.items(), key=lambda x: x[1], reverse=True):
            if count > 1:
                recommendations.append(f"Multiple issues found with **{action_type}** actions - review implementation")
        
        if not recommendations:
            recommendations.append("✅ No critical recommendations - website is performing well")
        
        return recommendations
    
    def _generate_statistics(
        self,
        session: TestSession,
        actions: List[Action],
        findings: List[Dict]
    ) -> Dict[str, Any]:
        """Generate test statistics."""
        duration = None
        if session.completed_at and session.created_at:
            duration = (session.completed_at - session.created_at).total_seconds()
        
        return {
            'duration_seconds': duration,
            'total_actions': len(actions),
            'llm_analyses': len(findings),
            'started_at': session.created_at.isoformat(),
            'completed_at': session.completed_at.isoformat() if session.completed_at else None
        }
    
    def export_as_markdown(self, report: Dict[str, Any]) -> str:
        """Export report as markdown."""
        md = f"""# QA Test Report

{report['executive_summary']['text']}

---

## Test Execution Timeline

Total Steps: {report['test_execution']['total_steps']}

| Step | Action | Target | Status |
|------|--------|--------|--------|
"""
        
        for entry in report['test_execution']['timeline']:
            md += f"| {entry['step']} | {entry['action']} | {entry['target'][:30]} | {entry['status']} |\n"
        
        md += "\n---\n\n## Issues Found\n\n"
        
        for severity in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            issues = report['issues_breakdown'][severity]
            if issues:
                md += f"\n### {severity} ({len(issues)} issues)\n\n"
                for issue in issues:
                    md += f"- **Action {issue['action_number']}**: {issue['description']}\n"
                    md += f"  {issue['details']}\n\n"
        
        md += "\n---\n\n## Recommendations\n\n"
        for i, rec in enumerate(report['recommendations'], 1):
            md += f"{i}. {rec}\n"
        
        return md


if __name__ == "__main__":
    # Test report generator
    generator = ComprehensiveReportGenerator()
    print("[Report] Generator initialized")
    print(f"[Report] LLM enabled: {generator.llm is not None}")
