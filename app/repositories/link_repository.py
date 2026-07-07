from bson import ObjectId
from app.database import db


class LinkRepository:
    def __init__(self):
        self.collection = db.links

    async def insert_link(self, link_data: dict) -> str:
        result = await self.collection.insert_one(link_data)
        return str(result.inserted_id)

    async def find_links_by_user(self, user_id: str, limit: int = 500) -> list:
        cursor = self.collection.find({"user_id": user_id})
        return await cursor.to_list(limit)

    async def delete_link(self, link_id: str, user_id: str) -> int:
        result = await self.collection.delete_one({"_id": ObjectId(link_id), "user_id": user_id})
        return result.deleted_count

    async def update_link(self, link_id: str, user_id: str, update_data: dict) -> int:
        result = await self.collection.update_one(
            {"_id": ObjectId(link_id), "user_id": user_id},
            {"$set": update_data}
        )
        return result.matched_count

    async def update_links_category(self, old_category: str, new_category: str, user_id: str):
        await self.collection.update_many(
            {"category": old_category, "user_id": user_id},
            {"$set": {"category": new_category}}
        )


link_repository = LinkRepository()
