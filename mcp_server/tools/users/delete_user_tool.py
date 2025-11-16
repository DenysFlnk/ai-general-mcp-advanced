from typing import Any

from tools.users.base import BaseUserServiceTool


class DeleteUserTool(BaseUserServiceTool):
    @property
    def name(self) -> str:
        return "delete_users"

    @property
    def description(self) -> str:
        return "Deletes user by id."

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                    "description": "User ID that should be deleted.",
                },
            },
            "required": ["id"],
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        try:
            id = int(arguments["id"])
            return await self._user_client.delete_user(id)
        except Exception as e:
            err_msg = f"Exception while deleting user: {e}"
            print(err_msg)
            return err_msg
