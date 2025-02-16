import requests


class xelAAPI:
    def __init__(self, config: dict):
        self.base_url = f"http://127.0.0.1:{config['XELA_PORT']}"

    def query(self, method: str, path: str, **kwargs) -> dict:
        r = requests.request(
            method.lower(),
            f"{self.base_url}{path}",
            **kwargs
        )

        if r.status_code != 200:
            raise Exception(r.text)

        return r.json()

    def get_ban(self, guild_id: int, user_id: int) -> dict:
        return self.query(
            "GET",
            f"/guilds/{guild_id}/bans/{user_id}"
        )

    def get_invite(self, invite_code: str) -> dict:
        return self.query(
            "GET",
            f"/invites/{invite_code}"
        )

    def get_guild(self, guild_id: int) -> dict:
        return self.query(
            "GET",
            f"/guilds/{guild_id}"
        )

    def get_appeal(self, user_id: int, appeal_id: str) -> dict:
        return self.query(
            "GET",
            f"/appeals/{user_id}/{appeal_id}"
        )

    def get_all_appeals(self, user_id: int) -> list[dict]:
        return self.query(
            "GET",
            f"/appeals/{user_id}"
        )

    def post_appeal(self, guild_id: int, user_id: int, reason: str) -> dict:
        return self.query(
            "POST",
            f"/guilds/{guild_id}/appeals/{user_id}",
            json={"appeal_reason": reason}
        )
