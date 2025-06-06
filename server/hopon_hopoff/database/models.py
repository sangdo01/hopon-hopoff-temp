from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.utils import timezone
from django.utils.crypto import get_random_string
import binascii
import os
from api.contants import REFRESH_TOKEN_EXPIRE_TIME, PASSWORD_RESET_TIMEOUT


#=================================== Authentication =============================================
class RefreshToken(models.Model):
    key = models.CharField(max_length=50, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='refresh_tokens')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'auth_refresh_token'

    def __str__(self):
        return self.key
    
    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        if not self.expires_at:
            # Refresh token valid for 7 days
            self.expires_at = timezone.now() + timezone.timedelta(seconds=REFRESH_TOKEN_EXPIRE_TIME)
        super().save(*args, **kwargs)

    def generate_key(self):
        # self.key = secrets.token_urlsafe(16)
        return binascii.hexlify(os.urandom(20)).decode()

    def is_expired(self):
        return timezone.now() > self.expires_at
    
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = 'auth_password_reset_token'

    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        if not self.expires_at:
            # Token valid for 1 hour
            self.expires_at = timezone.now() + timezone.timedelta(seconds=PASSWORD_RESET_TIMEOUT)
        super().save(*args, **kwargs)

    def generate_token(self):
        return get_random_string(50)

#=================================== Role-Based Access Control =============================================
class Role(models.Model):
    """Vai trò của người dùng trong hệ thống (Quản trị viên, Người dùng, Khách hàng)"""
    """Vai trò này sẽ được gán cho từng người dùng trong hệ thống"""
    """Vi dụ: admin, staff, customer"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Permission(models.Model):
    """Các hành động có thể cấp quyền"""
    """Quyền truy cập cho từng vai trò trong hệ thống"""
    """Ví dụ: Quyền xem, sửa, xóa thông tin tour, booking, khách hàng"""
    """Quyền này sẽ được gán cho từng vai trò trong hệ thống"""
    """Nếu không có quyền này thì sẽ kiểm tra theo role"""
    """Vi dụ: can_create_tour, can_read_tour, can_update_tour, can_delete_tour"""

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    module = models.CharField(max_length=50)  # Ví dụ: 'tour', 'booking', 'customer'
    action = models.CharField(max_length=50)  # Ví dụ: 'create', 'read', 'update', 'delete'
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['module', 'action']
        unique_together = ['module', 'action']

    def __str__(self):
        return f"{self.module}.{self.action}"

class RolePermission(models.Model):
    """Gán các quyền cho từng vai trò"""
    """Phân quyền cho từng vai trò"""
    """Ví dụ: Vai trò quản trị viên có quyền xem, sửa, xóa thông tin tour"""
    """Vai trò người dùng có quyền xem thông tin tour"""
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['role', 'permission']

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"

class UserRole(models.Model):
    """Gắn role với user"""
    """Phân quyền cho từng người dùng"""
    """Ví dụ: Người dùng A có quyền xem thông tin tour, booking"""
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['user', 'role']

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"
    

# RolePermission là mặc định
# UserPermission là override → bạn viết code has_permission() ưu tiên kiểm tra bảng này trước.
# Optional: user-permission override
class UserPermission(models.Model):
    """Gán quyền đặc biệt cho từng user"""
    """Phân quyền cho từng người dùng"""
    """Ví dụ: Người dùng A có quyền xem thông tin tour, booking"""
    """Nếu không có quyền này thì sẽ kiểm tra theo role"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'permission')

# User
#  └───1-1───> UserProfile
#                 └───N-1───> Role
#                                    └───N-N───> Permission (via RolePermission)

# User ─────N-N─────> Permission (via UserPermission)

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user.email})"
    
    @property
    def is_admin(self):
        return self.user.is_staff
    
    @property
    def is_customer(self):
        return not self.user.is_staff
    
    def get_active_bookings(self):
        return self.user.bookings.filter(status='active')
    
    def get_completed_bookings(self):
        return self.user.bookings.filter(status='completed')
    
    def get_total_spent(self):
        return self.user.bookings.filter(status='completed').aggregate(
            total=models.Sum('final_price')
        )['total'] or 0

#=================================== Tour Categories =============================================
class TourType(models.Model):
    """Phân loại tour (Trong nước, Nước ngoài)"""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100, null=True, blank=True)  # Quốc gia
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_active_destinations(self):
        """Get a list of active destinations in the city"""
        return self.destinations.filter(is_active=True)

    def get_tour_count(self):
        """Count the number of tours available in the city"""
        return Tour.objects.filter(destination__city=self).count()

    def get_popular_destinations(self, limit=5):
        """Get the most popular destinations in the city"""
        return self.destinations.filter(
            is_active=True
        ).annotate(
            tour_count=models.Count('tour')
        ).order_by('-tour_count')[:limit]

class Destination(models.Model):
    name = models.CharField(max_length=250)
    type = models.ForeignKey(TourType, on_delete=models.CASCADE, related_name='destinations', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='destinations', null=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.type.name})"

#=================================== Tour =============================================

class MeetingPoint(models.Model):
    name = models.CharField(max_length=500)
    link = models.URLField(max_length=500, blank=True, null=True)

class Tour(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá vé mặc định
    duration = models.IntegerField(help_text="Duration in days")
    max_participants = models.IntegerField() # Số lượng người tham gia tối đa
    current_participants = models.IntegerField(default=0) # Số lượng người tham gia hiện tại
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Thông tin địa điểm và phân loại
    tour_type  = models.ForeignKey(TourType, on_delete=models.SET_NULL, null=True)  # Trong nước/Nước ngoài
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True)  # Điểm đến cụ thể
    meeting_point = models.ForeignKey(MeetingPoint, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Thông tin tour
    departure_time = models.TimeField() # Thời gian khởi hành
    dynamic_level = models.IntegerField(null=True, blank=True) # Độ năng động
    meeting_point = models.TextField(blank=True)  # Điểm hẹn
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
        
    def get_main_image(self):
        return self.images.filter(is_main=True).first() # Sắp xếp theo thời gian tạo mới nhất

# Loại vé
class TicketType(models.Model):
    name = models.CharField(max_length=100)  # Ví dụ: "Người lớn", "Trẻ em", "Trẻ sơ sinh"
    code = models.CharField(max_length=20, unique=True)  # Ví dụ: "ADULT", "CHILD", "INFANT"
    description = models.TextField(blank=True)
    min_age = models.IntegerField(null=True, blank=True)  # Độ tuổi tối thiểu
    max_age = models.IntegerField(null=True, blank=True)  # Độ tuổi tối đa
    price_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100)  # Phần trăm giá so với giá gốc
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def calculate_price(self, base_price):
        """Calculate ticket price based on percentage of original price"""
        return base_price * (self.price_percentage / 100)

# Giá vé theo từng loại
class TourPricing(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="pricings")
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['tour', 'ticket_type']  # Đảm bảo mỗi loại vé chỉ có một giá cho mỗi tour

    def __str__(self):
        return f"{self.tour.name} - {self.ticket_type.name}"

# Quản lý nhiều hình ảnh cho mỗi tour
class TourImage(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='tours/')
    caption = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.tour.name}"

# # Lưu lịch trình chi tiết cho từng ngày của tour
# class TourSchedule(models.Model):
#     tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='schedules')
#     day_number = models.IntegerField()
#     title = models.CharField(max_length=200)
#     description = models.TextField()
    
#     class Meta:
#         ordering = ['day_number']
    
#     def __str__(self):
#         return f"{self.tour.name} - Day {self.day_number}"

#=================================== Booking Tour =============================================
class BookingInfo(models.Model):
    booking = models.OneToOneField('Booking', on_delete=models.CASCADE, related_name='booking_info')
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    full_name = models.CharField(max_length=200)
    country = models.CharField(max_length=100)
    hotel_address = models.TextField(blank=True)
    state = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Tour information
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='bookings')
    departure_date = models.DateTimeField()  # Ngày khởi hành
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    discount_code = models.CharField(max_length=50, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Tổng giá trước giảm
    final_price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá sau khi giảm
    
    def __str__(self):
        return f"Booking {self.id} - {self.tour.name}"
    
    def calculate_total_price(self):
        """Calculate the total price from the BookingItem"""
        return sum(item.total_price for item in self.items.all())
    
    def save(self, *args, **kwargs):
        """Automatically calculate total_price and final_price on save"""
        if not self.total_price:
            self.total_price = self.calculate_total_price()
        if not self.final_price:
            self.final_price = self.total_price - self.discount_amount
        super().save(*args, **kwargs)

# Chi tiết hóa từng loại vé trong booking
class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="items")
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)  # Giá một vé
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Tổng giá = unit_price * quantity

    def __str__(self):
        return f"{self.quantity} x {self.booking.tour.name} - {self.ticket_type.name}"
    
    def save(self, *args, **kwargs):
        """Automatically calculate total_price on save"""
        if not self.unit_price:
            self.unit_price = self.ticket_type.calculate_price(self.booking.tour.price)
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

class Discount(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    valid_from = models.DateTimeField() # Thời gian hiệu lực của mã bắt đầu
    valid_to = models.DateTimeField() # Thời gian hiệu lực của mã kết thúc
    is_active = models.BooleanField(default=True)
    max_uses = models.IntegerField(null=True, blank=True)  # Số lần sử dụng tối đa
    current_uses = models.IntegerField(null=True, blank=True, default=0)  # Số lần đã sử dụng
    min_purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Giá trị đơn hàng tối thiểu
    
    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"
    
    def is_valid(self):
        """Check if the discount code is valid"""
        now = timezone.now()
        return (
            self.is_active and
            self.valid_from <= now <= self.valid_to and
            (self.max_uses is None or self.current_uses < self.max_uses)
        )
    
    def apply_discount(self, total_amount):
        """Calculate the discount amount"""
        if not self.is_valid():
            return 0
        if self.min_purchase_amount and total_amount < self.min_purchase_amount:
            return 0
        return total_amount * (self.discount_percentage / 100)

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('wallet', 'E-Wallet/App Bank'),
        ('visa_master', 'Visa/Master/JCB'),
        ('atm', 'ATM Card'),
        ('momo', 'Momo'),
        ('zalo', 'ZaloPay'),
        ('shopee', 'ShopeePay'),
        ('viettel', 'Viettel Money'),
        ('qr', 'QR Code'),
    ]
    
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Số tiền thanh toán
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True) # ID giao dịch từ cổng thanh toán
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_completed_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    currency = models.CharField(max_length=20, null=True, blank=True) # Loại tiền tệ
    payment_provider = models.CharField(null=True, blank=True) # Nhà cung cấp dịch vụ thanh toán
    
    def __str__(self):
        return f"Payment {self.id} - {self.booking.tour.name} - {self.amount}"

class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.tour.name} by {self.user.get_full_name()}"

#===================================== Post ===========================
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)  # URL thân thiện
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_post_count(self):
        """Count the number of posts in a category"""
        return self.posts.count()
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    excerpt = models.TextField(blank=True)  # Tóm tắt bài viết
    views = models.PositiveIntegerField(default=0)  # Số lượt xem
    categories = models.ManyToManyField(Category, related_name='posts')  # Nhiều thể loại cho một bài viết
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='posts', null=True)

    def __str__(self):
        return self.title
    
    def get_main_image(self):
        return self.images.filter(is_main=True).first()
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='posts/')
    caption = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)  # Hình ảnh chính
    order = models.IntegerField(default=0)  # Thứ tự hiển thị
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"Image for {self.post.title}"


#===================================== Contact ===========================
class Contact(models.Model):
    email = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    message = models.TextField()

#===================================== Websit config ===========================
class WebsiteConfig(models.Model):
    hotline = models.CharField(max_length=200, blank=True, null=True)
    facebook_url = models.CharField(max_length=500, blank=True, null=True)
    twitter_url = models.CharField(max_length=500, blank=True, null=True)
    youtube_url = models.CharField(max_length=500, blank=True, null=True)
    company_url = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

#===================================== Menu and Pages ===========================
# class Menu(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(max_length=100, unique=True)
#     is_active = models.BooleanField(default=True)
#     order = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['order']
#         verbose_name = "Menu"
#         verbose_name_plural = "Menus"

#     def __str__(self):
#         return self.name

# class MenuItem(models.Model):
#     # menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')
#     title = models.CharField(max_length=100)
#     url = models.CharField(max_length=200, blank=True)
#     page = models.ForeignKey('Page', on_delete=models.SET_NULL, null=True, blank=True, related_name='menu_items')
#     parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
#     order = models.IntegerField(default=0)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['order']

#     def __str__(self):
#         return self.title

#     def get_url(self):
#         if self.page:
#             return self.page.get_absolute_url()
#         return self.url

# class Page(models.Model):
#     LAYOUT_CHOICES = [
#         ('default', 'Default Layout'),
#         ('full_width', 'Full Width'),
#         ('sidebar_left', 'Sidebar Left'),
#         ('sidebar_right', 'Sidebar Right'),
#         ('two_columns', 'Two Columns'),
#     ]

#     title = models.CharField(max_length=200)
#     slug = models.SlugField(max_length=200, unique=True)
#     content = models.TextField()
#     layout = models.CharField(max_length=20, choices=LAYOUT_CHOICES, default='default')
#     meta_title = models.CharField(max_length=200, blank=True)
#     meta_description = models.TextField(blank=True)
#     meta_keywords = models.CharField(max_length=200, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_homepage = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_pages')

#     class Meta:
#         ordering = ['-created_at']

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         if self.is_homepage:
#             return '/'
#         return f'/{self.slug}/'

#     def save(self, *args, **kwargs):
#         # Ensure only one page can be homepage
#         if self.is_homepage:
#             Page.objects.filter(is_homepage=True).exclude(pk=self.pk).update(is_homepage=False)
#         super().save(*args, **kwargs)

# class PageBlock(models.Model):
#     BLOCK_TYPE_CHOICES = [
#         ('text', 'Text Block'),
#         ('image', 'Image Block'),
#         ('gallery', 'Gallery Block'),
#         ('video', 'Video Block'),
#         ('form', 'Form Block'),
#         ('map', 'Map Block'),
#         ('custom', 'Custom HTML'),
#     ]

#     page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='blocks')
#     title = models.CharField(max_length=200)
#     block_type = models.CharField(max_length=20, choices=BLOCK_TYPE_CHOICES)
#     content = models.TextField()
#     order = models.IntegerField(default=0)
#     is_active = models.BooleanField(default=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ['order']

#     def __str__(self):
#         return f"{self.title} ({self.block_type})"
