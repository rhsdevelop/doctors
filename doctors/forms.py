from django import forms
from .models import Doctor, Phone, Specialty
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, HTML, ButtonHolder, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField  # opcional, para floating labels


class AddSpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        exclude = ['id', 'register_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.include_media = True  # garante assets quando necessário

        # Exemplo com grid Bootstrap 5 + FloatingField (opcional)
        self.helper.layout = Layout(
            Fieldset(
                "Dados da especialidade",
                Row(
                    Column("name", css_class="col-md-6"),
                ),
            ),
            ButtonHolder(
                Submit("submit", "Salvar", css_class="btn btn-primary")
            ),
        )


class FindSpecialtyForm(forms.ModelForm):
    class Meta:
        model = Specialty
        fields = ['name']


class AddDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        exclude = ['id',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.include_media = True  # garante assets quando necessário

        # Exemplo com grid Bootstrap 5 + FloatingField (opcional)
        self.helper.layout = Layout(
            Fieldset(
                "Dados do médico",
                Row(
                    Column("name", css_class="col-md-6"),
                    Column("crm", css_class="col-md-6"),
                ),
                Row(
                    Column("specialty", css_class="col-md-6"),
                    Column("status", css_class="col-md-6"),
                ),
                Row(
                    Column("hospital", css_class="col-md-6"),
                    Column("city", css_class="col-md-6"),
                ),
                "address",
                # Exemplo de FloatingField (se quiser floating labels):
                # FloatingField("name"),
                "obs",
            ),
            ButtonHolder(
                Submit("submit", "Salvar", css_class="btn btn-primary")
            ),
        )


class FindDoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'specialty', 'hospital', 'city']


class AddPhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude = ['id', 'doctor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = True
        self.helper.include_media = True  # garante assets quando necessário

        # Exemplo com grid Bootstrap 5 + FloatingField (opcional)
        self.helper.layout = Layout(
            Fieldset(
                "Adicionar número",
                Row(
                    Column("number", css_class="col-md-12"),
                    Column("observation", css_class="col-md-12"),
                ),
            ),
            ButtonHolder(
                Submit("submit", "Inserir", css_class="btn btn-primary")
            ),
        )
