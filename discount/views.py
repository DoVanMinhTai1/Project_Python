from django.http import JsonResponse
from .models import Discount
import datetime
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
@csrf_exempt
def apply_coupon(request):
    # Lấy coupon_code từ request (có thể lấy từ form hoặc từ query string)
    coupon_code = request.POST.get('coupon_code', '').strip()
    currency = request.POST.get('currency', 'USD')
    total_fare = request.POST.get('total_fare', '0')  # Chuyển đổi thành Decimal
    if currency == 'USD':
        total_fare = int(total_fare)  # Chuyển sang kiểu float sau khi làm sạch
    else :    
        total_fare = int(total_fare.replace('.', ''))  # Loại bỏ dấu phân cách hàng nghìn
       # Kiểm tra xem coupon có tồn tại trong cơ sở dữ liệu không
    try:
        coupon = Discount.objects.get(code=coupon_code)  # Dùng 'code' thay vì 'id'
    except Discount.DoesNotExist:
        return JsonResponse({'error': 'Mã coupon không hợp lệ.'}, status=400)

    # Kiểm tra đặc biệt với các mã coupon cụ thể
    if coupon.code == 'FL138S':
        today = datetime.date.today()
        if not (datetime.date(2025, 1, 1) <= today <= datetime.date(2025, 3, 1)):
            return JsonResponse({'error': 'Coupon "FL138S" chỉ có thể áp dụng từ 01/01/2025 đến 03/01/2025.'}, status=400)

    discount_percentage = coupon.discount_value  # Sử dụng trường discount_value trong Discount model
    # Tính toán giá trị tổng sau khi áp dụng giảm giá
    total_fare_with_discount = total_fare * (1 - discount_percentage / 100)

    # Lưu lại coupon đã áp dụng cho việc sử dụng sau (nếu cần)
    request.session['applied_coupon'] = coupon.code
    print(123)
    # Trả lại phản hồi JSON với thông tin về giá trị giảm giá và tổng sau khi giảm giá
    return JsonResponse({
        'total_fare': total_fare_with_discount,
        'discount': discount_percentage,  # Trả về mức giảm giá theo phần trăm
        'coupon_code': coupon.code,
        'currency': currency
    })
