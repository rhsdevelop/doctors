import django.contrib.auth.views
from django.urls import path

from . import views 

app_name = 'doctors'
urlpatterns = [
    path('', views.index, name='index'),
    path('config/email/', views.configure_email, name='configure_email'),
    path('config/email/testar/', views.testar_smtp, name='testar_smtp'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/list/', views.list_doctors, name='list_doctors'),
    path('doctors/<int:doctor_id>/edit/', views.edit_doctor, name='edit_doctor'),
    path('doctors/<int:doctor_id>/phone/<int:phone_id>/delete/', views.delete_phone, name='delete_phone'),
    path('doctors/export/xlsx/', views.export_doctors_xlsx, name='export_doctors_xlsx'),
    path('specialties/add/', views.add_specialty, name='add_specialties'),
    path('specialties/list/', views.list_specialties, name='list_specialties'),
    path('specialties/<int:specialty_id>/edit/', views.edit_specialty, name='edit_specialty'),
    path('phones/list/', views.list_phones, name='list_phones'),
    path('visits/add/', views.add_visit, name='add_visit'),
    path('visits/list/', views.list_visits, name='list_visits'),
    path('visits/<int:visit_id>/edit/', views.edit_visit, name='edit_visit'),
    path('visits/<int:visit_id>/delete/', views.delete_visit, name='delete_visit'),
    path('emergencia/add/', views.add_planilha_emergencia, name='add_planilha_emergencia'),
    path('emergencia/list/', views.list_planilhas, name='list_planilha_emergencia'),
    path('emergencia/<int:planilha_id>/edit/', views.edit_planilha_emergencia, name='edit_planilha_emergencia'),
    path('emergencia/<int:planilha_id>/submeter-gvp/', views.submeter_para_gvp, name='submeter_para_gvp'),
    path('emergencia/<int:planilha_id>/boletim/', views.gerar_boletim_whatsapp, name='gerar_boletim'),
    path('gvp/acompanhamentos/', views.list_gvp_active_cases, name='list_gvp_plan'),
    path('gvp/register/', views.add_gvp_visit, name='add_gvp_visit'),
    path('gvp/<int:planilha_id>/register/', views.add_gvp_visit, name='add_gvp_visit_direct'),
    #path('<int:doctor_id>/results/', views.results, name='results'),
    #path('<int:doctor_id>/vote/', views.vote, name='vote'),
]
