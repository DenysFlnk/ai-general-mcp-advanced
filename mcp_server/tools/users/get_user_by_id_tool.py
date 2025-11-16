from typing import Any

from tools.users.base import BaseUserServiceTool


class GetUserByIdTool(BaseUserServiceTool):
    @property
    def name(self) -> str:
        return "get_user_by_id"

    @property
    def description(self) -> str:
        return "Gets user by id."

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                    "description": "User ID that should be retrieved.",
                },
            },
            "required": ["id"],
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        try:
            id = int(arguments["id"])
            return await self._user_client.get_user(id)
        except Exception as e:
            err_msg = f"Exception while getting a user: {e}"
            print(err_msg)
            return err_msg
