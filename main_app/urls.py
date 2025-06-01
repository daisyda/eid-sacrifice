from django.urls import path

# Admin Views
from .views.admin_views import (
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

# User Views
from .views.user_views import (
    donor_search,
    donor_status,
)

urlpatterns = [
    # --------- User Routes ---------
    path('', donor_search, name='donor_search'),
    path('status/', donor_status, name='donor_status'),
   

    #  Admin Pages (renamed to avoid conflict with Django admin)
    path('panel/choose-status/', choose_status, name='choose_status'),
    path('panel/slaughtered/', page_slaughtered, name='page_slaughtered'),
    path('panel/cut/', page_Cut, name='page_cut'),
    path('panel/distributing_now/', page_Distributing_Now, name='page_distributing_now'),
    path('panel/distributing_done/', page_Distributing_Done, name='page_distributing_done'),
    path('panel/udhiyas/', udhiya_list, name='udhiya_list'),
]
