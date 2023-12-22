import asyncio

from tortoise import Tortoise, fields
from tortoise.models import Model

from db_app.config import config


class HltvMatchLinks(Model):
    link = fields.CharField(unique=True, max_length=1024)
    rating = fields.SmallIntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "hltv_match_links"

    def __str__(self) -> str:
        return (
            f"Link: {self.link}; "
            f"created_at: {self.created_at}; "
            f"updated_at: {self.updated_at}"
        )

    @classmethod
    def create_new_links_instances(cls, links_data: tuple[str, int]):
        return cls(
            link=links_data[0],
            rating=links_data[1],
        )


async def init_and_generate_schemas():
    await Tortoise.init(config)
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    asyncio.run(init_and_generate_schemas())
