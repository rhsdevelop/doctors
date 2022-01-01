from django.db import models

# Create your models here.

class Specialty(models.Model):
    name = models.CharField('Nome', max_length=50)
    register_date = models.DateTimeField('Data do cadastro', auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Doctor(models.Model):
    name = models.CharField('Nome', max_length=100)
    address = models.CharField('Endereço', max_length=100)
    specialty = models.ForeignKey(Specialty, verbose_name='Especialidade', on_delete=models.PROTECT)
    hospital = models.CharField('Hospital', max_length=100, null=True, blank=True)
    city = models.CharField('Cidade', max_length=50)
    crm = models.CharField('CRM', max_length=30, null=True, blank=True)
    status = models.CharField('Situação', max_length=40)
    obs = models.TextField('Observação', null=True, blank=True)
    register_date = models.DateTimeField('Data do cadastro', auto_now_add=True)


class Phone(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Médico')
    number = models.CharField('Número de telefone', max_length=20, null=True, blank=True)
    observation = models.TextField('Observação', null=True, blank=True)