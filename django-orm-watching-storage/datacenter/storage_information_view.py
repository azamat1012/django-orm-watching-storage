from datacenter.models import Visit, format_duration
from django.shortcuts import render
from django.utils import timezone


def storage_information_view(request):
    visits_with_no_leaving = Visit.objects.filter(leaved_at__isnull=True)

    non_closed_visits = []
    for visit in visits_with_no_leaving:
        entered_at = timezone.localtime(visit.entered_at)
        duration = visit.get_duration()
        formatted_duration = format_duration(duration)

        is_strange = visit.is_long(minutes=15)

        non_closed_visits.append({
            'who_entered': visit.passcard.owner_name,
            'entered_at': entered_at,
            'duration': formatted_duration,
            'is_strange': is_strange
        })

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
