from typing import Any

from models.user_info import UserSearchRequest
from tools.users.base import BaseUserServiceTool


class SearchUsersTool(BaseUserServiceTool):
    @property
    def name(self) -> str:
        return "search_users"

    @property
    def description(self) -> str:
        return "Search users by provided parameters."

    @property
    def input_schema(self) -> dict[str, Any]:
        return UserSearchRequest.model_json_schema()

    async def execute(self, arguments: dict[str, Any]) -> str:
        try:
            return await self._user_client.search_users(**arguments)
        except Exception as e:
            err_msg = f"Exception while searching users: {e}"
            print(err_msg)
            return err_msg
