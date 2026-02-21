from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from bson import ObjectId
from app.auth import get_current_user
from app.database import db

router = APIRouter(prefix="/categories", tags=["categories"])


class AddCategoryRequest(BaseModel):
    name: str
    icon: str
    color: str


def serialize_doc(doc):
    """Convert MongoDB document to JSON-serializable dict"""
    if doc.get("_id"):
        doc["_id"] = str(doc["_id"])
    if doc.get("created_at"):
        doc["created_at"] = doc["created_at"].isoformat()
    return doc


@router.post("/add-new-category")
async def add_category(data: AddCategoryRequest, user_id: str = Depends(get_current_user)):
    category_data = {
        "user_id": user_id,
        "name": data.name,
        "icon": data.icon,
        "color": data.color,
    }
    result = await db.categories.insert_one(category_data)
    category_data["_id"] = str(result.inserted_id)
    return {
        "success": True,
        "message": "Category added successfully",
        "data": category_data
    }


@router.get("/get-all-categories")
async def get_categories(user_id: str = Depends(get_current_user)):
    cursor = db.categories.find({"user_id": user_id})
    categories = await cursor.to_list(100)
    return {"categories": [serialize_doc(cat) for cat in categories]}


@router.delete("/{category_id}/delete-category")
async def delete_category(category_id: str, user_id: str = Depends(get_current_user)):
    # Move all links from this category to "other"
    await db.links.update_many(
        {"category": category_id, "user_id": user_id},
        {"$set": {"category": "other"}}
    )
    # Delete the category
    result = await db.categories.delete_one({"_id": ObjectId(category_id), "user_id": user_id})
    if result.deleted_count == 1:
        return {"success": True, "message": "Category deleted and links moved to 'other'"}
    else:
        return {"success": False, "message": "Category not found or not authorized"}


@router.put("/{category_id}/edit-category")
async def edit_category(category_id: str, data: AddCategoryRequest, user_id: str = Depends(get_current_user)):
    update_data = {
        "name": data.name,
        "description": data.description,
    }
    result = await db.categories.update_one(
        {"_id": ObjectId(category_id), "user_id": user_id},
        {"$set": update_data}
    )
    if result.matched_count == 1:
        return {"success": True, "message": "Category updated successfully"}
    else:
        return {"success": False, "message": "Category not found or not authorized"}
