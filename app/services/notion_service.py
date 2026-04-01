from notion_client import Client as NotionClient

notion = NotionClient(auth="YOUR_NOTION_KEY")
DATABASE_ID = "your_database_id_here"

def send_to_notion(roadmap: list, role: str = "") -> dict:
    tasks_created = 0
    for task in roadmap:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Task": {"title": [{"text": {"content": task["task"]}}]},
                "Skill": {"select": {"name": task["skill"]}},
                "Status": {"select": {"name": task["status"]}},
                "Priority": {"select": {"name": task["priority"]}},
                "Role": {"rich_text": [{"text": {"content": role}}]}
            }
        )
        tasks_created += 1

    return {
        "success": True,
        "message": f"Roadmap sent to Notion successfully ({tasks_created} tasks created)",
        "tasks_created": tasks_created,
        "role": role
    }