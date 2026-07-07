from bson.errors import InvalidId
from fastapi import HTTPException
from app.repositories.category_repository import category_repository
from app.repositories.link_repository import link_repository
from app.models.category import AddCategoryRequest
from app.utils.serializers import serialize_doc


class CategoryService:
    async def create_category(self, data: AddCategoryRequest, user_id: str) -> dict:
        category_data = {
            "user_id": user_id,
            "name": data.name,
            "icon": data.icon,
            "color": data.color,
        }
        try:
            inserted_id = await category_repository.insert_category(category_data)
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to create category")
        category_data["_id"] = inserted_id
        return {"success": True, "message": "Category added successfully", "data": category_data}

    async def get_all_categories(self, user_id: str) -> dict:
        try:
            categories = await category_repository.find_categories_by_user(user_id)
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to fetch categories")
        return {"categories": [serialize_doc(cat) for cat in categories]}

    async def delete_category(self, category_id: str, user_id: str) -> dict:
        try:
            await link_repository.update_links_category(category_id, "other", user_id)
            deleted_count = await category_repository.delete_category(category_id, user_id)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid category ID format")
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to delete category")
        if deleted_count == 0:
            raise HTTPException(status_code=404, detail="Category not found or not authorized")
        return {"success": True, "message": "Category deleted and links moved to 'other'"}

    async def edit_category(self, category_id: str, data: AddCategoryRequest, user_id: str) -> dict:
        update_data = {
            "name": data.name,
            "icon": data.icon,
            "color": data.color,
        }
        try:
            matched_count = await category_repository.update_category(category_id, user_id, update_data)
        except InvalidId:
            raise HTTPException(status_code=400, detail="Invalid category ID format")
        except Exception:
            raise HTTPException(status_code=500, detail="Failed to update category")
        if matched_count == 0:
            raise HTTPException(status_code=404, detail="Category not found or not authorized")
        return {"success": True, "message": "Category updated successfully"}


category_service = CategoryService()
