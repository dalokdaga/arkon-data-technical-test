from math import ceil
from typing import List, Any, Tuple, Dict


class Paginator:
    @staticmethod
    def paginate_results(results: List[Any], offset: int, limit: int) -> Tuple[List[Any], Dict[str, Any]]:
        total_items = len(results)
        start_index = offset
        end_index = min(offset + limit, total_items)
        total_pages = ceil(total_items / limit)
        current_page_results = results[start_index:end_index]
        pagination_info = {
            "total_items": total_items,
            "total_pages": total_pages,
            "current_page": offset // limit + 1,
            "items_per_page": limit
        }
        return current_page_results, pagination_info
