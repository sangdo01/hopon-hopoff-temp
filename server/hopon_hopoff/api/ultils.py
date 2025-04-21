from rest_framework.response import Response

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
    filters = request.GET.get("filter", "").slipt(",")
    filter_obj = {}
    oparator = "="
    for filter in filters:
        items = filter.split(oparator)
        filter_obj[items[0]] = items[1]

    params = {
        "page": int(request.GET.get("page", 1)),
        "limit": int(request.GET.get("limit", 10)),
        "search": request.GET.get("search", ""),
        "filters": filter_obj,
        "sort_by": request.GET.get("sort_by", ""),
        "sort_order": request.GET.get("sort_order", ""),
    }
    return params

def get_UI_URL() -> str:
    """
    Get the UI URL from environment variables or use a default value.
    """
    return  "http://localhost:3000"
    
