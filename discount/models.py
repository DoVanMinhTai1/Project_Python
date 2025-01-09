from django.db import models
from django.utils.timezone import now

class Discount(models.Model):
    # Chỉ còn giảm giá theo phần trăm
    code = models.CharField(max_length=10, primary_key=True, unique=True, blank=True)
    discount_value = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Discount Percentage")
    max_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Maximum Discount (For Percentage)")
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Minimum Order Value")
    start_date = models.DateTimeField(default=now, verbose_name="Start Date")
    end_date = models.DateTimeField(verbose_name="End Date")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    usage_limit = models.PositiveIntegerField(null=True, blank=True, verbose_name="Usage Limit")
    times_used = models.PositiveIntegerField(default=0, verbose_name="Times Used")
    
    def is_valid(self):
        """Check if the coupon is valid."""
        if not self.is_active:
            return False
        if self.end_date and self.end_date < now():
            return False
        if self.usage_limit and self.times_used >= self.usage_limit:
            return False
        return True

    def apply_discount(self, order_total):
        """Calculate the discounted amount based on the order total."""
        if not self.is_valid():
            raise ValueError("Coupon is invalid or expired.")

        if self.min_order_value and order_total < self.min_order_value:
            raise ValueError(f"Order total must be at least {self.min_order_value}.")

        # Áp dụng giảm giá theo phần trăm
        discount = order_total * (self.discount_value / 100)
        
        # Giới hạn giảm giá tối đa (nếu có)
        if self.max_discount:
            discount = min(discount, self.max_discount)

        return max(order_total - discount, 0)  # Đảm bảo tổng không âm

    def use_coupon(self):
        """Increment the usage count."""
        if self.usage_limit and self.times_used >= self.usage_limit:
            raise ValueError("Coupon usage limit reached.")
        self.times_used += 1
        self.save()

    def __str__(self):
        return f"{self.discount_value}% Off"
