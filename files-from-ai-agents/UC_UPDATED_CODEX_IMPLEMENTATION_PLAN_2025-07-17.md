#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
Codex CLI Specialist Router - Aligned with Technical Roadmap
Routes tasks to repurposed Claude instances based on specialization
"""

import re
from typing import Dict, List, Optional

class SpecialistRouter:
    def __init__(self):
        # Agent roles as defined in technical roadmap
        self.specialists = {
            'AC': {
                'name': 'Lead Developer (Alpine Claude)',
                'role': 'General implementation, new features, core functionality',
                'keywords': ['implement', 'create', 'build', 'add', 'feature', 'develop',
                           'api', 'endpoint', 'function', 'module', 'component'],
                'strengths': ['Writing new code', 'Feature implementation', 'General development']
            },
            'DC': {
                'name': 'Code Optimizer (Debian Claude)',
                'role': 'Refactoring, performance tuning, testing, code quality',
                'keywords': ['optimize', 'refactor', 'performance', 'test', 'testing',
                           'improve', 'clean', 'lint', 'debug', 'fix', 'efficiency',
                           'coverage', 'unit test', 'integration test'],
                'strengths': ['Code optimization', 'Testing', 'Documentation', 'Performance']
            },
            'UC': {
                'name': 'Design/UX Expert (Ubuntu Claude)',
                'role': 'UI/UX improvements, aesthetics, user experience',
                'keywords': ['design', 'ui', 'ux', 'style', 'css', 'layout', 'pretty',
                           'beautiful', 'responsive', 'accessibility', 'interface',
                           'animation', 'color', 'typography', 'user experience'],
                'strengths': ['UI design', 'UX improvements', 'Visual aesthetics', 'Accessibility']
            }
        }
        
        # Task patterns for intelligent routing
        self.task_patterns = {
            'new_feature': r'(add|create|implement|build|develop) .*(feature|function|component)',
            'optimization': r'(optimize|improve|speed up|refactor|clean)',
            'bug_fix': r'(fix|bug|error|issue|problem|broken)',
            'testing': r'(test|testing|coverage|unit test)',
            'ui_improvement': r'(design|style|pretty|beautiful|ui|ux|interface)',
            'performance': r'(performance|slow|fast|efficient|optimize)'
        }
    
    def analyze_task(self, task_text: str, project_name: Optional[str] = None) -> Dict:
        """Analyze task and route to appropriate specialist"""
        task_lower = task_text.lower()
        
        # Score each specialist
        scores = {agent: 0 for agent in self.specialists}
        
        # Check keywords
        for agent, profile in self.specialists.items():
            for keyword in profile['keywords']:
                if keyword in task_lower:
                    scores[agent] += 2
        
        # Analyze task patterns
        task_type = self._identify_task_type(task_lower)
        
        # Apply pattern-based scoring
        if task_type in ['new_feature']:
            scores['AC'] += 5  # Lead Developer handles new features
        elif task_type in ['optimization', 'performance']:
            scores['DC'] += 5  # Code Optimizer handles performance
        elif task_type in ['testing', 'bug_fix']:
            scores['DC'] += 4  # Code Optimizer handles testing/fixes
        elif task_type == 'ui_improvement':
            scores['UC'] += 5  # Design/UX Expert handles UI
        
        # Special project affinities
        if project_name:
            project_lower = project_name.lower()
            if 'dashboard' in project_lower or 'ui' in project_lower:
                scores['UC'] += 3
            elif 'api' in project_lower or 'backend' in project_lower:
                scores['AC'] += 3
        
        # Determine best specialist
        best_agent = max(scores, key=scores.get)
        confidence = scores[best_agent]
        
        # Default to Lead Developer for general tasks
        if confidence == 0:
            best_agent = 'AC'
            confidence = 1
        
        return {
            'recommended_agent': best_agent,
            'specialist': self.specialists[best_agent]['name'],
            'role': self.specialists[best_agent]['role'],
            'confidence': confidence,
            'scores': scores,
            'task_type': task_type,
            'reasoning': self._generate_reasoning(task_text, best_agent, scores, task_type)
        }
    
    def _identify_task_type(self, task_lower: str) -> Optional[str]:
        """Identify the type of task based on patterns"""
        for pattern_name, pattern in self.task_patterns.items():
            if re.search(pattern, task_lower):
                return pattern_name
        return None
    
    def _generate_reasoning(self, task: str, agent: str, scores: Dict, task_type: str) -> str:
        """Generate explanation for routing decision"""
        specialist = self.specialists[agent]
        reasons = []
        
        if task_type:
            reasons.append(f"Task type: {task_type.replace('_', ' ')}")
        
        if scores[agent] > 0:
            matched_keywords = [kw for kw in specialist['keywords'] if kw in task.lower()]
            if matched_keywords:
                reasons.append(f"Keywords: {', '.join(matched_keywords[:3])}")
        
        reasons.append(f"Best suited for: {specialist['role']}")
        
        return " | ".join(reasons)
    
    def get_specialist_summary(self) -> str:
        """Get a summary of all specialists and their roles"""
        summary = "SPECIALIST AI AGENTS:\n" + "="*50 + "\n"
        for agent, profile in self.specialists.items():
            summary += f"\n{agent}: {profile['name']}\n"
            summary += f"   Role: {profile['role']}\n"
            summary += f"   Strengths: {', '.join(profile['strengths'])}\n"
        return summary


# CLI Interface for testing
if __name__ == "__main__":
    import sys
    
    router = SpecialistRouter()
    
    if len(sys.argv) > 1 and sys.argv[1] == "summary":
        print(router.get_specialist_summary())
    elif len(sys.argv) > 1:
        # Test with command line argument
        task = " ".join(sys.argv[1:])
        result = router.analyze_task(task)
        
        print(f"\nTask: {task}")
        print(f"Assigned to: {result['specialist']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Reasoning: {result['reasoning']}")
        print(f"\nAll scores: {result['scores']}")
    else:
        # Interactive mode
        print("Specialist Task Router - Enter tasks to analyze (or 'quit' to exit)")
        print(router.get_specialist_summary())
        
        while True:
            task = input("\nEnter task: ").strip()
            if task.lower() in ['quit', 'exit', 'q']:
                break
                
            result = router.analyze_task(task)
            print(f"\n→ {result['specialist']}")
            print(f"  Reasoning: {result['reasoning']}")