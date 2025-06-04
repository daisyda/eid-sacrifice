from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.core.management import call_command
from django.conf import settings
from ..models import Udhiyah
import json
import os

# ✅ فقط للمشرفين
def staff_required(view_func):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff, login_url='admin_login')(view_func)

# ✅ تسجيل دخول المشرف
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('choose_status')
        else:
            messages.error(request, 'اسم المستخدم أو كلمة المرور غير صحيحة، أو الحساب ليس مشرفاً.')

    return render(request, 'admin/admin_login.html')


# ✅ صفحة قائمة الأضاحي
@staff_required
def udhiya_list(request):
    udhiyas = Udhiyah.objects.all()
    return render(request, 'admin/udhiyah_list.html', {'udhiyas': udhiyas})


# ✅ تحديث الحالة
@csrf_exempt
@staff_required
def update_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        numbers = data.get('numbers', [])
        status_value = data.get('status', '')

        if not status_value:
            return JsonResponse({"error": "لا توجد حالة محددة"}, status=400)

        Udhiyah.objects.filter(serial_number__in=numbers).update(status=status_value)
        return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request"}, status=400)


# ✅ اختيار رقم
@staff_required
def choose_number(request):
    return render(request, 'admin/choose_number.html')


# ✅ اختيار حالة
@staff_required
def choose_status(request):
    return render(request, 'admin/choose_status.html')


# ✅ جلب الأرقام للحالة حسب التسلسل الصحيح
@staff_required
def get_sacrifice_numbers(request):
    status = request.GET.get("status", "")

    # التسلسل المنطقي للحالات
    status_flow = {
        "تم الذبح": "تم حجز الأضحية",
        "تم التقطيع": "تم الذبح",
        "جاري التوزيع": "تم التقطيع",
        "تم التوزيع": "جاري التوزيع",
    }

    previous_status = status_flow.get(status)
    if not previous_status:
        return JsonResponse({"numbers": [], "selected_numbers": []})

    # الأرقام الجاهزة تنتقل للحالة الجديدة
    valid_numbers = list(
        Udhiyah.objects.filter(status=previous_status).values_list("serial_number", flat=True)
    )

    # الأرقام اللي أصلاً في الحالة المطلوبة (عشان تظهر كمختارة)
    selected_numbers = list(
        Udhiyah.objects.filter(status=status).values_list("serial_number", flat=True)
    )

    all_displayed = list(set(valid_numbers + selected_numbers))

    return JsonResponse({
        "numbers": all_displayed,
        "selected_numbers": selected_numbers
    })


# ✅ صفحة: تم الذبح
@staff_required
def page_slaughtered(request):
    udhiyas = Udhiyah.objects.filter(status="تم حجز الأضحية")
    return render(request, 'admin/slaughtered.html', {
        "status": "تم الذبح",
        "udhiyas": udhiyas
    })


# ✅ صفحة: تم التقطيع
@staff_required
def page_Cut(request):
    udhiyas = Udhiyah.objects.filter(status="تم الذبح")
    return render(request, 'admin/cut.html', {
        "status": "تم التقطيع",
        "udhiyas": udhiyas
    })


# ✅ صفحة: جاري التوزيع
@staff_required
def page_Distributing_Now(request):
    udhiyas = Udhiyah.objects.filter(status="تم التقطيع")
    return render(request, 'admin/distributing_now.html', {
        "status": "جاري التوزيع",
        "udhiyas": udhiyas
    })


# ✅ صفحة: تم التوزيع
@staff_required
def page_Distributing_Done(request):
    udhiyas = Udhiyah.objects.filter(status="جاري التوزيع")
    return render(request, 'admin/distribution_done.html', {
        "status": "تم التوزيع",
        "udhiyas": udhiyas
    })


# ✅ تحميل البيانات من CSV
@staff_required
def run_load_sacrifices(request):
    try:
        filepath = os.path.join(settings.BASE_DIR, 'sacrifices.csv')
        if not os.path.exists(filepath):
            return HttpResponse("❌ ملف sacrifices.csv غير موجود")

        call_command('load_sacrifices', filepath)
        return HttpResponse("✅ تم تحميل الأضاحي بنجاح")
    except Exception as e:
        return HttpResponse(f"❌ خطأ: {str(e)}")
