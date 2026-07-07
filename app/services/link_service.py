from datetime import datetime
from bson.errors import InvalidId
from fastapi import HTTPException
from app.repositories.link_repository import link_repository
from app.models.link import AddLinkRequest
from app.utils.serializers import serialize_doc


class LinkService:
    async def create_link(self, data: AddLinkRequest, user_id: str) -> dict:
        link_data = {
            "user_id": user_id,
            "title": data.title,
            "url": data.url,
            "category": data.category,
            "project": data.project,
            "description": data.description,
            "created_at": datetime.utcnow()
        }
        try:
            inserted_id = await link_repository.insert_link(link_data)
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to create link")
        link_data["_id"] = inserted_id
        link_data["created_at"] = link_data["created_at"].isoformat()
        return {"success": True, "message": "Link added successfully", "data": link_data}

    async def get_all_links(self, user_id: str) -> dict:
        try:
            links = await link_repository.find_links_by_user(user_id)
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to fetch links")
        return {"links": [serialize_doc(link) for link in links]}

    async def delete_link(self, link_id: str, user_id: str) -> dict:
        try:
            deleted_count = await link_repository.delete_link(link_id, user_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid link ID format")
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to delete link")
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Link not found or not authorized")
        return {"success": True, "message": "Link deleted successfully"}

    async def edit_link(self, link_id: str, data: AddLinkRequest, user_id: str) -> dict:
        update_data = {
            "title": data.title,
            "url": data.url,
            "category": data.category,
            "project": data.project,
            "description": data.description,
        }
        try:
            matched_count = await link_repository.update_link(link_id, user_id, update_data)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid link ID format")
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to update link")
        if matched_count == 0:
            raise HTTPException(status_code=404, detail="Link not found or not authorized")
        return {"success": True, "message": "Link updated successfully"}


link_service = LinkService()
