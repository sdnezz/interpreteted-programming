from turtledemo.penrose import start

from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Guest, Room, Booking
from xml.dom.minidom import Document, parse

def show_tables(request):
    guests = Guest.objects.all()
    rooms = Room.objects.all()
    bookings = Booking.objects.all()
    return render(request, 'show_tables.html',{
        'guests': guests,
        'rooms': rooms,
        'bookings': bookings,
    })

def export_to_xml(request):
    doc = Document()

    # Корневой элемент
    hotel_node = doc.createElement("hotel")
    doc.appendChild(hotel_node)

    # Экспорт гостей
    guests_node = doc.createElement("guests")
    hotel_node.appendChild(guests_node)
    for guest in Guest.objects.all():
        guest_node = doc.createElement("guest")
        guest_node.setAttribute("id", str(guest.id))

        for field in ["first_name", "last_name", "phone_number", "email", "passport_number"]:
            value = getattr(guest, field)
            field_node = doc.createElement(field)
            field_node.appendChild(doc.createTextNode(value or ""))
            guest_node.appendChild(field_node)

        guests_node.appendChild(guest_node)

    # Экспорт комнат
    rooms_node = doc.createElement("rooms")
    hotel_node.appendChild(rooms_node)
    for room in Room.objects.all():
        room_node = doc.createElement("room")
        room_node.setAttribute("id", str(room.id))

        for field in ["room_number", "room_type", "price_per_night", "status"]:
            value = str(getattr(room, field))
            field_node = doc.createElement(field)
            field_node.appendChild(doc.createTextNode(value))
            room_node.appendChild(field_node)

        rooms_node.appendChild(room_node)

    # Экспорт бронирований
    bookings_node = doc.createElement("bookings")
    hotel_node.appendChild(bookings_node)
    for booking in Booking.objects.all():
        booking_node = doc.createElement("booking")
        booking_node.setAttribute("id", str(booking.id))

        guest_id_node = doc.createElement("guest_id")
        guest_id_node.appendChild(doc.createTextNode(str(booking.guest.id)))
        booking_node.appendChild(guest_id_node)

        room_id_node = doc.createElement("room_id")
        room_id_node.appendChild(doc.createTextNode(str(booking.room.id)))
        booking_node.appendChild(room_id_node)

        for field in ["start_date", "end_date"]:
            value = str(getattr(booking, field))
            field_node = doc.createElement(field)
            field_node.appendChild(doc.createTextNode(value))
            booking_node.appendChild(field_node)

        bookings_node.appendChild(booking_node)

    response = HttpResponse(doc.toprettyxml(indent="  "), content_type="application/xml")
    response['Content-Disposition'] = 'attachment; filename="hotel_data.xml"'
    return response

# Задание 8: Импорт из XML
def import_from_xml(request):
    if request.method == "POST":
        xml_file = request.FILES.get("file")
        if not xml_file:
            return JsonResponse({"status": "error", "message": "Файл не был выбран."})

        try:
            # Очистка БД
            Booking.objects.all().delete()
            Room.objects.all().delete()
            Guest.objects.all().delete()

            dom = parse(xml_file)
            hotel_node = dom.documentElement

            # Импорт гостей
            for guest_node in hotel_node.getElementsByTagName("guest"):
                Guest.objects.create(
                    id=guest_node.getAttribute("id"),
                    first_name=guest_node.getElementsByTagName("first_name")[0].firstChild.data,
                    last_name=guest_node.getElementsByTagName("last_name")[0].firstChild.data,
                    phone_number=guest_node.getElementsByTagName("phone_number")[0].firstChild.data or None,
                    email=guest_node.getElementsByTagName("email")[0].firstChild.data or None,
                    passport_number=guest_node.getElementsByTagName("passport_number")[0].firstChild.data,
                )

            # Импорт комнат
            for room_node in hotel_node.getElementsByTagName("room"):
                Room.objects.create(
                    id=room_node.getAttribute("id"),
                    room_number=room_node.getElementsByTagName("room_number")[0].firstChild.data,
                    room_type=room_node.getElementsByTagName("room_type")[0].firstChild.data,
                    price_per_night=room_node.getElementsByTagName("price_per_night")[0].firstChild.data,
                    status=room_node.getElementsByTagName("status")[0].firstChild.data,
                )

            # Импорт бронирований
            for booking_node in hotel_node.getElementsByTagName("booking"):
                Booking.objects.create(
                    id=booking_node.getAttribute("id"),
                    guest=Guest.objects.get(id=booking_node.getElementsByTagName("guest_id")[0].firstChild.data),
                    room=Room.objects.get(id=booking_node.getElementsByTagName("room_id")[0].firstChild.data),
                    start_date=booking_node.getElementsByTagName("start_date")[0].firstChild.data,
                    end_date=booking_node.getElementsByTagName("end_date")[0].firstChild.data,
                )

            return JsonResponse({"status": "success", "message": "Данные успешно импортированы."})

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Ошибка обработки файла: {e}"})

    # Обработка GET-запроса (возврат страницы с формой загрузки)
    if request.method == "GET":
        return render(request, "import_form.html")

def home(request):
    return render(request, 'home.html')

def view_rooms(request):
    rooms = Room.objects.all()
    return render(request, 'view_rooms.html', {'rooms': rooms})

def view_guests(request):
    guests = Guest.objects.all()
    return render(request, 'view_guests.html', {'guests': guests})

def add_guest(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST.get('phone_number')
        email = request.POST.get('email')
        passport = request.POST['passport_number']
        Guest.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone,
            email=email,
            passport_number=passport
        )
        return redirect('home')
    return render(request, 'add_guest.html')

def edit_guest(request, guest_id):
    guest = get_object_or_404(Guest, id = guest_id)
    if request.method == 'POST':
        guest.first_name = request.POST.get("first_name", guest.first_name)
        guest.last_name = request.POST.get("last_name", guest.last_name)
        guest.phone = request.POST.get("phone_number", guest.phone_number)
        guest.email = request.POST.get("email", guest.email)
        guest.passport = request.POST.get("passport_number", guest.passport_number)
        guest.save()
    return redirect("view_guests")

def view_bookings(request):
    bookings = Booking.objects.all()
    return render(request, 'view_bookings.html', {'bookings': bookings})

def add_booking(request):
    if request.method == 'POST':
        guest = get_object_or_404(Guest, id=request.POST.get('guest_id'))
        room = get_object_or_404(Room, id=request.POST.get('room_id'))
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        Booking.objects.create(
            guest=guest, room=room,
            check_in_date=check_in_date, check_out_date=check_out_date
        )
        return redirect('view_bookings')
    guests = Guest.objects.all()
    rooms = Room.objects.all()
    return render(request, 'add_booking.html', {'guests': guests, 'rooms': rooms})

def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.guest = get_object_or_404(Guest, id=request.POST.get('guest_id'))
        booking.room = get_object_or_404(Room, id=request.POST.get('room_id'))
        booking.check_in_date = request.POST.get('check_in_date')
        booking.check_out_date = request.POST.get('check_out_date')
        booking.save()
        return redirect('view_bookings')
    guests = Guest.objects.all()
    rooms = Room.objects.all()
    return render(request, 'edit_booking.html', {'booking': booking, 'guests': guests, 'rooms': rooms})

def add_room(request):
    if request.method == 'POST':
        room_number = request.POST['room_number']
        room_type = request.POST['room_type']
        price_per_night = request.POST['price_per_night']
        status = request.POST['status']
        Room.objects.create(
            room_number = room_number,
            room_type = room_type,
            price_per_night = price_per_night,
            status = status
        )
        return redirect('home')
    return render(request, 'add_room.html')

def edit_room(request, room_id):
    room = get_object_or_404(Room, id = room_id)
    if request.method == 'POST':
        room.room_type = request.POST.get("room_type", room.room_type)
        room.price_per_night = request.POST.get("price_per_night", room.price_per_night)
        room.status = request.POST.get("status", room.status)
        room.save()
    return redirect("view_rooms")
