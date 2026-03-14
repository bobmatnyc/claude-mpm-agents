
# Agent file naming
 - agent filename must be a lowercase, kebab case dash-separated string without the '-agent' suffix. good: "python-engineer.md", "qa.md", bad: "python_Engineer.md", "python-engineer-agent.md"

# Agent frontmatter rules
 - agent_id field value must be a lowercase, kebab case dash-separated string without the '-agent' suffix. good: "python-engineer", bad: "python_Engineer", "python-engineer-agent"
 - name field value and use spaces as separators. good: "Python Engineer", bad: "Python_Engineer", "python-engineer-agent"
 - handoff_agents field values must match the agent_id of the target agent. Do not allow aspirational values, prevents drift. 