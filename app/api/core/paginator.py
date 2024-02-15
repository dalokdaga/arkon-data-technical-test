

class PaginationInfo:
    def __init__(self, total_items, limit, offset):
        self.total_items = total_items
        self.limit = limit
        self.offset = offset

    @property
    def total_pages(self):
        return (self.total_items + self.limit - 1) // self.limit

    @property
    def current_page(self):
        return self.offset // self.limit + 1

    def as_dict(self):
        return {
            "total_items": self.total_items,
            "total_pages": self.total_pages,
            "current_page": self.current_page,
            "items_per_page": self.limit
        }
