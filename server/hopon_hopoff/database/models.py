from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, URLValidator
from django.utils import timezone


#=================================== Role-Based Access Control =============================================
class Role(models.Model):
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
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['role', 'permission']

    def __str__(self):
        return f"{self.role.name} - {self.permission.name}"

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ['user', 'role']

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"


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
    tour_type  = models.ForeignKey(TourType, on_delete=models.DO_NOTHING)  # Trong nước/Nước ngoài
    destination = models.ForeignKey(Destination, on_delete=models.DO_NOTHING)  # Điểm đến cụ thể
    meeting_point = models.ForeignKey(MeetingPoint, on_delete=models.DO_NOTHING, null=True, blank=True)
    
    # Thông tin tour
    image = models.ImageField(upload_to='tours/', null=True, blank=True)
    departure_time = models.TimeField() # Thời gian khởi hành
    dynamic_level = models.IntegerField(null=True, blank=True) # Độ năng động
    meeting_point = models.TextField(blank=True)  # Điểm hẹn
    
    # Social media
    facebook_url = models.URLField(max_length=500, blank=True, null=True)
    instagram_url = models.URLField(max_length=500, blank=True, null=True)
    linkedin_url = models.URLField(max_length=500, blank=True, null=True)
    twitter_url = models.URLField(max_length=500, blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']  # Sắp xếp theo thời gian tạo mới nhất

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
        """Tính giá vé dựa trên phần trăm của giá gốc"""
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
    image = models.ImageField(upload_to='tour_images/')
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
# Customer information (Billing details)
class Customer(models.Model):
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
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
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
        """Tự động tính total_price khi lưu"""
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

# class Review(models.Model):
#     tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='reviews')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"Review for {self.tour.name} by {self.user.get_full_name()}"

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
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
