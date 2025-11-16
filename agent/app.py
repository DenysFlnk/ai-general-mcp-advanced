import asyncio
import os

from clients.custom_mcp_client import CustomMCPClient
from clients.mcp_client import MCPClient
from clients.openai_client import OpenAIClient
from models.message import Message, Role

SYSTEM_PROMPT = """
You are the User Management Agent, responsible for managing user information within a controlled system.
Your primary tasks are to:

Create, read, update, and delete (CRUD) user records.

Search and filter users by specified criteria.

Behavioral Guidelines:

Respond in a clear, structured, and professional tone.

Confirm actions before performing critical operations (e.g., deletion).

Provide concise explanations and meaningful error messages when operations fail or data is missing.

Maintain consistency in output format and terminology.
"""


async def main():
    tools = []
    tool_maps: dict[str, MCPClient | CustomMCPClient] = {}

    ums_client = await CustomMCPClient.create("http://localhost:8006/mcp")
    remote_mcp_client = await CustomMCPClient.create(
        "https://remote.mcpservers.org/fetch/mcp"
    )

    ums_tools = await ums_client.get_tools()
    remote_tools = await remote_mcp_client.get_tools()
    tools.extend(ums_tools)
    tools.extend(remote_tools)

    for tool in ums_tools:
        tool_maps[tool["function"]["name"]] = ums_client

    for tool in remote_tools:
        tool_maps[tool["function"]["name"]] = remote_mcp_client

    openai_client = OpenAIClient(
        api_key=os.getenv("OPENAI_API_KEY", ""),
        model="gpt-4o",
        tools=tools,
        tool_name_client_map=tool_maps,
    )

    messages = [Message(role=Role.SYSTEM, content=SYSTEM_PROMPT)]

    while True:
        user_input = input("🧒: ").strip()

        if user_input.lower() == "exit":
            print("=" * 100)
            exit(0)

        messages.append(Message(role=Role.USER, content=user_input))

        response = await openai_client.get_completion(messages)

        messages.append(response)


if __name__ == "__main__":
    asyncio.run(main())


# Check if Arkadiy Dobkin present as a user, if not then search info about him in the web and add him
