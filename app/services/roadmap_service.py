"""
Roadmap Service - Generates learning roadmaps from skills.

This module provides functions to create structured learning roadmaps
based on the extracted skills for a career role.
"""


def generate_roadmap(skills: list) -> list:
    """
    Generate a learning roadmap from a list of skills.
    
    This function takes a list of skills and creates a structured
    learning roadmap with tasks, organized in a logical learning order.
    
    Args:
        skills: List of skill names to include in the roadmap.
               Example: ["Python", "Machine Learning", "SQL"]
    
    Returns:
        A list of task dictionaries, each containing:
        - task: Description of the learning task
        - skill: The skill this task relates to
        - status: Current status (always "Not Started" for new roadmaps)
        - priority: Learning priority (Beginner, Intermediate, Advanced)
        
        Example: [
            {"task": "Learn Python basics", "skill": "Python", "status": "Not Started", "priority": "Beginner"},
            {"task": "Build Python projects", "skill": "Python", "status": "Not Started", "priority": "Intermediate"},
            ...
        ]
    """
    # Define learning tasks for common skills
    # Each skill can have multiple learning tasks at different priority levels
    skill_learning_tasks = {
        "Python": [
            {"task": "Learn Python basics (variables, loops, functions)", "priority": "Beginner"},
            {"task": "Master object-oriented programming in Python", "priority": "Intermediate"},
            {"task": "Build Python projects and contribute to open source", "priority": "Advanced"},
        ],
        "JavaScript": [
            {"task": "Learn JavaScript fundamentals", "priority": "Beginner"},
            {"task": "Master async programming and ES6+ features", "priority": "Intermediate"},
            {"task": "Build full-stack JavaScript applications", "priority": "Advanced"},
        ],
        "TypeScript": [
            {"task": "Learn TypeScript basics and type system", "priority": "Beginner"},
            {"task": "Apply TypeScript in real projects", "priority": "Intermediate"},
        ],
        "SQL": [
            {"task": "Learn SQL basics (SELECT, INSERT, UPDATE, DELETE)", "priority": "Beginner"},
            {"task": "Master complex queries and joins", "priority": "Intermediate"},
            {"task": "Learn database optimization and indexing", "priority": "Advanced"},
        ],
        "Machine Learning": [
            {"task": "Learn ML fundamentals (supervised/unsupervised learning)", "priority": "Beginner"},
            {"task": "Build ML models with scikit-learn", "priority": "Intermediate"},
            {"task": "Deploy ML models to production", "priority": "Advanced"},
        ],
        "Deep Learning": [
            {"task": "Learn neural network fundamentals", "priority": "Intermediate"},
            {"task": "Build deep learning models with TensorFlow/PyTorch", "priority": "Advanced"},
        ],
        "TensorFlow": [
            {"task": "Learn TensorFlow basics and Keras API", "priority": "Intermediate"},
            {"task": "Build and deploy TensorFlow models", "priority": "Advanced"},
        ],
        "PyTorch": [
            {"task": "Learn PyTorch fundamentals", "priority": "Intermediate"},
            {"task": "Build neural networks with PyTorch", "priority": "Advanced"},
        ],
        "LLMs": [
            {"task": "Understand transformer architecture", "priority": "Intermediate"},
            {"task": "Learn prompt engineering techniques", "priority": "Intermediate"},
            {"task": "Fine-tune and deploy LLMs", "priority": "Advanced"},
        ],
        "NLP": [
            {"task": "Learn NLP fundamentals (tokenization, embeddings)", "priority": "Intermediate"},
            {"task": "Build NLP applications", "priority": "Advanced"},
        ],
        "Natural Language Processing": [
            {"task": "Learn NLP fundamentals (tokenization, embeddings)", "priority": "Intermediate"},
            {"task": "Build NLP applications", "priority": "Advanced"},
        ],
        "Data Analysis": [
            {"task": "Learn data analysis with Pandas and NumPy", "priority": "Beginner"},
            {"task": "Create data visualizations", "priority": "Intermediate"},
            {"task": "Perform statistical analysis", "priority": "Advanced"},
        ],
        "Git": [
            {"task": "Learn Git basics (commit, push, pull, branch)", "priority": "Beginner"},
            {"task": "Master Git workflows and collaboration", "priority": "Intermediate"},
        ],
        "Docker": [
            {"task": "Learn Docker basics (images, containers, Dockerfile)", "priority": "Intermediate"},
            {"task": "Containerize applications and use Docker Compose", "priority": "Advanced"},
        ],
        "Kubernetes": [
            {"task": "Learn Kubernetes fundamentals", "priority": "Advanced"},
            {"task": "Deploy and manage containerized applications", "priority": "Advanced"},
        ],
        "AWS": [
            {"task": "Learn AWS core services (EC2, S3, Lambda)", "priority": "Intermediate"},
            {"task": "Build serverless applications on AWS", "priority": "Advanced"},
        ],
        "REST APIs": [
            {"task": "Learn REST API design principles", "priority": "Beginner"},
            {"task": "Build and document REST APIs", "priority": "Intermediate"},
        ],
        "React": [
            {"task": "Learn React fundamentals (components, state, props)", "priority": "Beginner"},
            {"task": "Master React hooks and context", "priority": "Intermediate"},
            {"task": "Build full-stack React applications", "priority": "Advanced"},
        ],
        "HTML": [
            {"task": "Learn HTML5 semantics and structure", "priority": "Beginner"},
        ],
        "CSS": [
            {"task": "Learn CSS fundamentals and layouts", "priority": "Beginner"},
            {"task": "Master Flexbox, Grid, and responsive design", "priority": "Intermediate"},
        ],
        "Node.js": [
            {"task": "Learn Node.js basics and Express.js", "priority": "Intermediate"},
            {"task": "Build REST APIs with Node.js", "priority": "Intermediate"},
            {"task": "Master async patterns and microservices", "priority": "Advanced"},
        ],
        "CI/CD": [
            {"task": "Learn CI/CD concepts and tools", "priority": "Intermediate"},
            {"task": "Set up automated pipelines", "priority": "Advanced"},
        ],
        "Problem Solving": [
            {"task": "Practice coding challenges on LeetCode/HackerRank", "priority": "Beginner"},
            {"task": "Solve system design problems", "priority": "Intermediate"},
        ],
        "Communication": [
            {"task": "Practice technical writing and documentation", "priority": "Beginner"},
            {"task": "Improve presentation and teamwork skills", "priority": "Intermediate"},
        ],
        "Agile": [
            {"task": "Learn Agile methodology basics", "priority": "Beginner"},
            {"task": "Participate in Agile teams and sprints", "priority": "Intermediate"},
        ],
        "MongoDB": [
            {"task": "Learn MongoDB basics and CRUD operations", "priority": "Intermediate"},
            {"task": "Design MongoDB schemas and indexing", "priority": "Advanced"},
        ],
        "PostgreSQL": [
            {"task": "Learn PostgreSQL fundamentals", "priority": "Intermediate"},
            {"task": "Master advanced PostgreSQL features", "priority": "Advanced"},
        ],
        "Redis": [
            {"task": "Learn Redis basics and use cases", "priority": "Intermediate"},
            {"task": "Implement caching strategies with Redis", "priority": "Advanced"},
        ],
        "Linux": [
            {"task": "Learn Linux command line basics", "priority": "Beginner"},
            {"task": "Master Linux system administration", "priority": "Intermediate"},
        ],
        "Bash": [
            {"task": "Learn Bash scripting fundamentals", "priority": "Beginner"},
            {"task": "Write automation scripts", "priority": "Intermediate"},
        ],
        "Terraform": [
            {"task": "Learn Infrastructure as Code with Terraform", "priority": "Intermediate"},
            {"task": "Manage complex infrastructure with Terraform", "priority": "Advanced"},
        ],
        "Microservices": [
            {"task": "Learn microservices architecture principles", "priority": "Intermediate"},
            {"task": "Design and implement microservices", "priority": "Advanced"},
        ],
        "MLOps": [
            {"task": "Learn MLOps fundamentals", "priority": "Advanced"},
            {"task": "Implement ML pipelines and monitoring", "priority": "Advanced"},
        ],
        "Statistics": [
            {"task": "Learn statistical fundamentals", "priority": "Beginner"},
            {"task": "Apply statistics to data analysis", "priority": "Intermediate"},
        ],
        "Data Visualization": [
            {"task": "Learn data visualization principles", "priority": "Beginner"},
            {"task": "Create dashboards with Tableau/Power BI", "priority": "Intermediate"},
        ],
        "Pandas": [
            {"task": "Learn Pandas for data manipulation", "priority": "Beginner"},
            {"task": "Master advanced Pandas operations", "priority": "Intermediate"},
        ],
        "NumPy": [
            {"task": "Learn NumPy arrays and operations", "priority": "Beginner"},
            {"task": "Apply NumPy for numerical computing", "priority": "Intermediate"},
        ],
        "Java": [
            {"task": "Learn Java fundamentals", "priority": "Beginner"},
            {"task": "Master object-oriented programming in Java", "priority": "Intermediate"},
            {"task": "Build enterprise Java applications", "priority": "Advanced"},
        ],
        "R": [
            {"task": "Learn R programming basics", "priority": "Beginner"},
            {"task": "Perform statistical analysis with R", "priority": "Intermediate"},
        ],
        "Tableau": [
            {"task": "Learn Tableau basics", "priority": "Beginner"},
            {"task": "Create interactive dashboards", "priority": "Intermediate"},
        ],
        "Jupyter": [
            {"task": "Learn Jupyter notebook basics", "priority": "Beginner"},
            {"task": "Create reproducible data science projects", "priority": "Intermediate"},
        ],
        "Next.js": [
            {"task": "Learn Next.js fundamentals", "priority": "Intermediate"},
            {"task": "Build full-stack applications with Next.js", "priority": "Advanced"},
        ],
        "Responsive Design": [
            {"task": "Learn mobile-first responsive design", "priority": "Beginner"},
            {"task": "Master CSS frameworks for responsiveness", "priority": "Intermediate"},
        ],
        "Testing": [
            {"task": "Learn unit testing fundamentals", "priority": "Beginner"},
            {"task": "Implement integration and E2E tests", "priority": "Intermediate"},
        ],
        "Webpack": [
            {"task": "Learn Webpack configuration basics", "priority": "Intermediate"},
            {"task": "Optimize build processes", "priority": "Advanced"},
        ],
        "Azure": [
            {"task": "Learn Azure core services", "priority": "Intermediate"},
            {"task": "Build cloud solutions on Azure", "priority": "Advanced"},
        ],
        "GCP": [
            {"task": "Learn Google Cloud Platform basics", "priority": "Intermediate"},
            {"task": "Build applications on GCP", "priority": "Advanced"},
        ],
        "Networking": [
            {"task": "Learn networking fundamentals", "priority": "Beginner"},
            {"task": "Understand cloud networking", "priority": "Intermediate"},
        ],
        "Security": [
            {"task": "Learn cybersecurity basics", "priority": "Beginner"},
            {"task": "Implement security best practices", "priority": "Intermediate"},
        ],
        "Monitoring": [
            {"task": "Learn monitoring and logging basics", "priority": "Intermediate"},
            {"task": "Set up observability pipelines", "priority": "Advanced"},
        ],
        "Product Strategy": [
            {"task": "Learn product management fundamentals", "priority": "Beginner"},
            {"task": "Develop product strategy skills", "priority": "Intermediate"},
        ],
        "User Research": [
            {"task": "Learn user research methods", "priority": "Beginner"},
            {"task": "Conduct user interviews and analysis", "priority": "Intermediate"},
        ],
        "A/B Testing": [
            {"task": "Learn A/B testing fundamentals", "priority": "Intermediate"},
            {"task": "Design and analyze experiments", "priority": "Advanced"},
        ],
        "Roadmapping": [
            {"task": "Learn product roadmap creation", "priority": "Beginner"},
            {"task": "Master strategic planning", "priority": "Intermediate"},
        ],
        "Stakeholder Management": [
            {"task": "Learn stakeholder communication", "priority": "Beginner"},
            {"task": "Master stakeholder alignment", "priority": "Intermediate"},
        ],
        "Jira": [
            {"task": "Learn Jira basics for project management", "priority": "Beginner"},
            {"task": "Master Jira workflows and reporting", "priority": "Intermediate"},
        ],
        "Cloud Computing": [
            {"task": "Learn cloud computing fundamentals", "priority": "Beginner"},
            {"task": "Get certified in a cloud platform", "priority": "Intermediate"},
        ],
    }
    
    roadmap = []
    
    for skill in skills:
        # Check if we have predefined tasks for this skill
        skill_tasks = skill_learning_tasks.get(skill, None)
        
        if skill_tasks:
            # Add all predefined tasks for this skill
            for task_info in skill_tasks:
                roadmap.append({
                    "task": task_info["task"],
                    "skill": skill,
                    "status": "Not Started",
                    "priority": task_info["priority"]
                })
        else:
            # Generate generic learning tasks for unknown skills
            roadmap.append({
                "task": f"Learn {skill} fundamentals",
                "skill": skill,
                "status": "Not Started",
                "priority": "Beginner"
            })
            roadmap.append({
                "task": f"Build projects using {skill}",
                "skill": skill,
                "status": "Not Started",
                "priority": "Intermediate"
            })
            roadmap.append({
                "task": f"Master advanced {skill} concepts",
                "skill": skill,
                "status": "Not Started",
                "priority": "Advanced"
            })
    
    # Sort roadmap by priority (Beginner first, then Intermediate, then Advanced)
    priority_order = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
    roadmap.sort(key=lambda x: priority_order.get(x["priority"], 3))
    
    return roadmap