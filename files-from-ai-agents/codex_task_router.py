#!/mnt/c/Users/david/projects-master/venv/bin/python
"""
Codex CLI Task Router
Routes tasks to appropriate AI agents based on content analysis
"""

import re
from typing import Dict, List, Optional, Tuple

class TaskRouter:
    def __init__(self):
        # Agent capabilities and keywords
        self.agent_profiles = {
            'UC': {
                'name': 'Ubuntu Claude (Design/UX)',
                'keywords': ['ui', 'ux', 'frontend', 'design', 'style', 'css', 'react', 
                           'dashboard', 'interface', 'component', 'layout', 'responsive',
                           'animation', 'color', 'typography', 'accessibility'],
                'project_affinity': ['personal dashboard', 'interactive resume', 'this page']
            },
            'DC': {
                'name': 'Debian Claude (Optimization)',  
                'keywords': ['optimize', 'performance', 'refactor', 'efficiency', 'test',
                           'debug', 'fix', 'improve', 'clean', 'lint', 'quality',
                           'backend', 'api', 'database', 'server', 'postgresql'],
                'project_affinity': ['operations center', 'maestro dashboard']
            },
            'AC': {
                'name': 'Alpine Claude (DevOps)',
                'keywords': ['deploy', 'devops', 'docker', 'ci/cd', 'render', 'hosting',
                           'environment', 'config', 'setup', 'install', 'infrastructure'],
                'project_affinity': []
            }
        }
        
        # Task type patterns
        self.task_patterns = {
            'bug_fix': r'(fix|bug|error|issue|problem|broken|crash)',
            'feature': r'(add|create|implement|build|new feature)',
            'optimization': r'(optimize|improve|speed up|enhance performance)',
            'ui_work': r'(design|style|layout|ui|ux|frontend)',
            'testing': r'(test|testing|coverage|unit test)',
            'deployment': r'(deploy|publish|release|hosting)'
        }
    
    def analyze_task(self, task_text: str, project_name: Optional[str] = None) -> Dict:
        """Analyze task and determine routing"""
        task_lower = task_text.lower()
        
        # Score each agent
        scores = {agent: 0 for agent in self.agent_profiles}
        
        # Check keywords
        for agent, profile in self.agent_profiles.items():
            for keyword in profile['keywords']:
                if keyword in task_lower:
                    scores[agent] += 2
        
        # Check project affinity
        if project_name:
            project_lower = project_name.lower()
            for agent, profile in self.agent_profiles.items():
                for project in profile['project_affinity']:
                    if project in project_lower:
                        scores[agent] += 5  # Strong project affinity
        
        # Check task patterns
        task_type = None
        for pattern_name, pattern in self.task_patterns.items():
            if re.search(pattern, task_lower):
                task_type = pattern_name
                break
        
        # Apply task type bonuses
        if task_type == 'bug_fix' or task_type == 'optimization':
            scores['DC'] += 3
        elif task_type == 'ui_work':
            scores['UC'] += 3
        elif task_type == 'deployment':
            scores['AC'] += 3
        elif task_type == 'testing':
            scores['DC'] += 2
        
        # Determine best agent
        best_agent = max(scores, key=scores.get)
        confidence = scores[best_agent]
        
        # If no clear winner, default to UC for general tasks
        if confidence == 0:
            best_agent = 'UC'
            confidence = 1
        
        return {
            'recommended_agent': best_agent,
            'agent_name': self.agent_profiles[best_agent]['name'],
            'confidence': confidence,
            'scores': scores,
            'task_type': task_type,
            'reasoning': self._generate_reasoning(task_text, best_agent, scores, task_type)
        }
    
    def _generate_reasoning(self, task: str, agent: str, scores: Dict, task_type: str) -> str:
        """Generate human-readable reasoning for the routing decision"""
        reasons = []
        
        if task_type:
            reasons.append(f"Task type identified as '{task_type}'")
        
        if scores[agent] > 0:
            profile = self.agent_profiles[agent]
            matched_keywords = [kw for kw in profile['keywords'] if kw in task.lower()]
            if matched_keywords:
                reasons.append(f"Keywords matched: {', '.join(matched_keywords[:3])}")
        
        if not reasons:
            reasons.append("Default routing for general task")
        
        return " | ".join(reasons)
    
    def route_batch(self, tasks: List[Dict]) -> List[Dict]:
        """Route multiple tasks and balance load"""
        routed_tasks = []
        agent_load = {'UC': 0, 'DC': 0, 'AC': 0}
        
        for task in tasks:
            routing = self.analyze_task(
                task.get('task', ''),
                task.get('project')
            )
            
            # Consider load balancing
            recommended = routing['recommended_agent']
            if agent_load[recommended] > 2:
                # Try to balance to next best agent
                sorted_agents = sorted(routing['scores'].items(), 
                                     key=lambda x: x[1], reverse=True)
                for agent, score in sorted_agents:
                    if agent_load[agent] < 2 and score > 0:
                        recommended = agent
                        routing['recommended_agent'] = agent
                        routing['reasoning'] += " | Load balanced"
                        break
            
            agent_load[recommended] += 1
            task['routing'] = routing
            routed_tasks.append(task)
        
        return routed_tasks


# CLI Interface
if __name__ == "__main__":
    import sys
    
    router = TaskRouter()
    
    if len(sys.argv) > 1:
        # Test with command line argument
        task = " ".join(sys.argv[1:])
        result = router.analyze_task(task)
        
        print(f"\nTask: {task}")
        print(f"Recommended Agent: {result['agent_name']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Reasoning: {result['reasoning']}")
        print(f"\nAll scores: {result['scores']}")
    else:
        # Interactive mode
        print("Task Router - Enter tasks to analyze (or 'quit' to exit)")
        while True:
            task = input("\nEnter task: ").strip()
            if task.lower() in ['quit', 'exit', 'q']:
                break
                
            result = router.analyze_task(task)
            print(f"\nRecommended: {result['agent_name']}")
            print(f"Confidence: {result['confidence']}")
            print(f"Reasoning: {result['reasoning']}")