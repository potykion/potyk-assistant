from urllib.parse import urljoin
from typing import Any

import httpx


class BBCli:
    def __init__(
        self,
        email: str,
        # https://id.atlassian.com/manage-profile/security/api-tokens
        api_token: str,
        org: str,
        repo: str,
        base_url: str = "https://api.bitbucket.org",
    ) -> None:
        self.email = email
        self.api_token = api_token
        self.client = httpx.Client(auth=(self.email, self.api_token))
        self.org = org
        self.repo = repo
        self.base_url = base_url

    def __del__(self) -> None:
        self.client.close()

    def get_src(
        self,
        path_wo_slash: str,
        branch: str = "master",
    ) -> str:
        path = f"/2.0/repositories/{self.org}/{self.repo}/src/{branch}/{path_wo_slash}"
        resp = self.client.get(urljoin(self.base_url, path))
        return resp.text

    def commit(
        self,
        # like ".gitignore"
        path_wo_slash: str,
        content: str,
        msg: str | None = None,
        branch: str = "master",
    ) -> dict[str, Any]:
        msg = msg or f"Updated {path_wo_slash}"

        files: dict[str, Any] = {
            "message": (None, msg),
            "branch": (None, branch),
            f"/{path_wo_slash}": (
                path_wo_slash,
                content,
                "application/x-www-form-urlencoded",
            ),
        }
        path = f"/2.0/repositories/{self.org}/{self.repo}/src"

        resp = self.client.post(urljoin(self.base_url, path), files=files)
        if resp.is_success:
            return {"result": "ok"}
