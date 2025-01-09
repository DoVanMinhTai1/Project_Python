from datetime import datetime

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
import secrets
from flights.constant import FEE
from flights.models import Flight
from payment.models import Payment, Passenger, Ticket, Seat, TicketSeat, PaymentTicket
from frontend.template import *
from flights import handler
from django.core import serializers

def payment_view(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            request.session.pop('ticket_ids',None)
            tickets = request.POST.get("tickets")
            ticketIds = tickets
            date = None
            if tickets:
                try:
                    ticket_ids = [int(t) for t in tickets.split(',')]
                    tickets = [Ticket.objects.get(id=ticket_id) for ticket_id in ticket_ids]
                    date = tickets[0].booking_date.strftime('%Y-%m-%dT%H:%M:%S')
                except Ticket.DoesNotExist:
                    # Handle the case where a ticket with a given id doesn't exist
                    # For example, you can log the error or return a message
                    tickets = []
                except ValueError:
                    # Handle the case where conversion of id to int fails
                    tickets = []
            else:
                tickets = []
            res = {'tickets': tickets}
            fare = request.POST.get("fare")
            currency = request.POST.get('currency')
            print(fare)
            print(currency)
            cardNumber = request.POST.get('cardNumber')
            cardHolderName = request.POST.get('cardHolderName')
            expMonth = int(request.POST.get('expMonth'))
            expYear = int(request.POST.get('expYear'))
            cvv = request.POST.get('cvv')
            # Lấy ngày tháng năm hiện tại.
            current_year = datetime.today().year
            current_month = datetime.today().month
            if currency == 'VND':
                # Chuyển fare từ dạng chuỗi tiền tệ thành số nguyên
                fare_numeric = float(fare.replace('₫', '').replace(',', '').strip())
                fare = int(fare_numeric)  # Chuyển thành số nguyên
                print(f"Fare after conversion: {fare}")

            try:
                # Kiểm tra số của thẻ có dưới 12 chữ số hay không. Không thì báo lỗi
                payment = Payment.objects.create(
                    fare=fare,
                    card_number=cardNumber,
                    card_holder_name=cardHolderName,
                    expMonth=expMonth,
                    expYear=expYear,
                    cvv=cvv,
                    status='PENDING',
                )
                for ticket in tickets:
                    if ticket.status == 'PENDING':
                        ticket.booking_date = datetime.now()
                        ticket.status = 'CONFIRMED'
                        ticket.save()
                        payment_ticket = PaymentTicket.objects.create(payment=payment, ticket=ticket)
                        payment_ticket.save()
                if tickets[0].status == 'CONFIRMED':
                    payment.status = 'CONFIRMED'
                    payment.save()
                return render(request, 'payment_process.html', res)
            except Exception as e:
                return HttpResponse(e)
    else:
        return HttpResponseRedirect(reverse('login'))


def ticket_data(request, ref):
    try:
        ticket = Ticket.objects.get(ref_no=ref)
        return JsonResponse({
            'ref': ticket.ref_no,
            'from': ticket.flight.origin.code,
            'to': ticket.flight.destination.code,
            'flight_date': ticket.flight_ddate,
            'status': ticket.status
        })
    except Ticket.DoesNotExist:
        return JsonResponse({'error': 'Ticket not found'}, status=404)


def book(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            tripType = request.POST.get('tripType')
            ticket_ids = request.session.get('ticket_ids')
            if ticket_ids:
                total = 0
                ticketIds = ticket_ids.split(',')
                for ticket_id in ticketIds:
                    ticket = Ticket.objects.get(id=int(ticket_id))
                    total += ticket.total_fare
                res = {
                    'fare': total,
                    'tickets': ticket_ids,
                    'tripType': tripType,
                    'date': Ticket.objects.get(id=int(ticketIds[0])).booking_date.strftime('%Y-%m-%dT%H:%M:%S')
                }
                return render(request, 'payment.html', res)
            data = {}
            seat = request.POST.get('seat')
            people = request.POST.get('people')
            if int(request.POST.get('seat_amount')) > 0:
                seatn1 = 'selectedSeat_'
                seats1 = []
                for i in range(1, int(people) + 1):
                    s = Seat.objects.get(id=request.POST.get(seatn1 + str(i)))
                    seats1.append(s)
            if int(request.POST.get('seat_amount1')) > 0:
                seats2 = []
                seatn2 = 'selectedSeat1_'
                for i in range(1, int(people) + 1):
                    s1 = Seat.objects.get(id=request.POST.get(seatn2 + str(i)))
                    seats2.append(s1)
            tripType = request.POST.get('tripType')
            countrycode = request.POST['countryCode']
            mobile = request.POST['mobile']
            email = request.POST['email']
            currency = request.POST['currency']
            print(f"Currency: {currency}")
            discount = request.POST['coupon']
            discountPercentage = float(request.POST['discountPercentage'])
            print(f"discount: {discount}")
            print(f"discount: {discountPercentage}")
            if tripType == '1':
                seat = request.POST.get('seat')
                stop = request.POST.get('stop')
                if stop == 'yes':
                    flight0 = Flight.objects.get(id=request.POST.get('flight.0.id'))
                    flight1 = Flight.objects.get(id=request.POST.get('flight.1.id'))
                    flight0Date = request.POST.get('flight.0.date')
                    flight1Date = request.POST.get('flight.1.date')
                if stop == 'no':
                    flight1 = Flight.objects.get(id=request.POST.get('flight1'))
                    flight_1date = request.POST.get('flight1Date')
                    flight_1class = request.POST.get('flight1Class')
            if tripType == '2':
                stop1 = request.POST.get('stop1')
                stop2 = request.POST.get('stop2')
                if stop1 == 'no':
                    flight1 = Flight.objects.get(id=request.POST.get('flight1'))
                    flight_1date = request.POST.get('flight1Date')
                    flight_1class = request.POST.get('flight1Class')
                if stop1 == 'yes':
                    flight0 = Flight.objects.get(id=request.POST.get('flight.0.id'))
                    flight1 = Flight.objects.get(id=request.POST.get('flight.1.id'))
                    flight0Date = request.POST.get('flight.0.date')
                    flight1Date = request.POST.get('flight.1.date')
                if stop2 == 'no':
                    flight2 = Flight.objects.get(id=request.POST.get('flight2'))
                    flight_2date = request.POST.get('flight2Date')
                    flight_2class = request.POST.get('flight2Class')
                    f2 = True
                if stop2 == 'yes':
                    flight2 = Flight.objects.get(id=request.POST.get('flight.2.id'))
                    flight3 = Flight.objects.get(id=request.POST.get('flight.3.id'))
                    flight2Date = request.POST.get('flight.2.date')
                    flight3Date = request.POST.get('flight.3.date')
                if tripType == '1':
                    mes = {'tripType': '1', 'seat': seat, "fee": FEE, 'people': people, }
                    if stop == 'no':
                        mes.update({
                            'flight1': flight1,
                            "flight1Date": flight_1date,  # Pass it back to the template
                            "flight1Class": flight_1class,
                            'stop': 'no',
                            'seats1': Seat.objects.filter(flight=flight1.pk),
                        })
                    if stop == 'yes':
                        connecting = handler.connecting_flights(flight0.pk, flight1.pk, flight0Date, flight1Date)
                        mes.update({
                            'flight0': connecting.get('flight0'),
                            'flight1': connecting.get('flight1'),
                            'flight0adate': connecting.get('flight0adate'),
                            'flight0ddate': connecting.get('flight0ddate'),
                            "flight1ddate": connecting.get('flight1ddate'),
                            "flight1adate": connecting.get('flight1adate'),
                            'seats1': Seat.objects.filter(flight=connecting.get('flight0').pk),
                            'stop': 'yes', })
                if tripType == '2':
                    mes = {'tripType': '2', 'seat': seat, "fee": FEE, }
                    if stop1 == 'no':
                        mes.update({
                            'flight1': flight1,
                            "flight1Date": flight_1date,  # Pass it back to the template
                            "flight1Class": flight_1class,
                            'stop1': 'no',
                            'seats1': Seat.objects.filter(flight=flight1.pk),
                        })
                    if stop1 == 'yes':
                        connecting = handler.connecting_flights(flight0.pk, flight1.pk, flight0Date, flight1Date)
                        mes.update({
                            'flight0': connecting.get('flight0'),
                            'flight1': connecting.get('flight1'),
                            'flight0adate': connecting.get('flight0adate'),
                            'flight0ddate': connecting.get('flight0ddate'),
                            "flight1ddate": connecting.get('flight1ddate'),
                            "flight1adate": connecting.get('flight1adate'),
                            'seats1': Seat.objects.filter(flight=connecting.get('flight0').pk),
                            'stop1': 'yes', })
                    if stop2 == 'no':
                        mes.update({
                            'flight2': flight2,
                            "flight2Date": flight_2date,
                            "flight2Class": flight_2class,
                            'stop2': 'no',
                            'seats2': Seat.objects.filter(flight=flight2.pk),
                        })
                    if stop2 == 'yes':
                        connecting = handler.connecting_flights(flight2.pk, flight3.pk, flight2Date, flight3Date)
                        mes.update({
                            'flight2': connecting.get('flight0'),
                            'flight3': connecting.get('flight1'),
                            'flight2adate': connecting.get('flight0adate'),
                            'flight2ddate': connecting.get('flight0ddate'),
                            "flight3ddate": connecting.get('flight1ddate'),
                            "flight3adate": connecting.get('flight1adate'),
                            'seats2': Seat.objects.filter(flight=connecting.get('flight0').pk),
                            'stop2': 'yes'
                        })
            if len(mobile) != 10:
                messages.warning(request, 'Mobile must be 10 digits')
                mes = {}
                if tripType == '1':
                    mes = {'tripType': '1', 'seat': seat, "fee": FEE, 'people': people, }
                    if stop == 'no':
                        mes.update({
                            'flight1': flight1,
                            "flight1Date": flight_1date,  # Pass it back to the template
                            "flight1Class": flight_1class,
                            'stop': 'no',
                            'seats1': Seat.objects.filter(flight=flight1.pk),
                        })
                    if stop == 'yes':
                        connecting = handler.connecting_flights(flight0.pk, flight1.pk, flight0Date, flight1Date)
                        mes.update({
                            'flight0': connecting.get('flight0'),
                            'flight1': connecting.get('flight1'),
                            'flight0adate': connecting.get('flight0adate'),
                            'flight0ddate': connecting.get('flight0ddate'),
                            "flight1ddate": connecting.get('flight1ddate'),
                            "flight1adate": connecting.get('flight1adate'),
                            'seats1': Seat.objects.filter(flight=connecting.get('flight0').pk),
                            'stop': 'yes', })
                if tripType == '2':
                    mes = {'tripType': '2', 'seat': seat, "fee": FEE, }
                    if stop1 == 'no':
                        mes.update({
                            'flight1': flight1,
                            "flight1Date": flight_1date,  # Pass it back to the template
                            "flight1Class": flight_1class,
                            'stop1': 'no',
                            'seats1': Seat.objects.filter(flight=flight1.pk),
                        })
                    if stop1 == 'yes':
                        connecting = handler.connecting_flights(flight0.pk, flight1.pk, flight0Date, flight1Date)
                        mes.update({
                            'flight0': connecting.get('flight0'),
                            'flight1': connecting.get('flight1'),
                            'flight0adate': connecting.get('flight0adate'),
                            'flight0ddate': connecting.get('flight0ddate'),
                            "flight1ddate": connecting.get('flight1ddate'),
                            "flight1adate": connecting.get('flight1adate'),
                            'seats1': Seat.objects.filter(flight=connecting.get('flight0').pk),
                            'stop1': 'yes', })
                    if stop2 == 'no':
                        mes.update({
                            'flight2': flight2,
                            "flight2Date": flight_2date,
                            "flight2Class": flight_2class,
                            'stop2': 'no',
                            'seats2': Seat.objects.filter(flight=flight2.pk),
                        })
                    if stop2 == 'yes':
                        connecting = handler.connecting_flights(flight2.pk, flight3.pk, flight2Date, flight3Date)
                        mes.update({
                            'flight2': connecting.get('flight0'),
                            'flight3': connecting.get('flight1'),
                            'flight2adate': connecting.get('flight0adate'),
                            'flight2ddate': connecting.get('flight0ddate'),
                            "flight3ddate": connecting.get('flight1ddate'),
                            "flight3adate": connecting.get('flight1adate'),
                            'seats2': Seat.objects.filter(flight=connecting.get('flight0').pk),
                            'stop2': 'yes'
                        })
                return render(request, 'book.html', mes)
            passengerscount = request.POST['passengersCount']
            passengers = []
            for i in range(1, int(passengerscount) + 1):
                fname = request.POST[f'passenger{i}FName']
                lname = request.POST[f'passenger{i}LName']
                gender = request.POST[f'passenger{i}Gender']
                passengers.append(Passenger.objects.create(first_name=fname, last_name=lname, gender=gender.lower()))
            coupon = discount
            tickets = []
            try:
                if int(request.POST.get('seat_amount')) > 0:
                    if tripType == '1':
                        for s in seats1:
                            if stop == 'yes':
                                tickets.append(
                                    createticket(request.user, passengers, passengerscount, flight0, flight0Date,
                                                 seat, coupon, countrycode, email, mobile, s,discountPercentage))
                                tickets.append(
                                    createticket(request.user, passengers, passengerscount, flight1, flight1Date,
                                                 seat, coupon, countrycode, email, mobile, s,discountPercentage))
                            if stop == 'no':
                                tickets.append(
                                    createticket(request.user, passengers, passengerscount, flight1, flight_1date,
                                                 flight_1class, coupon, countrycode, email, mobile, s,discountPercentage))

                if int(request.POST.get('seat_amount1')) > 0:
                    for s in seats2:
                        if stop1 == 'no':
                            tickets.append(
                                createticket(request.user, passengers, passengerscount, flight1, flight_1date,
                                             flight_1class, coupon, countrycode, email, mobile, s,discountPercentage))
                        if stop1 == 'yes':
                            tickets.append(
                                createticket(request.user, passengers, passengerscount, flight0, flight0Date,
                                             seat, coupon, countrycode, email, mobile, s,discountPercentage))
                            tickets.append(
                                createticket(request.user, passengers, passengerscount, flight1, flight1Date,
                                             seat, coupon, countrycode, email, mobile, s,discountPercentage))
                        if stop2 == 'no':
                            tickets.append(
                                createticket(request.user, passengers, passengerscount, flight2, flight_2date,
                                             flight_2class, coupon, countrycode, email, mobile, s,discountPercentage))
                        if stop2 == 'yes':
                            tickets.append(
                                createticket(request.user, passengers, passengerscount, flight2, flight2Date,
                                             seat, coupon, countrycode, email, mobile, s,discountPercentage))
                            tickets.append(
                                createticket(request.user, passengers, passengerscount, flight3, flight3Date,
                                             seat, coupon, countrycode, email, mobile, s,discountPercentage))

                total_fare = sum([t.total_fare for t in tickets])
                if discountPercentage < 100:
                    total_fare += (FEE * (100 - discountPercentage)/100)
                else:
                    total_fare += FEE
                if currency == 'VND':
                    total_fare *= 24000
                    fare_formatted = "{:,.0f} ₫".format(total_fare)
                print(f"Total Fare after conversion: {total_fare}")
                fare_formatted = int(total_fare)
            except Exception as e:
                return HttpResponse(e)
            ticket_ids = ''
            for ticket in tickets:
                ticket_ids += str(ticket.pk) + ','
            ticket_ids = ticket_ids.rstrip(',')
            request.session['ticket_ids'] = ticket_ids
            res = {
                'currency': currency,
                'fare': fare_formatted,
                'tickets': ticket_ids,
                'tripType': tripType,
                'date': tickets[0].booking_date.strftime('%Y-%m-%dT%H:%M:%S')
            }
            if tripType == '1':
                if stop == 'yes':
                    res.update({'stop': stop, 'flight0': flight0, 'flight1': flight1})
                if stop == 'no':
                    res.update({'stop': stop, 'flight1': flight1})
            if tripType == '2':
                if stop1 == 'yes':
                    res.update({'stop1': stop1, 'flight0': flight0, 'flight1': flight1})
                if stop1 == 'no':
                    res.update({'stop1': stop1, 'flight1': flight1})
                if stop2 == 'yes':
                    res.update({'stop2': stop2, 'flight2': flight2, 'flight3': flight3})
                if stop2 == 'no':
                    res.update({'stop2': stop2, 'flight2': flight2})
        return render(request, "payment.html", res)
    else:
        return HttpResponseRedirect(reverse('login'))

def cancelPayment(request,tickets):
    ticket_ids = tickets.split(',')
    tickets = [Ticket.objects.get(id=int(t)) for t in ticket_ids]
    for ticket in tickets:
        ticket.status = 'CANCELLED'
        ticket.save()
        seats = TicketSeat.objects.filter(ticket=ticket)
        for s in seats:
            seat = Seat.objects.get(pk=s.seat.pk)
            seat.status = 'AVAILABLE'
            seat.save()
    return render(request, "index.html", )

def createticket(user, passengers, passengerscount, flight1, flight_1date, flight_1class, coupon, countrycode, email,
                 mobile, seat,percent):
    coupons = {'FL928K': 0.3, 'FL239D': 0.4, 'FL138S': 0.2}
    ticket = Ticket.objects.create()
    ticket.user = user
    ticket.ref_no = secrets.token_hex(3).upper()
    for passenger in passengers:
        ticket.passengers.add(passenger)
    ticket.flight = flight1
    ticket.flight_ddate = datetime(int(flight_1date.split('-')[2]), int(flight_1date.split('-')[1]),
                                   int(flight_1date.split('-')[0]))
    ###################
    flight1ddate = datetime(int(flight_1date.split('-')[2]), int(flight_1date.split('-')[1]),
                            int(flight_1date.split('-')[0]), flight1.depart_time.hour, flight1.depart_time.minute)
    flight1adate = (flight1ddate + flight1.duration)
    ###################
    ticket.flight_adate = datetime(flight1adate.year, flight1adate.month, flight1adate.day)
    ffre = 0.0
    if flight_1class.lower() == 'first':
        ticket.flight_fare = flight1.first_fare * int(passengerscount)
        ffre = flight1.first_fare * int(passengerscount)
    elif flight_1class.lower() == 'business':
        ticket.flight_fare = flight1.business_fare * int(passengerscount)
        ffre = flight1.business_fare * int(passengerscount)
    else:
        ticket.flight_fare = flight1.economy_fare * int(passengerscount)
        ffre = flight1.economy_fare * int(passengerscount)
    ticket.other_charges = FEE
    ticket.total_fare = ffre  + 0.0 + seat.price
    ##########Total(Including coupon)
    # set status của seat
    seat.status = 'SELECTED'
    seat.save()
    ticket_seat = TicketSeat.objects.create(ticket=ticket, seat=seat)
    ticket_seat.save()
    if coupon:
        if percent < 100:
            ticket.coupon_used = coupon
            ticket.total_fare = round(ticket.total_fare * (100 - percent) / 100, 1)
    ticket.seat_class = flight_1class.lower()
    ticket.status = 'PENDING'
    ticket.mobile = ('+' + countrycode + ' ' + mobile)
    ticket.email = email
    ticket.save()
    return ticket
