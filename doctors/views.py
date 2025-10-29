from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from .forms import (AddDoctorForm, AddPhoneForm, AddSpecialtyForm, FindDoctorForm,
                    FindSpecialtyForm)
from .models import Doctor, Phone, Specialty

# Create your views here.


@login_required
def index(request):
    doctors_list = Doctor.objects.order_by('id')
    template = loader.get_template('index.html')
    context = {
        'title': 'Gestão de Médicos Cooperadores da Colih',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'doctors_list': doctors_list,
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('doctors.add_specialty')
def add_specialty(request):
    if request.POST:
        form = AddSpecialtyForm(request.POST)
        item = form
        item.save()
        messages.success(request, 'Registro adicionado com sucesso.')
        return redirect('/specialties/list')
    form = AddSpecialtyForm()
    template = loader.get_template('specialties/add.html')
    context = {
        'title': 'Adicionar Especialidade Médica',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('doctors.change_specialty')
def edit_specialty(request, specialty_id):
    specialty = Specialty.objects.get(id=specialty_id)
    if request.POST:
        form = AddSpecialtyForm(request.POST, instance=specialty)
        item = form
        item.save()
        messages.success(request, 'Registro alterado com sucesso.')
        return redirect('/specialties/list')
    form = AddSpecialtyForm(instance=specialty)
    template = loader.get_template('specialties/edit.html')
    context = {
        'title': 'Editar Especialidade Cadastrada',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def list_specialties(request):
    form = FindSpecialtyForm(request.GET)
    form.fields['name'].required = False
    filter_search = {}
    for key, value in request.GET.items():
        if key in ['name', 'hospital', 'city'] and value:
            filter_search['%s__icontains' % key] = value
    specialties = Specialty.objects.filter(**filter_search)
    template = loader.get_template('specialties/list.html')
    context = {
        'title': 'Relação de Especialidades Médicas',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'specialties': specialties,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('doctors.add_doctor')
def add_doctor(request):
    if request.POST:
        form = AddDoctorForm(request.POST)
        item = form
        item.save()
        messages.success(request, 'Registro adicionado com sucesso.')
        return redirect('/doctors/list')
    form = AddDoctorForm()
    template = loader.get_template('doctors/add.html')
    context = {
        'title': 'Adicionar Médico Cooperador',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def edit_doctor(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    if request.POST:
        if 'number' in request.POST:
            form = AddPhoneForm(request.POST)
            item = form.save(commit=False)
            if not item.number:
                messages.error(request, 'Informe o número de telefone a ser adicionado!')
            else:
                item.doctor = doctor
                item.save()
                messages.success(request, 'Contato telefônico adicionado com sucesso.')
        else:
            form = AddDoctorForm(request.POST, instance=doctor)
            item = form
            item.save()
            messages.success(request, 'Registro alterado com sucesso.')
            return redirect('/doctors/list')
    phones = Phone.objects.filter(doctor=doctor)
    form = AddDoctorForm(instance=doctor)
    phone_form = AddPhoneForm()
    template = loader.get_template('doctors/edit.html')
    context = {
        'title': 'Dados de Médico Cadastrado',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'phones': phones,
        'form': form,
        'doctor_id': doctor_id,
        'phone_form': phone_form,
    }
    return HttpResponse(template.render(context, request))


@login_required
def list_doctors(request):
    form = FindDoctorForm(request.GET)
    form.fields['name'].required = False
    form.fields['specialty'].required = False
    form.fields['hospital'].required = False
    form.fields['city'].required = False
    filter_search = {}
    for key, value in request.GET.items():
        if key in ['name', 'hospital', 'city'] and value:
            filter_search['%s__icontains' % key] = value
        elif key in ['specialty'] and value:
            filter_search[key] = value
    doctors = Doctor.objects.filter(**filter_search)
    template = loader.get_template('doctors/list.html')
    context = {
        'title': 'Relação de Médicos Cooperadores',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'doctors': doctors,
        'form': form,
    }
    return HttpResponse(template.render(context, request))


@login_required
@permission_required('doctors.delete_phone')
def delete_phone(request, doctor_id, phone_id):
    phone = Phone.objects.get(id=phone_id)
    phone.delete()
    messages.success(request, 'Contato telefônico removido com sucesso.')
    return redirect('/doctors/%s/edit/' % doctor_id)


@login_required
def list_phones(request):
    phones = Phone.objects.all()
    print(phones)
    template = loader.get_template('phones/list.html')
    context = {
        'title': 'Contatos telefônicos dos médicos',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'phones': phones,
    }
    return HttpResponse(template.render(context, request))

def detail(request, doctor_id):
    try:
        doctor = Doctor.objects.get(pk=doctor_id)
    except Doctor.DoesNotExist:
        raise Http404("Doctor does not exist")
    context = {
        'title': 'Dados de Médico Cadastrado',
        'username': '%s %s' % (request.user.first_name, request.user.last_name),
        'doctor': '%s - %s' % (doctor.name, doctor.hospital)
    }
    return render(request, 'doctors/detail.html', context)
