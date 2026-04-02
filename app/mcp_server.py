"""
MCP Server - Exposes career tracker pipeline as MCP tools.

Claude Desktop connects to this via stdio transport.
Each tool maps directly to one step in the pipeline.

Setup in claude_desktop_config.json:
{
  "mcpServers": {
    "career-tracker": {
      "command": "python",
      "args": ["-m", "app.mcp_server"],
      "cwd": "C:/path/to/your/project"
    }
  }
}
"""

import json
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from app.services.search_service import search_web
from app.services.llm_service import analyze_data
from app.services.roadmap_service import generate_roadmap
from app.services.sqlite_service import send_to_notion, get_all_roadmaps, update_task_status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

server = Server("career-tracker")


@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="analyze_career_role",
            description=(
                "Full career analysis pipeline: searches the web for a role, "
                "extracts required skills using a local LLM (Ollama), generates "
                "a learning roadmap, and saves everything to SQLite. "
                "Use this when the user wants to explore a career path or get a learning plan."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "description": "Career role to analyze, e.g. 'AI Engineer', 'Data Scientist'",
                    }
                },
                "required": ["role"],
            },
        ),
        Tool(
            name="search_skills_for_role",
            description=(
                "Search the web for skills and job requirements for a career role. "
                "Returns raw search results without LLM processing. "
                "Use when you only need current job market data."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {
                        "type": "string",
                        "description": "Career role to search for",
                    }
                },
                "required": ["role"],
            },
        ),
        Tool(
            name="generate_learning_roadmap",
            description=(
                "Generate a structured learning roadmap from a list of skills. "
                "Returns prioritized tasks (Beginner / Intermediate / Advanced). "
                "Use when you already have a skills list and want actionable next steps."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "skills": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of skill names to generate a roadmap for",
                    }
                },
                "required": ["skills"],
            },
        ),
        Tool(
            name="get_career_history",
            description=(
                "Retrieve all previously analyzed career roles and their roadmaps from the database. "
                "Use when the user wants to review past analyses or track progress."
            ),
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        Tool(
            name="update_task_progress",
            description=(
                "Update the status of a learning task in the database. "
                "Valid statuses: 'Not Started', 'In Progress', 'Completed'. "
                "Use when the user wants to mark progress on their learning roadmap."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "task_id": {
                        "type": "integer",
                        "description": "The task ID to update",
                    },
                    "status": {
                        "type": "string",
                        "enum": ["Not Started", "In Progress", "Completed"],
                        "description": "New status for the task",
                    },
                },
                "required": ["task_id", "status"],
            },
        ),
        Tool(
            name="get_memory_summary",
            description=(
                "Retrieve the user's full career learning memory: all roles analyzed, "
                "skills learned, tasks completed, tasks in progress, and skill gaps. "
                "Use this at the START of any career conversation to personalize advice."
            ),
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="get_role_memory",
            description=(
                "Retrieve detailed memory for a specific career role: progress percentage, "
                "skill gap, completed and in-progress tasks. "
                "Use when the user asks about a specific role they've tracked before."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "role": {"type": "string", "description": "The career role to look up"}
                },
                "required": ["role"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:

    if name == "analyze_career_role":
        role = arguments["role"].strip()
        logger.info(f"MCP: analyze_career_role → '{role}'")

        search_results = search_web(role)
        skills = analyze_data(search_results)
        roadmap = generate_roadmap(skills)
        db_sync = send_to_notion(roadmap, role)

        result = {
            "role": role,
            "skills": skills,
            "total_tasks": len(roadmap),
            "db_sync": db_sync,
            "roadmap_preview": roadmap[:5],  # first 5 tasks as preview
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "search_skills_for_role":
        role = arguments["role"].strip()
        logger.info(f"MCP: search_skills_for_role → '{role}'")

        search_results = search_web(role)
        result = {
            "role": role,
            "total_results": len(search_results.get("results", [])),
            "results": search_results.get("results", []),
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "generate_learning_roadmap":
        skills = arguments["skills"]
        logger.info(f"MCP: generate_learning_roadmap → {skills}")

        roadmap = generate_roadmap(skills)
        result = {
            "skills": skills,
            "total_tasks": len(roadmap),
            "roadmap": roadmap,
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "get_career_history":
        logger.info("MCP: get_career_history")

        roadmaps = get_all_roadmaps()
        result = {
            "total_roadmaps": len(roadmaps),
            "roadmaps": roadmaps,
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "update_task_progress":
        task_id = arguments["task_id"]
        status = arguments["status"]
        logger.info(f"MCP: update_task_progress → task {task_id} = '{status}'")

        success = update_task_status(task_id, status)
        result = {
            "success": success,
            "task_id": task_id,
            "status": status,
        }
        return [TextContent(type="text", text=json.dumps(result, indent=2))]
    
    elif name == "get_memory_summary":
        from app.services.memory_service import get_memory_summary
        result = get_memory_summary()
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "get_role_memory":
        from app.services.memory_service import get_role_memory
        result = get_role_memory(arguments["role"])
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    else:
        return [TextContent(type="text", text=json.dumps({"error": f"Unknown tool: {name}"}))]


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())