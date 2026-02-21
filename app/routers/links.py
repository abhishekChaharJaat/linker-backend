from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.auth import get_current_user
from app.database import db

router = APIRouter(prefix="/links", tags=["links"])


class AddLinkRequest(BaseModel):
    title: str
    url: str
    category: str
    project: str
    description: Optional[str] = None

def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc.get("_id"):
        doc["_id"] = str(doc["_id"])
    if doc.get("created_at"):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc


@router.post("/add-new-link")
async def add_link(data: AddLinkRequest, user_id: str = Depends(get_current_user)):
    # Save the link to MongoDB
    link_data = {
        "user_id": user_id,
        "title": data.title,
        "url": data.url,
        "category": data.category,
        "project": data.project,
        "description": data.description,
        "created_at": datetime.utcnow()
    }
    result = await db.links.insert_one(link_data)
    link_data["_id"] = str(result.inserted_id)
    link_data["created_at"] = link_data["created_at"].isoformat()
    return {
        "success": True,
        "message": "Link added successfully",
        "data": link_data
    }


@router.get("/get-all-links")
async def get_links(user_id: str = Depends(get_current_user)):
    # Get links from MongoDB for this user
    cursor = db.links.find({"user_id": user_id})
    links = await cursor.to_list(500)
    return {"links": [serialize_doc(link) for link in links]}


@router.delete("/{link_id}/delete-link")
async def delete_link(link_id: str, user_id: str = Depends(get_current_user)):
    # Delete the link from MongoDB
    result = await db.links.delete_one({"_id": ObjectId(link_id), "user_id": user_id})
    if result.deleted_count == 1:
        return {"success": True, "message": "Link deleted successfully"}
    else:
        return {"success": False, "message": "Link not found or not authorized"}   


@router.put("/{link_id}/edit-link")
async def edit_link(link_id: str, data: AddLinkRequest, user_id: str = Depends(get_current_user)):
    # Update the link in MongoDB
    update_data = {
        "title": data.title,
        "url": data.url,
        "category": data.category,
        "project": data.project,
        "description": data.description,
    }
    result = await db.links.update_one(
        {"_id": ObjectId(link_id), "user_id": user_id},
        {"$set": update_data}
    )
    if result.matched_count == 1:
        return {"success": True, "message": "Link updated successfully"}
    else:
        return {"success": False, "message": "Link not found or not authorized"}

