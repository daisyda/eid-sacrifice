from django.urls import path
from main_app.views.admin_views import (
    run_load_sacrifices,
    admin_login_view,  # ✅ أضفنا هذا
    udhiya_list,
    update_status,
    choose_number,
    choose_status,
    get_sacrifice_numbers,
    page_slaughtered,
    page_Cut,
    page_Distributing_Now,
    page_Distributing_Done,
)

from .views.user_views import (
    donor_search,
    donor_status,
)

urlpatterns = [
    # --------- User Routes ---------
    path('', donor_search, name='donor_search'),
    path('status/', donor_status, name='donor_status'),
    #path('run-fix/', run_fix_status, name='run_fix_status'),

    # --------- Admin Auth ---------
    path('admin-login/', admin_login_view, name='admin_login'),  # ✅ أضفنا هذا

    # --------- Admin Pages ---------
    path('panel/choose-status/', choose_status, name='choose_status'),
    path('panel/slaughtered/', page_slaughtered, name='page_slaughtered'),
    path('panel/cut/', page_Cut, name='page_cut'),
    path('panel/distributing_now/', page_Distributing_Now, name='page_distributing_now'),
    path('panel/distributing_done/', page_Distributing_Done, name='page_distributing_done'),
    path('panel/udhiyas/', udhiya_list, name='udhiya_list'),

    # --------- API Endpoints ---------
    path('api/numbers/', get_sacrifice_numbers, name='get_sacrifice_numbers'),
    path('api/update-status/', update_status, name='update_status'),

    # --------- Admin Tools ---------
    path('admin/run-load/', run_load_sacrifices, name='run_load_sacrifices'),
]
