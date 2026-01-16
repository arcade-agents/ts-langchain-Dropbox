from arcadepy import AsyncArcade
from dotenv import load_dotenv
from google.adk import Agent, Runner
from google.adk.artifacts import InMemoryArtifactService
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService, Session
from google_adk_arcade.tools import get_arcade_tools
from google.genai import types
from human_in_the_loop import auth_tool, confirm_tool_usage

import os

load_dotenv(override=True)


async def main():
    app_name = "my_agent"
    user_id = os.getenv("ARCADE_USER_ID")

    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    client = AsyncArcade()

    agent_tools = await get_arcade_tools(
        client, toolkits=["Dropbox"]
    )

    for tool in agent_tools:
        await auth_tool(client, tool_name=tool.name, user_id=user_id)

    agent = Agent(
        model=LiteLlm(model=f"openai/{os.environ["OPENAI_MODEL"]}"),
        name="google_agent",
        instruction="# Introduction
Welcome to the Dropbox AI Agent! This agent is designed to assist you in managing your files on Dropbox efficiently. Whether you need to search for specific documents, list items in a folder, or download necessary files, the agent can streamline these tasks for you. By utilizing various tools, it can interact with your Dropbox storage seamlessly.

# Instructions
1. **Search for Files or Folders**: Use the search tool to find specific items based on keywords. 
2. **List Items in a Folder**: Browse the contents of a specific folder to see what files and folders are available.
3. **Download Files**: Download any file found using the previous workflows by providing either the file path or file ID.

# Workflows
## Workflow 1: Search for Files or Folders  
- **Tool**: `Dropbox_SearchFilesAndFolders`  
- **Parameters**: 
  - `keywords`: The terms you want to search for in your Dropbox.
  - `search_in_folder_path`: Optional folder path for more specific searches.
  - `limit`: Maximum number of items to return (default is 100). 
  
## Workflow 2: List Items in a Folder  
- **Tool**: `Dropbox_ListItemsInFolder`  
- **Parameters**: 
  - `folder_path`: Path to the folder you want to browse.
  - `limit`: Maximum number of items to return (default is 100).  

## Workflow 3: Download a File  
- **Tool**: `Dropbox_DownloadFile`  
- **Parameters**: 
  - `file_path` or `file_id`: Provide the path or ID of the file you wish to download.  

By following these workflows, the agent can efficiently handle your Dropbox tasks, making file management easier and quicker.",
        description="An agent that uses Dropbox tools provided to perform any task",
        tools=agent_tools,
        before_tool_callback=[confirm_tool_usage],
    )

    session = await session_service.create_session(
        app_name=app_name, user_id=user_id, state={
            "user_id": user_id,
        }
    )
    runner = Runner(
        app_name=app_name,
        agent=agent,
        artifact_service=artifact_service,
        session_service=session_service,
    )

    async def run_prompt(session: Session, new_message: str):
        content = types.Content(
            role='user', parts=[types.Part.from_text(text=new_message)]
        )
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].text:
                print(f'** {event.author}: {event.content.parts[0].text}')

    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        await run_prompt(session, user_input)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())