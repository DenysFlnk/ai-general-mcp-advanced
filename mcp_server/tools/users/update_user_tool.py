from typing import Any

from models.user_info import UserUpdate
from tools.users.base import BaseUserServiceTool


class UpdateUserTool(BaseUserServiceTool):
    @property
    def name(self) -> str:
        return "update_user"

    @property
    def description(self) -> str:
        return "Updates user by id and provided info."

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                    "description": "User ID that should be updated.",
                },
                "new_info": UserUpdate.model_json_schema(),
            },
            "required": ["id"],
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        try:
            id = int(arguments["id"])
            request = UserUpdate.model_validate(arguments["new_info"])

            return await self._user_client.update_user(id, request)
        except Exception as e:
            err_msg = f"Exception while updating user: {e}"
            print(err_msg)
            return err_msg
