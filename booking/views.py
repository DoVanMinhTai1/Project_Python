from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from payment.models import Ticket, Payment, PaymentTicket


def bookings(request):
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user).order_by('-booking_date')
        return render(request, 'bookings.html', {
            'page': 'bookings',
            'tickets': tickets,
        })
    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def cancel_ticket(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ref = request.POST['ref']
            try:
                ticket = Ticket.objects.get(ref_no=ref)
                if ticket.user == request.user:
                    ticket.status = 'CANCELLED'
                    ticket.save()
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({
                        'success': False,
                        'error': "User unauthorised"
                    })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': e
                })
        else:
            return HttpResponse("User unauthorised")
    else:
        return HttpResponse("Method must be POST.")


def resume_booking(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ticket = Ticket.objects.get(id=request.POST['ticketId'])
            tickets = [Ticket.objects.get(t.ticket) for t in PaymentTicket.objects.filter(payment=PaymentTicket.objects.get(ticket=ticket).payment)]
            totalFare = 0
            for t in tickets:
                totalFare += t.flight_fare
            if ticket.user == request.user:
                return render(request, "payment.html", {
                    'fare': totalFare,
                    'tickets': tickets
                })
            else:
                return HttpResponse("User unauthorised")
        else:
            return HttpResponseRedirect(reverse("login"))
    else:
        return HttpResponse("Method must be post.")


