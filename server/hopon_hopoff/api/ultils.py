from rest_framework.response import Response
from api.contants import PAGE_SIZE


def app_response(success: bool, data: dict, status: int = 200, total: int = 0) -> Response:
    """
    Format the response for the app.
    """
    res_dict = {
        "success": success,
    }
    if success:
        res_dict["data"] = data
    else:
        res_dict["error"] = data
    if total:
        res_dict["total"] = total
    return Response(res_dict, status=status)

def get_UI_URL() -> str:
    """
    Get the UI URL from environment variables or use a default value.
    """
    return "http://localhost:3000"

def format_time(time: str) -> str:
    """
    Format time from 'HH:MM' to 'HH:MM AM/PM'
    """
    if not time:
        return ""
    try:
        return time.strftime("%I:%M %p")
    except ValueError:
        return time
    
def format_date(date: str) -> str:
    """
    Format date from 'YYYY-MM-DD' to 'DD/MM/YYYY'
    """
    if not date:
        return ""
    try:
        return date.strftime("%d/%m/%Y")
    except ValueError:
        return date
    
def format_datetime(datetime: str) -> str:
    """
    Format datetime from 'YYYY-MM-DD HH:MM:SS' to 'DD/MM/YYYY HH:MM AM/PM'
    """
    if not datetime:
        return ""
    try:
        return datetime.strftime("%d/%m/%Y %I:%M %p")
    except ValueError:
        return datetime
    
def load_table_params(request) -> dict:
    """
    Load table parameters from request.
    """
    filters = request.GET.get("filter", "").split(",")
    filter_obj = {}
    oparator = "="
    for filter in filters:
        items = filter.split(oparator)
        if len(items) < 2:
            continue
        filter_obj[items[0]] = items[1]

    page = int(request.GET.get("page", 1))
    page_size = int(request.GET.get("page_size", PAGE_SIZE))
    search = request.GET.get("search", "")
    sort_by = request.GET.get("sort_by", "")
    sort_order = request.GET.get("sort_order", "")
    filters = filter_obj
    return page, page_size, search, sort_by, sort_order, filters

def string_to_int(string: str) -> int:
    """
    Convert string to int.
    """
    try:
        return int(string)
    except ValueError:
        return 0

def pagination(data, page, page_size) -> dict:
    """
    Paginate the data based on page and page size.
    returns a tuple of paginated data and total count.
    """
    page = string_to_int(page)
    page_size = string_to_int(page_size)
    page = page - 1 if page > 0 else page
    page_size = page_size if page_size > 0 else PAGE_SIZE
    start = page * page_size
    end = start + page_size
    total = len(data)
    if end > total:
        end = total
    if start > total:
        start = total
    data = data[start:end]
    return data, total

def sort_queryset(queryset, sort_by, sort_order) -> dict:
    """
    Sort queryset by given field and order.
    """
    if not sort_by or not sort_order:
        return queryset
    if sort_order == "asc":
        return queryset.order_by(sort_by)
    else:
        return queryset.order_by("-" + sort_by)

def sort_data(data, sort_by, sort_order) -> dict:
    """
    Sort data by given field and order.
    """
    if not sort_by or not sort_order:
        return data
    if sort_order == "asc":
        return sorted(data, key=lambda x: x[sort_by])
    else:
        return sorted(data, key=lambda x: x[sort_by], reverse=True)

    
