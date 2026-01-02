import datetime
from django import forms
from django.contrib.auth.models import User
from django.utils import timezone
from .models import EmailConfiguration, MembroGvp, Hospital, Doctor, Phone, Specialty, Visit, PlanilhaEmergencia, GvpVisit
from crispy_forms.bootstrap import TabHolder, Tab
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, HTML, ButtonHolder, Submit
from crispy_bootstrap5.bootstrap5 import FloatingField  # opcional, para floating labels


class EmailConfigForm(forms.ModelForm):
    class Meta:
        model = EmailConfiguration
        fields = '__all__'
        widgets = {
            'email_password': forms.PasswordInput(render_value=True),
        }


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
        exclude = ['id', 'register_date'] # Excluímos id e data de cadastro automática
        
        # Isto transforma o campo de texto simples num calendário HTML5
        widgets = {
            'last_visit': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = True

        self.helper.layout = Layout(
            Fieldset(
                "Dados Principais",
                Row(
                    Column("name", css_class="col-md-6"),
                    Column("email", css_class="col-md-6"),
                ),
                Row(
                    Column("crm", css_class="col-md-4"),
                    Column("user", css_class="col-md-4"), # Campo do Usuário (COLIH)
                    Column("status", css_class="col-md-4"),
                ),
            ),
            
            Fieldset(
                "Localização",
                Row(
                    Column("hospital", css_class="col-md-6"),
                    Column("city", css_class="col-md-6"),
                ),
                "address",
            ),

            Fieldset(
                "Especialidades",
                Row(
                    Column("specialty", css_class="col-md-4"),
                    Column("specialty2", css_class="col-md-4"),
                    Column("specialty3", css_class="col-md-4"),
                ),
                "subspecialty",
            ),

            Fieldset(
                "Detalhes do Atendimento",
                Row(
                    Column("type_patient", css_class="col-md-6"),
                    Column("last_visit", css_class="col-md-6"), # Calendário
                ),
                Row(
                    Column("attends_sus", css_class="col-md-2"),       # Ajustei largura
                    Column("attends_private", css_class="col-md-2"),   # <--- NOVO NO FORM
                    Column("performs_surgeries", css_class="col-md-2"),
                    Column("is_jehovah_witness", css_class="col-md-3"),
                    Column("is_hid_consultant", css_class="col-md-3"),
                    css_class="mb-3 mt-3" 
                ),                
                "obs",
            ),
            ButtonHolder(
                Submit("submit", "Salvar Médico", css_class="btn btn-primary")
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


class FindVisitForm(forms.ModelForm):
    # Campo extra para digitar o nome do médico (pesquisa flexível)
    doctor_name = forms.CharField(label="Nome do Médico", required=False)

    class Meta:
        model = Visit
        fields = ['visit_type', 'specialty'] # Filtros baseados no Model


class AddVisitForm(forms.ModelForm):
    class Meta:
        model = Visit
        exclude = ['id', 'created_at'] # A data de lançamento é automática
        
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'outcome': forms.Textarea(attrs={'rows': 3}), # Caixa de texto menor (3 linhas)
            'members': forms.CheckboxSelectMultiple(), # Mostra lista com caixinhas para marcar
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_tag = True

        self.helper.layout = Layout(
            Fieldset(
                "Dados Principais",
                Row(
                    Column("doctor", css_class="col-md-6"),
                    Column("visit_date", css_class="col-md-6"),
                ),
                Row(
                    Column("visit_type", css_class="col-md-4"),
                    Column("specialty", css_class="col-md-4"),
                    Column("hospital", css_class="col-md-4"),
                ),
            ),
            
            Fieldset(
                "Conteúdo da Visita",
                "article",
                "outcome",
            ),

            Fieldset(
                "Quem realizou a visita?",
                "members", # Aqui aparecerão os checkboxes com os nomes dos usuários
            ),

            ButtonHolder(
                Submit("submit", "Registrar Visita", css_class="btn btn-primary")
            ),
        )


class PlanilhaEmergenciaForm(forms.ModelForm):
    class Meta:
        model = PlanilhaEmergencia
        exclude = ['created_at', 'updated_at']
        
        # Widgets para garantir que apareça o calendário e o relógio nos navegadores
        widgets = {
            'data_hora_contato': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'  # Garante que o Django formate corretamente ao editar
            ),
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'membros_colih': forms.Textarea(attrs={'rows': 2}),
            'anciaos_contatados': forms.Textarea(attrs={'rows': 2}),
            'comentarios_espirituais': forms.Textarea(attrs={'rows': 3}),
            'problema_especifico': forms.Textarea(attrs={'rows': 3}),
            'historico_saude': forms.Textarea(attrs={'rows': 3}),
            'plano_tratamento': forms.Textarea(attrs={'rows': 3}),
            'estrategias_opcoes': forms.Textarea(attrs={'rows': 3}),
            'artigos_fornecidos': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.initial.get('data_hora_contato'):
            # O formato deve ser exato para o input datetime-local funcionar
            self.initial['data_hora_contato'] = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M')
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True
        
        # Organização em ABAS para facilitar o preenchimento
        self.helper.layout = Layout(
            TabHolder(
                # ABA 1: Notificação e Paciente
                Tab('1. Inicial & Paciente',
                    Fieldset("Dados da Notificação",
                        Row(
                            Column('data_hora_contato', css_class='col-md-4'),
                            Column('nome_telefonou', css_class='col-md-4'),
                            Column('contato_telefonou', css_class='col-md-4'),
                        ),
                        Row(
                            Column('parentesco', css_class='col-md-4'),
                            Column('membros_colih', css_class='col-md-8'),
                        ),
                        'paciente_solicitou_ajuda',
                    ),
                    Fieldset("Dados do Paciente",
                        Row(
                            Column('nome_paciente', css_class='col-md-6'),
                            Column('sexo', css_class='col-md-3'),
                            Column('idade', css_class='col-md-3'),
                        ),
                        Row(
                            Column('batizado', css_class='col-md-4'),
                            Column('boa_condicao_espiritual', css_class='col-md-4'),
                            Column('cartao_diretivas', css_class='col-md-4'),
                        ),
                    ),
                    css_id='aba-inicial',  # ID manual (começa com letra)
                ),

                # ABA 2: Hospital e Contatos
                Tab('2. Hospital & Espiritual',
                    Fieldset("Localização e Convênio",
                        Row(
                            Column('nome_hospital', css_class='col-md-6'),
                            Column('tipo_atendimento', css_class='col-md-3'),
                            Column('plano_saude', css_class='col-md-3'),
                        ),
                        Row(
                            Column('numero_quarto', css_class='col-md-6'),
                            Column('telefone_hospital', css_class='col-md-6'),
                        ),
                    ),
                    Fieldset("Suporte Espiritual",
                        'congregacao',
                        'anciaos_contatados',
                        'comentarios_espirituais',
                    ),
                    css_id='aba-hospital' # <--- ID manual
                ),

                # ABA 3: Menores (Opcional)
                Tab('3. Menores/Recém-Nascido',
                    Row(
                        Column('nome_pai', css_class='col-md-6'),
                        Column('pai_batizado', css_class='col-md-6'),
                    ),
                    Row(
                        Column('nome_mae', css_class='col-md-6'),
                        Column('mae_batizada', css_class='col-md-6'),
                    ),
                    Row(
                        Column('data_nascimento', css_class='col-md-3'),
                        Column('peso_nascer', css_class='col-md-3'),
                        Column('apgar', css_class='col-md-3'),
                        Column('idade_gestacional', css_class='col-md-3'),
                    ),
                    'documento_s55_considerado',
                    css_id='aba-menores' # <--- ID manual
                ),

                # ABA 4: Dados Médicos
                Tab('4. Quadro Clínico',
                    'problema_especifico',
                    'historico_saude',
                    Fieldset("Equipe Médica",
                        Row(
                            Column('medico_responsavel', css_class='col-md-6'),
                            Column('especialidade_responsavel', css_class='col-md-6'),
                        ),
                        Row(
                            Column('outro_medico', css_class='col-md-6'),
                            Column('especialidade_outro', css_class='col-md-6'),
                        ),
                        'plano_tratamento',
                        Row(
                            Column('equipe_informada_colih', css_class='col-md-4'),
                            Column('equipe_cooperando', css_class='col-md-4'),
                            Column('acao_judicial_mencionada', css_class='col-md-4'),
                        ),
                    ),
                    css_id='aba-clinico' # <--- ID manual
                ),

                # ABA 5: Estratégias e Consultoria
                Tab('5. Estratégias & Transferência',
                    'estrategias_opcoes',
                    'artigos_fornecidos',
                    'medico_cooperativo_apos_artigos',
                    
                    Fieldset("Consultoria e Transferência",
                        Row(
                            Column('medico_consultor', css_class='col-md-6'),
                            Column('especialidade_consultor', css_class='col-md-6'),
                        ),
                        'infos_consultor',
                        Row(
                            Column('necessidade_transferencia', css_class='col-md-6'),
                            Column('procedimentos_transferencia_confirmados', css_class='col-md-6'),
                        ),
                        Row(
                            Column('hospital_destino', css_class='col-md-6'),
                            Column('colih_destino_informada', css_class='col-md-6'),
                        ),
                        Row(
                            Column('medico_destino', css_class='col-md-6'),
                            Column('telefone_destino', css_class='col-md-6'),
                        ),
                    ),
                    css_id='aba-estrategias' # <--- ID manual
                ),

                # ABA 6: Desfecho
                Tab('6. Resultado',
                    'resultado_acompanhamento',
                    'anciaos_locais_acompanhamento',
                    css_id='aba-resultado' # <--- ID manual
                )
            ),
            
            # Botões de Ação
            ButtonHolder(
                Submit('submit', 'Salvar Planilha de Emergência', css_class='btn btn-success mt-3'),
                Submit('cancel', 'Cancelar', css_class='btn btn-secondary mt-3', formaction="/emergencia/list/") # Ajuste a rota de cancelar conforme necessário
            )
        )


class FindPlanilhaForm(forms.ModelForm):
    # Campo de busca livre para nome
    nome_paciente = forms.CharField(label="Nome do Paciente", required=False)

    class Meta:
        model = PlanilhaEmergencia
        fields = ['nome_hospital'] # O hospital será um dropdown automático
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove a obrigatoriedade do hospital para permitir buscar todos
        self.fields['nome_hospital'].required = False
        self.fields['nome_hospital'].label = "Filtrar por Hospital"


class FilterGvpStatusForm(forms.Form):
    nome_paciente = forms.CharField(label="Nome do Paciente", required=False)
    status_gvp = forms.ChoiceField(
        label="Situação",
        required=False,
        choices=[('', 'Todos (Andamento/Finalizado)'), ('AND', 'Em Acompanhamento'), ('FIN', 'Finalizado')]
    )
    hospital = forms.ModelChoiceField(
        queryset=Hospital.objects.all(), 
        required=False, 
        label="Hospital"
    )


class GvpVisitForm(forms.ModelForm):
    # Campo extra que não está no model GvpVisit, mas serve para controlar a Planilha
    finalizar_caso = forms.BooleanField(
        required=False, 
        label="Finalizar Caso?", 
        help_text="Marque esta opção se o acompanhamento GVP foi concluído."
    )

    class Meta:
        model = GvpVisit
        fields = ['planilha', 'designated_members', 'status_patient', 'action_taken', 'finalizar_caso']
        widgets = {
            'designated_members': forms.CheckboxSelectMultiple(),
            'action_taken': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Se você quiser que o GVP só veja planilhas de emergências ativas, 
        # pode filtrar aqui:
        # self.fields['planilha'].queryset = PlanilhaEmergencia.objects.all().order_by('-created_at')

        # Filtra para que apenas Usuários vinculados ao MembroGvp apareçam
        # Usamos o 'user_id' para buscar no modelo User os IDs presentes em MembroGvp
        membros_ids = MembroGvp.objects.filter(ativo=True).values_list('user_id', flat=True)
        print(membros_ids)
        self.fields['designated_members'].queryset = User.objects.filter(id__in=membros_ids)
        # Estilização opcional para facilitar seleção
        #self.fields['designated_members'].widget = forms.CheckboxSelectMultiple()

        # Inicializamos o Helper        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = True

        # Lógica de bloqueio
        bloquear = False
        if self.instance and self.instance.pk:
            # Se a planilha vinculada estiver finalizada
            if self.instance.planilha.status_gvp == 'FIN':
                # E se o usuário pertencer ao grupo operacional
                if self.user and self.user.groups.filter(name='GVP - Operacional').exists():
                    bloquear = True

        # Definimos o Layout
        self.helper.layout = Layout(
            Fieldset(
                "Vínculo e Status",
                Row(
                    # A planilha ocupa a maior parte, status a menor
                    Column('planilha', css_class='col-md-4'),
                    Column('status_patient', css_class='col-md-8'),
                ),
            ),
            
            Fieldset(
                "Equipe GVP",
                # Colocamos os membros em uma linha própria
                Row(
                    Column('designated_members', css_class='col-md-12'),
                ),
                css_class="mb-3"
            ),
            
            Fieldset(
                "Registro da Atuação",
                'action_taken',
            ),

            Fieldset(
                "Encerramento",
                # Adicionamos o novo campo com um destaque visual (CSS)
                Row(
                    Column(HTML('<div class="alert alert-warning mb-0">'), css_class='col-md-12'),
                    Column('finalizar_caso', css_class='col-md-11'),
                )
            ),
        )
        if bloquear:
            # 1. Desabilita todos os campos
            for field in self.fields:
                self.fields[field].disabled = True
            
            # 2. Adiciona um aviso visual e remove o botão de submit
            self.helper.layout.append(
                HTML('<div class="alert alert-warning mt-3"><strong>Atenção:</strong> Este caso foi finalizado e o registro não pode mais ser editado.</div>')
            )
        else:
            # 3. Caso contrário, adiciona o botão normalmente
            self.helper.layout.append(
                ButtonHolder(
                    Submit('submit', 'Registrar Atuação GVP', css_class='btn btn-primary btn-block')
                )
            )

        # Opcional: Personalizar o rótulo da planilha para ser mais claro
        self.fields['planilha'].label = "Selecione o Paciente (Planilha de Emergência)"