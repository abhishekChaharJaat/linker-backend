from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.models.link import AddLinkRequest
from app.services.link_service import link_service

router = APIRouter(prefix="/links", tags=["links"])


@router.post("/add-new-link")
async def add_link(data: AddLinkRequest, user_id: str = Depends(get_current_user)):
    return await link_service.create_link(data, user_id)


@router.get("/get-all-links")
async def get_links(user_id: str = Depends(get_current_user)):
    return await link_service.get_all_links(user_id)


@router.delete("/{link_id}/delete-link")
async def delete_link(link_id: str, user_id: str = Depends(get_current_user)):
    return await link_service.delete_link(link_id, user_id)


@router.put("/{link_id}/edit-link")
async def edit_link(link_id: str, data: AddLinkRequest, user_id: str = Depends(get_current_user)):
    return await link_service.edit_link(link_id, data, user_id)
