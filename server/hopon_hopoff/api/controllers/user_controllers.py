from django.db.models import Q
from django.contrib.auth.models import User
from api._serializers.user_serializers import UserSerializer
from api.ultils import format_datetime, pagination, sort_queryset


def process_user_data(page, page_size, search, sort_by, sort_order, filters):
    """
    Process user data to extract relevant information.
    """
    user_data = []
    total = 0
    try:
        users = User.objects.all()
        if filters:
            for key, value in filters.items():
                users = users.filter(**{key: value})
        if search:
            users = users.filter(Q(username__icontains=search) | Q(email__icontains=search))

        users = sort_queryset(users, sort_by, sort_order)
        (data, total) = pagination(users, page, page_size)
        serializer = UserSerializer(data, many=True)
        user_data = serializer.data
        
    except Exception as e:
        print(f"Error processing user data: {e}")
        user_data = []

    return user_data, total
    