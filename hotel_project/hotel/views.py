from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import Dancer, Group, Schedule
from xml.dom.minidom import Document, parse

def home(request):
    return render(request, 'home.html')

# Отображение всех таблиц
def show_tables(request):
    dancers = Dancer.objects.all()
    groups = Group.objects.all()
    schedules = Schedule.objects.all()
    return render(request, 'show_tables.html', {
        'dancers': dancers,
        'groups': groups,
        'schedules': schedules,
    })

# Экспорт данных в XML
def export_to_xml(request):
    doc = Document()
    dance_school_node = doc.createElement("dance_school")
    doc.appendChild(dance_school_node)

    # Экспорт танцоров
    dancers_node = doc.createElement("dancers")
    dance_school_node.appendChild(dancers_node)
    for dancer in Dancer.objects.all():
        dancer_node = doc.createElement("dancer")
        dancer_node.setAttribute("id", str(dancer.id))

        for field in ["first_name", "last_name", "age", "phone_number", "email", "unique_id"]:
            value = str(getattr(dancer, field) or "")
            field_node = doc.createElement(field)
            field_node.appendChild(doc.createTextNode(value))
            dancer_node.appendChild(field_node)

        dancers_node.appendChild(dancer_node)

    # Экспорт групп
    groups_node = doc.createElement("groups")
    dance_school_node.appendChild(groups_node)
    for group in Group.objects.all():
        group_node = doc.createElement("group")
        group_node.setAttribute("id", str(group.id))

        for field in ["group_name", "dance_style", "status"]:
            value = str(getattr(group, field))
            field_node = doc.createElement(field)
            field_node.appendChild(doc.createTextNode(value))
            group_node.appendChild(field_node)

        groups_node.appendChild(group_node)

    # Экспорт расписаний
    schedules_node = doc.createElement("schedules")
    dance_school_node.appendChild(schedules_node)
    for schedule in Schedule.objects.all():
        schedule_node = doc.createElement("schedule")
        schedule_node.setAttribute("id", str(schedule.id))

        dancer_id_node = doc.createElement("dancer_id")
        dancer_id_node.appendChild(doc.createTextNode(str(schedule.dancer.id)))
        schedule_node.appendChild(dancer_id_node)

        group_id_node = doc.createElement("group_id")
        group_id_node.appendChild(doc.createTextNode(str(schedule.group.id)))
        schedule_node.appendChild(group_id_node)

        for field in ["session_date", "start_time", "end_time"]:
            value = str(getattr(schedule, field))
            field_node = doc.createElement(field)
            field_node.appendChild(doc.createTextNode(value))
            schedule_node.appendChild(field_node)

        schedules_node.appendChild(schedule_node)

    response = HttpResponse(doc.toprettyxml(indent="  "), content_type="application/xml")
    response['Content-Disposition'] = 'attachment; filename="dance_school_data.xml"'
    return response

# Импорт данных из XML
def import_from_xml(request):
    if request.method == "POST":
        xml_file = request.FILES.get("file")
        if not xml_file:
            return JsonResponse({"status": "error", "message": "Файл не был выбран."})

        try:
            Schedule.objects.all().delete()
            Group.objects.all().delete()
            Dancer.objects.all().delete()

            dom = parse(xml_file)
            dance_school_node = dom.documentElement

            for dancer_node in dance_school_node.getElementsByTagName("dancer"):
                Dancer.objects.create(
                    id=dancer_node.getAttribute("id"),
                    first_name=dancer_node.getElementsByTagName("first_name")[0].firstChild.data,
                    last_name=dancer_node.getElementsByTagName("last_name")[0].firstChild.data,
                    age=dancer_node.getElementsByTagName("age")[0].firstChild.data,
                    phone_number=dancer_node.getElementsByTagName("phone_number")[0].firstChild.data or None,
                    email=dancer_node.getElementsByTagName("email")[0].firstChild.data or None,
                    unique_id=dancer_node.getElementsByTagName("unique_id")[0].firstChild.data,
                )

            for group_node in dance_school_node.getElementsByTagName("group"):
                Group.objects.create(
                    id=group_node.getAttribute("id"),
                    group_name=group_node.getElementsByTagName("group_name")[0].firstChild.data,
                    dance_style=group_node.getElementsByTagName("dance_style")[0].firstChild.data,
                    status=group_node.getElementsByTagName("status")[0].firstChild.data,
                )

            for schedule_node in dance_school_node.getElementsByTagName("schedule"):
                Schedule.objects.create(
                    id=schedule_node.getAttribute("id"),
                    dancer=Dancer.objects.get(id=schedule_node.getElementsByTagName("dancer_id")[0].firstChild.data),
                    group=Group.objects.get(id=schedule_node.getElementsByTagName("group_id")[0].firstChild.data),
                    session_date=schedule_node.getElementsByTagName("session_date")[0].firstChild.data,
                    start_time=schedule_node.getElementsByTagName("start_time")[0].firstChild.data,
                    end_time=schedule_node.getElementsByTagName("end_time")[0].firstChild.data,
                )

            return JsonResponse({"status": "success", "message": "Данные успешно импортированы."})

        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Ошибка обработки файла: {e}"})

    if request.method == "GET":
        return render(request, "import_form.html")

# Работа с танцорами
def view_dancers(request):
    dancers = Dancer.objects.all()
    return render(request, 'view_dancers.html', {'dancers': dancers})

def add_dancer(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        age = request.POST['age']
        phone = request.POST.get('phone_number')
        email = request.POST.get('email')
        unique_id = request.POST['unique_id']
        Dancer.objects.create(
            first_name=first_name, last_name=last_name, age=age,
            phone_number=phone, email=email, unique_id=unique_id
        )
        return redirect('home')
    return render(request, 'add_dancer.html')

def edit_dancer(request, dancer_id):
    dancer = get_object_or_404(Dancer, id=dancer_id)
    if request.method == 'POST':
        dancer.first_name = request.POST.get("first_name", dancer.first_name)
        dancer.last_name = request.POST.get("last_name", dancer.last_name)
        dancer.age = request.POST.get("age", dancer.age)
        dancer.phone_number = request.POST.get("phone_number", dancer.phone_number)
        dancer.email = request.POST.get("email", dancer.email)
        dancer.unique_id = request.POST.get("unique_id", dancer.unique_id)
        dancer.save()
        return redirect("view_dancers")

# Работа с группами
def view_groups(request):
    groups = Group.objects.all()
    return render(request, 'view_groups.html', {'groups': groups})

def add_group(request):
    if request.method == 'POST':
        group_name = request.POST['group_name']
        dance_style = request.POST['dance_style']
        status = request.POST['status']
        Group.objects.create(
            group_name=group_name, dance_style=dance_style, status=status
        )
        return redirect('home')
    return render(request, 'add_group.html')

def edit_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        group.group_name = request.POST.get("group_name", group.group_name)
        group.dance_style = request.POST.get("dance_style", group.dance_style)
        group.status = request.POST.get("status", group.status)
        group.save()
        return redirect("view_groups")
    return render(request, 'edit_group.html', {'group': group})


# Работа с расписанием
def view_schedule(request):
    schedules = Schedule.objects.all()
    return render(request, 'view_schedule.html', {'schedules': schedules})

def add_schedule(request):
    if request.method == 'POST':
        dancer = get_object_or_404(Dancer, id=request.POST.get('dancer_id'))
        group = get_object_or_404(Group, id=request.POST.get('group_id'))
        session_date = request.POST.get('session_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        Schedule.objects.create(
            dancer=dancer, group=group,
            session_date=session_date, start_time=start_time, end_time=end_time
        )
        return redirect('view_schedule')
    dancers = Dancer.objects.all()
    groups = Group.objects.all()
    return render(request, 'add_schedule.html', {'dancers': dancers, 'groups': groups})

def edit_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    if request.method == 'POST':
        schedule.dancer = get_object_or_404(Dancer, id=request.POST.get('dancer_id'))
        schedule.group = get_object_or_404(Group, id=request.POST.get('group_id'))
        schedule.session_date = request.POST.get('session_date')
        schedule.start_time = request.POST.get('start_time')
        schedule.end_time = request.POST.get('end_time')
        schedule.save()
        return redirect('view_schedule')
    dancers = Dancer.objects.all()
    groups = Group.objects.all()
    return render(request, 'edit_schedule.html', {'schedule': schedule, 'dancers': dancers, 'groups': groups})
