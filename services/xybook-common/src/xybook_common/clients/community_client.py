from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

import httpx


class CommunityClient:
    """Async httpx client for Community Service API."""

    def __init__(self, base_url: str = "http://localhost:8001"):
        self._client = httpx.AsyncClient(
            base_url=base_url, timeout=30.0, headers={"Content-Type": "application/json"}
        )

    async def close(self):
        await self._client.aclose()

    # --- Feed ---

    async def get_feed(
        self, sort: str = "latest", limit: int = 20, offset: int = 0
    ) -> list[dict[str, Any]]:
        resp = await self._client.get(
            "/api/community/feed", params={"sort": sort, "limit": limit, "offset": offset}
        )
        resp.raise_for_status()
        return resp.json()

    async def get_hot_posts(
        self, since: str | None = None, limit: int = 10, category: str | None = None
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit}
        if since:
            params["since"] = since
        if category:
            params["category"] = category
        resp = await self._client.get("/api/community/posts/hot", params=params)
        resp.raise_for_status()
        return resp.json()

    # --- Posts ---

    async def create_post(
        self,
        author_id: uuid.UUID,
        content: str,
        *,
        title: str | None = None,
        category: str | None = None,
        tags: list[str] | None = None,
        post_type: str | None = None,
        parent_id: uuid.UUID | None = None,
        root_post_id: uuid.UUID | None = None,
        media: list[str] | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "author_id": str(author_id),
            "content": content,
        }
        if title:
            body["title"] = title
        if category:
            body["category"] = category
        if tags:
            body["tags"] = tags
        if post_type:
            body["post_type"] = post_type
        if parent_id:
            body["parent_id"] = str(parent_id)
        if root_post_id:
            body["root_post_id"] = str(root_post_id)
        if media:
            body["media"] = media
        resp = await self._client.post("/api/community/posts", json=body)
        resp.raise_for_status()
        return resp.json()

    async def get_post(self, post_id: uuid.UUID) -> dict[str, Any]:
        resp = await self._client.get(f"/api/community/posts/{post_id}")
        resp.raise_for_status()
        return resp.json()

    async def get_post_thread(self, post_id: uuid.UUID) -> list[dict[str, Any]]:
        resp = await self._client.get(f"/api/community/posts/{post_id}/thread")
        resp.raise_for_status()
        return resp.json()

    async def get_new_replies(
        self, post_id: uuid.UUID, since: datetime
    ) -> list[dict[str, Any]]:
        resp = await self._client.get(
            f"/api/community/posts/{post_id}/new-replies",
            params={"since": since.isoformat()},
        )
        resp.raise_for_status()
        return resp.json()

    # --- Interactions ---

    async def like_post(
        self, post_id: uuid.UUID, user_id: uuid.UUID
    ) -> dict[str, Any]:
        resp = await self._client.post(
            f"/api/community/posts/{post_id}/like",
            json={"user_id": str(user_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def repost(
        self, post_id: uuid.UUID, user_id: uuid.UUID, content: str | None = None
    ) -> dict[str, Any]:
        body: dict[str, Any] = {"user_id": str(user_id)}
        if content:
            body["content"] = content
        resp = await self._client.post(
            f"/api/community/posts/{post_id}/repost", json=body
        )
        resp.raise_for_status()
        return resp.json()

    # --- Read States ---

    async def record_read_state(
        self, agent_id: uuid.UUID, post_id: uuid.UUID
    ) -> dict[str, Any]:
        resp = await self._client.post(
            "/api/community/read-states",
            json={"agent_id": str(agent_id), "post_id": str(post_id)},
        )
        resp.raise_for_status()
        return resp.json()

    async def batch_read_states(
        self, agent_id: uuid.UUID, post_ids: list[uuid.UUID]
    ) -> list[dict[str, Any]]:
        resp = await self._client.post(
            "/api/community/read-states/batch",
            json={"agent_id": str(agent_id), "post_ids": [str(pid) for pid in post_ids]},
        )
        resp.raise_for_status()
        return resp.json()

    async def get_read_states(
        self, agent_id: uuid.UUID
    ) -> list[dict[str, Any]]:
        resp = await self._client.get(
            "/api/community/read-states", params={"agent_id": str(agent_id)}
        )
        resp.raise_for_status()
        return resp.json()

    # --- My Threads ---

    async def get_my_threads(
        self, agent_id: uuid.UUID
    ) -> list[dict[str, Any]]:
        resp = await self._client.get(
            "/api/community/my/threads", params={"agent_id": str(agent_id)}
        )
        resp.raise_for_status()
        return resp.json()

    # --- Users ---

    async def get_user(self, user_id: uuid.UUID) -> dict[str, Any]:
        resp = await self._client.get(f"/api/community/users/{user_id}")
        resp.raise_for_status()
        return resp.json()

    async def get_user_posts(
        self, user_id: uuid.UUID, limit: int = 20, offset: int = 0
    ) -> list[dict[str, Any]]:
        resp = await self._client.get(
            f"/api/community/users/{user_id}/posts",
            params={"limit": limit, "offset": offset},
        )
        resp.raise_for_status()
        return resp.json()

    async def create_user(
        self,
        username: str,
        *,
        bio: str | None = None,
        avatar_url: str | None = None,
        location: str | None = None,
        tags: list[str] | None = None,
        is_agent: bool = True,
        agent_id: str | None = None,
    ) -> dict[str, Any]:
        body: dict[str, Any] = {
            "username": username,
            "is_agent": is_agent,
        }
        if bio:
            body["bio"] = bio
        if avatar_url:
            body["avatar_url"] = avatar_url
        if location:
            body["location"] = location
        if tags:
            body["tags"] = tags
        if agent_id:
            body["agent_id"] = agent_id
        resp = await self._client.post("/api/community/users", json=body)
        resp.raise_for_status()
        return resp.json()

    async def follow_user(
        self, user_id: uuid.UUID, target_id: uuid.UUID
    ) -> dict[str, Any]:
        resp = await self._client.post(
            f"/api/community/users/{target_id}/follow",
            json={"follower_id": str(user_id)},
        )
        resp.raise_for_status()
        return resp.json()

    # --- Notifications ---

    async def get_notifications(
        self, user_id: uuid.UUID
    ) -> list[dict[str, Any]]:
        resp = await self._client.get(
            "/api/community/notifications", params={"user_id": str(user_id)}
        )
        resp.raise_for_status()
        return resp.json()
