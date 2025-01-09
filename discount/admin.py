# discounts/admin.py
from django.contrib import admin
from .models import Discount
from config.admin import custom_admin_site


class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        'code', 
        'discount_value', 
        'max_discount', 
        'min_order_value', 
        'start_date', 
        'end_date', 
        'is_active', 
        'usage_limit', 
        'times_used'
    )  # Hiển thị các trường trong danh sách
    search_fields = ('code',)  # Tìm kiếm theo mã giảm giá
    list_filter = ('is_active', 'start_date', 'end_date')  # Lọc theo trạng thái và ngày bắt đầu/kết thúc
    list_editable = ('is_active',)  # Cho phép chỉnh sửa trực tiếp trạng thái hoạt động
    list_per_page = 10  # Giới hạn số lượng mục hiển thị trên một trang
    readonly_fields = ('times_used',)  # Trường chỉ đọc để không cho phép chỉnh sửa thủ công

    class Media:
        css = {
            'all': ('css/custom_admin.css',)  # Đảm bảo bạn đã tạo file custom_admin.css trong static
        }
        js = ('js/admin/admin.js',)  # Đảm bảo file admin.js tồn tại trong static


# Đăng ký model Discount với custom admin site
custom_admin_site.register(Discount, DiscountAdmin)
