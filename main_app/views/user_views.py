from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ..models import Udhiyah, STATUS_CHOICES

# -------------------------------
# Donor Views
# -------------------------------

def donor_search(request):
    return render(request, 'user/donor_search.html')

def donor_status(request):
    udhiyah_id = request.GET.get('udhiyah_id')
    phone = request.GET.get('phone')

    record = Udhiyah.objects.filter(order_number=udhiyah_id, phone_number=phone).first()
    if not record:
        return render(request, 'user/donor_status.html', {'status': 'not_found'})

    donor_name = record.name
    current_status = record.status
    donation_type = getattr(record, 'donation_type', 'full')

    status_sequence = ['paid', 'booked', 'slaughtered', 'cutting']
    if donation_type == 'full':
        status_sequence += ['distributing', 'done']
    else:
        status_sequence += ['half_ready', 'distributing', 'done']

    timeline_steps = []
    current_index = status_sequence.index(current_status) if current_status in status_sequence else -1

    for i, step in enumerate(status_sequence):
        if i < current_index:
            status = 'done'
        elif i == current_index:
            status = 'active'
        else:
            status = 'upcoming'

        timeline_steps.append({
            'code': step,
            'label': dict(Udhiyah._meta.get_field('status').choices).get(step, step),
            'status': status
        })

    return render(request, 'user/donor_status.html', {
        'udhiyah_id': record.order_number,
        'phone': record.phone_number,
        'donor_name': donor_name,
        'status': current_status,
        'timeline_steps': timeline_steps,
    })
