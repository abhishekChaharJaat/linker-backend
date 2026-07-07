from bson import ObjectId
from app.database import db


class CategoryRepository:
    def __init__(self):
        self.collection = db.categories

    async def insert_category(self, category_data: dict) -> str:
        result = await self.collection.insert_one(category_data)
        return str(result.inserted_id)

    async def find_categories_by_user(self, user_id: str, limit: int = 100) -> list:
        cursor = self.collection.find({"user_id": user_id})
        return await cursor.to_list(limit)

    async def delete_category(self, category_id: str, user_id: str) -> int:
        result = await self.collection.delete_one({"_id": ObjectId(category_id), "user_id": user_id})
        return result.deleted_count

    async def update_category(self, category_id: str, user_id: str, update_data: dict) -> int:
        result = await self.collection.update_one(
            {"_id": ObjectId(category_id), "user_id": user_id},
            {"$set": update_data}
        )
        return result.matched_count


category_repository = CategoryRepository()
