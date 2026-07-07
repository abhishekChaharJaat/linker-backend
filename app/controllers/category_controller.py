from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.models.category import AddCategoryRequest
from app.services.category_service import category_service

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/add-new-category")
async def add_category(data: AddCategoryRequest, user_id: str = Depends(get_current_user)):
    return await category_service.create_category(data, user_id)


@router.get("/get-all-categories")
async def get_categories(user_id: str = Depends(get_current_user)):
    return await category_service.get_all_categories(user_id)


@router.delete("/{category_id}/delete-category")
async def delete_category(category_id: str, user_id: str = Depends(get_current_user)):
    return await category_service.delete_category(category_id, user_id)


@router.put("/{category_id}/edit-category")
async def edit_category(category_id: str, data: AddCategoryRequest, user_id: str = Depends(get_current_user)):
    return await category_service.edit_category(category_id, data, user_id)
