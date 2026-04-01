"""
Roadmap Service - Generates actionable learning roadmaps from extracted skills.

For known skills uses a curated task library. For LLM-extracted skills that
don't match the library, generates sensible generic tasks so every skill
returned by the LLM becomes actionable study tickets — no dead ends.
"""

import logging

logger = logging.getLogger(__name__)

# ── Curated task library for common skills ──────────────────────────────────
SKILL_TASKS = {
    "Python": [
        {"task": "Learn Python basics — variables, loops, functions", "priority": "Beginner"},
        {"task": "Master object-oriented programming in Python", "priority": "Intermediate"},
        {"task": "Build Python projects and contribute to open source", "priority": "Advanced"},
    ],
    "JavaScript": [
        {"task": "Learn JavaScript fundamentals and ES6+ syntax", "priority": "Beginner"},
        {"task": "Master async programming — Promises, async/await", "priority": "Intermediate"},
        {"task": "Build full-stack JavaScript applications", "priority": "Advanced"},
    ],
    "TypeScript": [
        {"task": "Learn TypeScript basics and the type system", "priority": "Beginner"},
        {"task": "Apply TypeScript to a real React or Node.js project", "priority": "Intermediate"},
    ],
    "SQL": [
        {"task": "Learn SQL basics — SELECT, INSERT, UPDATE, DELETE", "priority": "Beginner"},
        {"task": "Master complex queries, JOINs, and window functions", "priority": "Intermediate"},
        {"task": "Learn database optimization, indexing, and query planning", "priority": "Advanced"},
    ],
    "Machine Learning": [
        {"task": "Learn ML fundamentals — supervised vs. unsupervised learning", "priority": "Beginner"},
        {"task": "Build ML models with scikit-learn on real datasets", "priority": "Intermediate"},
        {"task": "Deploy ML models to production and monitor drift", "priority": "Advanced"},
    ],
    "LLMs": [
        {"task": "Understand transformer architecture and attention mechanisms", "priority": "Intermediate"},
        {"task": "Practice prompt engineering and few-shot techniques", "priority": "Intermediate"},
        {"task": "Fine-tune and deploy open-source LLMs (Llama, Mistral)", "priority": "Advanced"},
    ],
    "RAG Pipelines": [
        {"task": "Learn retrieval-augmented generation concepts and architecture", "priority": "Intermediate"},
        {"task": "Build a RAG pipeline with LangChain and a vector DB", "priority": "Intermediate"},
        {"task": "Optimize retrieval quality — chunking, reranking, hybrid search", "priority": "Advanced"},
    ],
    "Prompt Engineering": [
        {"task": "Learn zero-shot, few-shot, and chain-of-thought prompting", "priority": "Beginner"},
        {"task": "Master system prompts, structured outputs, and tool use", "priority": "Intermediate"},
        {"task": "Build prompt evaluation frameworks and automated testing", "priority": "Advanced"},
    ],
    "LangChain": [
        {"task": "Learn LangChain fundamentals — chains, agents, tools", "priority": "Intermediate"},
        {"task": "Build a production LangChain agent with memory", "priority": "Advanced"},
    ],
    "Vector Databases": [
        {"task": "Learn vector embedding concepts and similarity search", "priority": "Intermediate"},
        {"task": "Integrate Pinecone, Weaviate, or ChromaDB into an app", "priority": "Advanced"},
    ],
    "Deep Learning": [
        {"task": "Learn neural network fundamentals and backpropagation", "priority": "Intermediate"},
        {"task": "Build and train deep learning models with PyTorch or TF", "priority": "Advanced"},
    ],
    "TensorFlow": [
        {"task": "Learn TensorFlow basics and the Keras API", "priority": "Intermediate"},
        {"task": "Build, train, and serve TensorFlow models", "priority": "Advanced"},
    ],
    "PyTorch": [
        {"task": "Learn PyTorch fundamentals — tensors, autograd, nn.Module", "priority": "Intermediate"},
        {"task": "Build and train neural networks with PyTorch Lightning", "priority": "Advanced"},
    ],
    "MLOps": [
        {"task": "Learn MLOps fundamentals — versioning, pipelines, monitoring", "priority": "Intermediate"},
        {"task": "Implement ML pipelines with MLflow or Kubeflow", "priority": "Advanced"},
    ],
    "NLP": [
        {"task": "Learn NLP fundamentals — tokenization, embeddings, POS tagging", "priority": "Intermediate"},
        {"task": "Build NLP applications using HuggingFace Transformers", "priority": "Advanced"},
    ],
    "Natural Language Processing": [
        {"task": "Learn NLP fundamentals — tokenization, embeddings, POS tagging", "priority": "Intermediate"},
        {"task": "Build NLP applications using HuggingFace Transformers", "priority": "Advanced"},
    ],
    "FastAPI": [
        {"task": "Learn FastAPI basics — routes, models, dependency injection", "priority": "Beginner"},
        {"task": "Build and document production-grade FastAPI services", "priority": "Intermediate"},
    ],
    "Docker": [
        {"task": "Learn Docker basics — images, containers, Dockerfile", "priority": "Intermediate"},
        {"task": "Containerize applications with Docker Compose", "priority": "Advanced"},
    ],
    "Kubernetes": [
        {"task": "Learn Kubernetes concepts — pods, deployments, services", "priority": "Advanced"},
        {"task": "Deploy and manage containerized apps on a K8s cluster", "priority": "Advanced"},
    ],
    "AWS": [
        {"task": "Learn AWS core services — EC2, S3, Lambda, IAM", "priority": "Intermediate"},
        {"task": "Build serverless and containerized apps on AWS", "priority": "Advanced"},
    ],
    "AWS SageMaker": [
        {"task": "Learn SageMaker fundamentals — training jobs, endpoints", "priority": "Intermediate"},
        {"task": "Deploy ML pipelines on SageMaker with auto-scaling", "priority": "Advanced"},
    ],
    "GCP": [
        {"task": "Learn Google Cloud Platform basics — GCS, BigQuery, Vertex AI", "priority": "Intermediate"},
        {"task": "Build and deploy ML models using Vertex AI", "priority": "Advanced"},
    ],
    "Azure": [
        {"task": "Learn Azure core services — Blob, AKS, Azure ML", "priority": "Intermediate"},
        {"task": "Build cloud solutions and pipelines on Azure", "priority": "Advanced"},
    ],
    "Terraform": [
        {"task": "Learn Infrastructure as Code with Terraform", "priority": "Intermediate"},
        {"task": "Manage multi-cloud infrastructure using Terraform modules", "priority": "Advanced"},
    ],
    "CI/CD": [
        {"task": "Learn CI/CD concepts and set up a GitHub Actions pipeline", "priority": "Intermediate"},
        {"task": "Build automated test, build, and deploy workflows", "priority": "Advanced"},
    ],
    "Git": [
        {"task": "Learn Git basics — commit, push, pull, branch, merge", "priority": "Beginner"},
        {"task": "Master Git workflows — rebase, squash, pull requests", "priority": "Intermediate"},
    ],
    "REST APIs": [
        {"task": "Learn REST API design principles and HTTP methods", "priority": "Beginner"},
        {"task": "Build, document, and version REST APIs", "priority": "Intermediate"},
    ],
    "React": [
        {"task": "Learn React fundamentals — components, state, props", "priority": "Beginner"},
        {"task": "Master React hooks, context, and performance patterns", "priority": "Intermediate"},
        {"task": "Build and deploy full-stack React applications", "priority": "Advanced"},
    ],
    "Node.js": [
        {"task": "Learn Node.js basics and Express.js", "priority": "Intermediate"},
        {"task": "Build REST APIs and microservices with Node.js", "priority": "Advanced"},
    ],
    "Data Analysis": [
        {"task": "Learn data analysis with Pandas and NumPy", "priority": "Beginner"},
        {"task": "Create exploratory data analysis reports and visualizations", "priority": "Intermediate"},
    ],
    "Data Visualization": [
        {"task": "Learn data visualization principles and chart types", "priority": "Beginner"},
        {"task": "Build interactive dashboards with Tableau or Power BI", "priority": "Intermediate"},
    ],
    "Statistics": [
        {"task": "Learn statistical fundamentals — distributions, hypothesis testing", "priority": "Beginner"},
        {"task": "Apply statistics to A/B testing and experiment design", "priority": "Intermediate"},
    ],
    "Feature Engineering": [
        {"task": "Learn feature selection and extraction techniques", "priority": "Intermediate"},
        {"task": "Build automated feature engineering pipelines", "priority": "Advanced"},
    ],
    "Pandas": [
        {"task": "Learn Pandas for data manipulation and cleaning", "priority": "Beginner"},
        {"task": "Master advanced Pandas — groupby, merge, time series", "priority": "Intermediate"},
    ],
    "NumPy": [
        {"task": "Learn NumPy arrays, broadcasting, and vectorized ops", "priority": "Beginner"},
        {"task": "Apply NumPy for numerical computing and linear algebra", "priority": "Intermediate"},
    ],
    "System Design": [
        {"task": "Learn system design fundamentals — scalability, caching, queues", "priority": "Intermediate"},
        {"task": "Practice designing large-scale distributed systems", "priority": "Advanced"},
    ],
    "Linux": [
        {"task": "Learn Linux command line basics and file system", "priority": "Beginner"},
        {"task": "Master Linux system administration and shell scripting", "priority": "Intermediate"},
    ],
    "Bash": [
        {"task": "Learn Bash scripting fundamentals", "priority": "Beginner"},
        {"task": "Write automation and DevOps scripts in Bash", "priority": "Intermediate"},
    ],
    "Redis": [
        {"task": "Learn Redis basics — strings, lists, hashes, sets", "priority": "Intermediate"},
        {"task": "Implement caching, sessions, and pub/sub with Redis", "priority": "Advanced"},
    ],
    "PostgreSQL": [
        {"task": "Learn PostgreSQL fundamentals and PSQL CLI", "priority": "Intermediate"},
        {"task": "Master advanced PostgreSQL — partitioning, full-text search", "priority": "Advanced"},
    ],
    "MongoDB": [
        {"task": "Learn MongoDB basics and CRUD operations", "priority": "Intermediate"},
        {"task": "Design MongoDB schemas and indexing strategies", "priority": "Advanced"},
    ],
    "Monitoring": [
        {"task": "Learn monitoring and logging basics — Prometheus, Grafana", "priority": "Intermediate"},
        {"task": "Set up full observability — traces, metrics, and alerts", "priority": "Advanced"},
    ],
    "Agile": [
        {"task": "Learn Agile methodology — Scrum, Kanban, sprints", "priority": "Beginner"},
        {"task": "Participate in and facilitate Agile ceremonies", "priority": "Intermediate"},
    ],
    "Communication": [
        {"task": "Practice technical writing and documentation", "priority": "Beginner"},
        {"task": "Improve presentation skills and cross-team collaboration", "priority": "Intermediate"},
    ],
    "Problem Solving": [
        {"task": "Practice coding challenges on LeetCode / HackerRank", "priority": "Beginner"},
        {"task": "Solve medium/hard LeetCode and system design problems", "priority": "Intermediate"},
    ],
    "Product Strategy": [
        {"task": "Learn product management fundamentals", "priority": "Beginner"},
        {"task": "Develop and communicate a product strategy", "priority": "Intermediate"},
    ],
    "User Research": [
        {"task": "Learn user research methods — interviews, surveys, usability", "priority": "Beginner"},
        {"task": "Conduct and synthesize user research findings", "priority": "Intermediate"},
    ],
    "A/B Testing": [
        {"task": "Learn A/B testing fundamentals and statistical significance", "priority": "Intermediate"},
        {"task": "Design, run, and analyze product experiments", "priority": "Advanced"},
    ],
    "Roadmapping": [
        {"task": "Learn product roadmap creation and prioritization frameworks", "priority": "Beginner"},
        {"task": "Master OKR-driven strategic planning", "priority": "Intermediate"},
    ],
    "Stakeholder Management": [
        {"task": "Learn stakeholder communication and alignment techniques", "priority": "Beginner"},
        {"task": "Master influence without authority and executive communication", "priority": "Intermediate"},
    ],
    "Jira": [
        {"task": "Learn Jira basics for project and sprint management", "priority": "Beginner"},
        {"task": "Master Jira workflows, epics, and reporting", "priority": "Intermediate"},
    ],
    "Cloud Computing": [
        {"task": "Learn cloud computing fundamentals — IaaS, PaaS, SaaS", "priority": "Beginner"},
        {"task": "Get certified in AWS, Azure, or GCP", "priority": "Intermediate"},
    ],
    "Security": [
        {"task": "Learn cybersecurity basics — OWASP top 10, auth patterns", "priority": "Beginner"},
        {"task": "Implement security best practices in applications", "priority": "Intermediate"},
    ],
    "Networking": [
        {"task": "Learn networking fundamentals — TCP/IP, DNS, HTTP", "priority": "Beginner"},
        {"task": "Understand cloud networking — VPCs, load balancers, CDNs", "priority": "Intermediate"},
    ],
    "Testing": [
        {"task": "Learn unit testing fundamentals and test-driven development", "priority": "Beginner"},
        {"task": "Implement integration tests, mocking, and E2E tests", "priority": "Intermediate"},
    ],
    "Microservices": [
        {"task": "Learn microservices architecture principles and trade-offs", "priority": "Intermediate"},
        {"task": "Design, build, and deploy a microservices system", "priority": "Advanced"},
    ],
    "Tableau": [
        {"task": "Learn Tableau basics — connecting data and building charts", "priority": "Beginner"},
        {"task": "Create interactive dashboards and publish to Tableau Server", "priority": "Intermediate"},
    ],
    "scikit-learn": [
        {"task": "Learn scikit-learn API — fit, predict, pipeline", "priority": "Intermediate"},
        {"task": "Build end-to-end ML pipelines with scikit-learn", "priority": "Advanced"},
    ],
    "HuggingFace": [
        {"task": "Learn the HuggingFace Transformers API and model hub", "priority": "Intermediate"},
        {"task": "Fine-tune and deploy HuggingFace models", "priority": "Advanced"},
    ],
}

PRIORITY_ORDER = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}


def generate_roadmap(skills: list) -> list:
    """
    Generate an actionable learning roadmap from a list of skills.

    For skills in the curated library, returns specific tasks.
    For LLM-extracted skills not in the library, generates generic
    but sensible Beginner / Intermediate / Advanced tasks.

    Args:
        skills: List of skill names (from skill_service.extract_skills)

    Returns:
        Sorted list of task dicts:
        [{"task": str, "skill": str, "status": str, "priority": str}, ...]
    """
    roadmap = []

    for skill in skills:
        tasks = SKILL_TASKS.get(skill)

        if tasks:
            for t in tasks:
                roadmap.append({
                    "task":     t["task"],
                    "skill":    skill,
                    "status":   "Not Started",
                    "priority": t["priority"],
                })
        else:
            # Generic tasks for any LLM-extracted skill not in the library
            logger.info(f"No curated tasks for '{skill}' — generating generic tasks")
            roadmap.extend([
                {
                    "task":     f"Learn {skill} fundamentals and core concepts",
                    "skill":    skill,
                    "status":   "Not Started",
                    "priority": "Beginner",
                },
                {
                    "task":     f"Build a hands-on project using {skill}",
                    "skill":    skill,
                    "status":   "Not Started",
                    "priority": "Intermediate",
                },
                {
                    "task":     f"Master advanced {skill} patterns and best practices",
                    "skill":    skill,
                    "status":   "Not Started",
                    "priority": "Advanced",
                },
            ])

    roadmap.sort(key=lambda x: PRIORITY_ORDER.get(x["priority"], 3))
    return roadmap