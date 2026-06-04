from math import ceil

from sqlalchemy.orm import Query

from app.schemas.common import PageMeta


def paginate(query: Query, page: int, size: int):
    page = max(page, 1)
    size = min(max(size, 1), 100)
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    return items, PageMeta(total=total, page=page, size=size, pages=ceil(total / size) if total else 0)
