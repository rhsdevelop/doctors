from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

PATIENT_TYPE_CHOICES = (
    ('Pediátrico', 'Pediátrico'),
    ('Adulto', 'Adulto'),
    ('Ambos', 'Ambos'),
)
STATUS_GVP_CHOICES = [
    ('PEN', 'Pendente'),
    ('AND', 'Em Acompanhamento'),
    ('FIN', 'Finalizado'),
]


class EmailConfiguration(models.Model):
    # Identificador simples para a configuração
    nome_config = models.CharField(max_length=50, default="Padrao", verbose_name="Nome da Configuração")
    
    # SMTP (Envio)
    smtp_server = models.CharField(max_length=255, verbose_name="Servidor SMTP (Ex: smtp.gmail.com)")
    smtp_port = models.IntegerField(default=587, verbose_name="Porta SMTP")
    use_tls = models.BooleanField(default=True, verbose_name="Usar TLS?")
    
    # Credenciais
    email_user = models.EmailField(verbose_name="E-mail de Origem (Usuário)")
    email_password = models.CharField(max_length=255, verbose_name="Senha do E-mail")
    
    # IMAP (Recebimento - Opcional para futuras funções)
    imap_server = models.CharField(max_length=255, blank=True, null=True, verbose_name="Servidor IMAP")

    class Meta:
        verbose_name = "Configuração de E-mail"
        verbose_name_plural = "Configurações de E-mail"

    def __str__(self):
        return f"Servidor: {self.smtp_server} ({self.email_user})"

class MembroColih(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário", related_name='perfil_colih')
    ativo = models.BooleanField(default=True, verbose_name="Ativo")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def total_visitas_recentes(self):
        """
        Calcula o total de visitas a MÉDICOS/HOSPITAIS (Model Visit) 
        que este usuário realizou nos últimos 30 dias.
        """
        trinta_dias_atras = timezone.now() - timedelta(days=30)
        from .models import Visit
        # Filtramos as visitas (Visit) onde este usuário é o autor/visitante
        # Ajuste o campo 'user' se o nome no seu model Visit for diferente (ex: 'membro')
        return Visit.objects.filter(
            members=self.user, 
            visit_date__gte=trinta_dias_atras
        ).count()
    
    class Meta:
        verbose_name = "Membro da COLIH"
        verbose_name_plural = "Membros da COLIH"

class MembroGvp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def total_visitas_recentes(self):
        """
        Calcula o total de visitas que este usuário realizou nos últimos 30 dias.
        Útil para o Admin e para a lógica de escala.
        """
        trinta_dias_atras = timezone.now() - timedelta(days=30)
        from .models import GvpVisit
        # Filtramos as visitas onde este usuário específico está na lista de membros designados
        return GvpVisit.objects.filter(
            designated_members=self.user, 
            submission_date__gte=trinta_dias_atras
        ).count()
    
    class Meta:
        verbose_name = "Membro do GVP"
        verbose_name_plural = "Membros do GVP"

# 1. Modelo para Cidades (Padronização)
class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Cidade")
    uf = models.CharField(max_length=2, verbose_name="UF")

    class Meta:
        verbose_name = "Cidade"
        verbose_name_plural = "Cidades"
        ordering = ['name']

    def __str__(self):
        return self.name

# 2. Modelo para Hospitais (Padronização)
class Hospital(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Hospital")
    city = models.ForeignKey(City, on_delete=models.PROTECT, verbose_name="Cidade")
    address = models.CharField(max_length=200, verbose_name="Endereço", null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name="Telefone", null=True, blank=True)
    register_date = models.DateTimeField('Data do cadastro', auto_now_add=True)
    observation = models.TextField('Observação', null=True, blank=True)

    class Meta:
        verbose_name = "Hospital"
        verbose_name_plural = "Hospitais"
        ordering = ['name']

    def __str__(self):
        return self.name

class Specialty(models.Model):
    name = models.CharField('Nome', max_length=100)
    register_date = models.DateTimeField('Data do cadastro', auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Doctor(models.Model):
    name = models.CharField('Nome', max_length=100)
    # Alterado de CharField para ForeignKey
    city = models.ForeignKey(
        City, 
        on_delete=models.PROTECT, 
        verbose_name="Cidade",
        blank=True, 
        null=True
    )
    # Alterado de CharField para ForeignKey
    hospital = models.ForeignKey(
        Hospital, 
        on_delete=models.PROTECT, 
        verbose_name="Hospital",
        blank=True, 
        null=True
    )
    address = models.CharField('Endereço', max_length=100)
    email = models.EmailField('E-mail', null=True, blank=True)
    specialty = models.ForeignKey(Specialty, verbose_name='Especialidade 1', on_delete=models.PROTECT, related_name='doctors_primary')
    specialty2 = models.ForeignKey(Specialty, verbose_name='Especialidade 2', on_delete=models.PROTECT, related_name='doctors_secondary', blank=True, null=True)
    specialty3 = models.ForeignKey(Specialty, verbose_name='Especialidade 3', on_delete=models.PROTECT, related_name='doctors_tertiary', blank=True, null=True)
    subspecialty = models.CharField('Subespecialidade', max_length=30, null=True, blank=True)
    crm = models.CharField('CRM', max_length=80, null=True, blank=True)
    type_patient = models.CharField(
        'Tipo de paciente', 
        max_length=40, 
        choices=PATIENT_TYPE_CHOICES,
        default='Adulto' # É bom ter um padrão para facilitar
    )
    status = models.CharField('Situação', max_length=40)
    # --- NOVOS CAMPOS ADICIONADOS AQUI ---
    attends_sus = models.BooleanField('Atende SUS?', default=False)
    attends_private = models.BooleanField('Atende particular?', default=False) # <--- NOVO CAMPO
    performs_surgeries = models.BooleanField('Faz cirurgias?', default=False)
    # null=True, blank=True pois pode ser um médico novo que ainda não foi visitado
    last_visit = models.DateField('Data da última visita', null=True, blank=True) 
    is_jehovah_witness = models.BooleanField('É Testemunha de Jeová?', default=False)
    is_hid_consultant = models.BooleanField('É Consultor informado ao HID?', default=False)
    # -------------------------------------    
    obs = models.TextField('Observação', null=True, blank=True)
    user = models.ForeignKey(
        User, 
        verbose_name='Usuário (COLIH)', 
        on_delete=models.PROTECT, # Impede apagar o usuário se ele tiver médicos
        null=True,  # Permite que o campo fique vazio (caso ninguém visite ainda)
        blank=True
    )    
    register_date = models.DateTimeField('Data do cadastro', auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class Phone(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='Médico')
    number = models.CharField('Número de telefone', max_length=20, null=True, blank=True)
    observation = models.TextField('Observação', null=True, blank=True)

class Visit(models.Model):
    # Opções de Tipo de Visita
    VISIT_TYPE_CHOICES = (
        ('Preventiva', 'Preventiva'),
        ('Apresentacao', 'Apresentação de Artigo'), # Nome sugerido
        ('Intervencao', 'Intervenção'),
    )

    # 1. Quem foi visitado?
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        verbose_name='Médico'
    )

    # 2. Qual o tipo da visita?
    visit_type = models.CharField(
        'Tipo de Visita', 
        max_length=20, 
        choices=VISIT_TYPE_CHOICES,
        default='Preventiva'
    )

    # 3. Local da visita (Vinculado aos hospitais cadastrados)
    # Se a visita for fora de um hospital cadastrado, pode deixar em branco.
    hospital = models.ForeignKey(
        Hospital, 
        on_delete=models.SET_NULL, # Se apagar o hospital, mantém o histórico da visita
        verbose_name='Local da Visita (Hospital)',
        null=True, 
        blank=True
    )
    
    # 4. Qual artigo/assunto?
    article = models.CharField('Artigo Apresentado / Assunto', max_length=200, null=True, blank=True)

    # 5. Especialidade focada na visita
    specialty = models.ForeignKey(
        Specialty, 
        on_delete=models.PROTECT, 
        verbose_name='Especialidade Abordada'
    )

    # 6. Datas
    visit_date = models.DateField('Data da Visita') # Data manual (quando ocorreu)
    created_at = models.DateTimeField('Data do Lançamento', auto_now_add=True) # Automático (sistema)

    # 7. Quem realizou a visita? (ManyToManyField é o ideal aqui)
    members = models.ManyToManyField(
        User, 
        verbose_name='Membros Visitantes',
        related_name='visits' 
    )

    # Campo extra para anotações do resultado da visita
    outcome = models.TextField('Desfecho / Resultado', null=True, blank=True)

    class Meta:
        verbose_name = "Visita"
        verbose_name_plural = "Visitas"
        ordering = ['-visit_date'] # Ordena da mais recente para a mais antiga

    def __str__(self):
        return f"{self.get_visit_type_display()} - {self.doctor.name} ({self.visit_date})"

class PlanilhaEmergencia(models.Model):
    # --- Choices ---
    SEXO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ]
    
    TIPO_ATENDIMENTO_CHOICES = [
        ('PAR', 'Particular'),
        ('PUB', 'Público'),
    ]

    # --- 1. Notificação ---
    data_hora_contato = models.DateTimeField(verbose_name="Data/hora do contato")
    nome_telefonou = models.CharField(max_length=150, verbose_name="Nome da pessoa que telefonou")
    contato_telefonou = models.CharField(max_length=100, verbose_name="Contato da pessoa que telefonou")
    paciente_solicitou_ajuda = models.BooleanField(default=False, verbose_name="Paciente solicitou ajuda da Colih?")
    parentesco = models.CharField(max_length=100, verbose_name="Parentesco com o paciente")
    membros_colih = models.TextField(verbose_name="Membros da Colih envolvidos")

    # --- 2. Informações do Paciente e Hospital ---
    nome_paciente = models.CharField(max_length=200, verbose_name="Nome do paciente")
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name="Sexo")
    idade = models.CharField(max_length=50, verbose_name="Idade") # CharField para aceitar "2 meses", "45 anos"
    
    # Status Espiritual/Legal
    batizado = models.BooleanField(default=False, verbose_name="Batizado?")
    boa_condicao_espiritual = models.BooleanField(default=True, verbose_name="Boa condição espiritual?")
    cartao_diretivas = models.BooleanField(default=False, verbose_name="Cartão de Diretivas completo?")
    
    # Dados Hospitalares
    tipo_atendimento = models.CharField(max_length=3, choices=TIPO_ATENDIMENTO_CHOICES, verbose_name="Tipo de atendimento")
    plano_saude = models.CharField(max_length=150, blank=True, null=True, verbose_name="Plano de saúde e abrangência")
    nome_hospital = models.ForeignKey(
        Hospital, 
        on_delete=models.SET_NULL, # Se apagar o hospital, mantém a planilha mas com campo vazio
        verbose_name="Nome do Hospital",
        null=True, 
        blank=True
    )
    numero_quarto = models.CharField(max_length=50, blank=True, null=True, verbose_name="N.º do quarto")
    telefone_hospital = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telefone do hospital/quarto")
    
    # Contatos Religiosos
    congregacao = models.CharField(max_length=150, verbose_name="Congregação (Nome, Cidade, UF)")
    anciaos_contatados = models.TextField(verbose_name="Nomes e telefones dos anciãos contatados")
    comentarios_espirituais = models.TextField(blank=True, null=True, verbose_name="Comentários (condição espiritual, etc.)")

    # --- 3. Menores de Idade ou Recém-nascidos (Campos Opcionais) ---
    nome_pai = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nome completo do pai")
    pai_batizado = models.BooleanField(default=False, verbose_name="Pai batizado?")
    nome_mae = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nome completo da mãe")
    mae_batizada = models.BooleanField(default=False, verbose_name="Mãe batizada?")
    
    peso_nascer = models.CharField(max_length=50, blank=True, null=True, verbose_name="Peso ao nascer")
    apgar = models.CharField(max_length=50, blank=True, null=True, verbose_name="Pontuação APGAR (5 min)")
    idade_gestacional = models.CharField(max_length=50, blank=True, null=True, verbose_name="Idade gestacional")
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de nascimento")
    documento_s55_considerado = models.BooleanField(default=False, verbose_name="Documento S-55 foi considerado com os pais?")

    # --- 4. Informações Médicas (Texto) ---
    problema_especifico = models.TextField(verbose_name="Problema específico / Diagnóstico")
    historico_saude = models.TextField(verbose_name="Histórico de saúde / Causa da emergência")

    # --- 5. Médicos e Plano ---
    medico_responsavel = models.CharField(max_length=150, verbose_name="Médico responsável")
    especialidade_responsavel = models.ForeignKey(
        Specialty, 
        on_delete=models.SET_NULL, # Se apagar a especialidade, mantém a planilha
        verbose_name="Especialidade",
        null=True, 
        blank=True
    )
    outro_medico = models.CharField(max_length=150, blank=True, null=True, verbose_name="Outro médico")
    especialidade_outro = models.ForeignKey(
        Specialty, 
        on_delete=models.SET_NULL,
        verbose_name="Especialidade",
        null=True, 
        blank=True,
        related_name='planilhas_emergencia_secundaria' # Necessário pois temos 2 links para o mesmo model
    )
    
    plano_tratamento = models.TextField(verbose_name="Plano de tratamento médico")
    
    equipe_informada_colih = models.BooleanField(default=False, verbose_name="Equipe informada sobre ajuda da Colih?")
    equipe_cooperando = models.BooleanField(default=False, verbose_name="Equipe está cooperando?")
    acao_judicial_mencionada = models.BooleanField(default=False, verbose_name="Foi mencionada ação judicial?")

    # --- 6. Estratégias e Artigos (Página 2) ---
    estrategias_opcoes = models.TextField(verbose_name="Estratégias / Opções de tratamento")
    artigos_fornecidos = models.TextField(blank=True, null=True, verbose_name="Artigos médicos fornecidos")
    medico_cooperativo_apos_artigos = models.BooleanField(default=False, verbose_name="Médico disposto a cooperar após artigos?")

    # --- 7. Médico Consultor e Transferência ---
    medico_consultor = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nome do médico consultor")
    especialidade_consultor = models.CharField(max_length=100, blank=True, null=True, verbose_name="Especialidade do consultor")
    infos_consultor = models.TextField(blank=True, null=True, verbose_name="Preferências de contato / Outras infos")

    necessidade_transferencia = models.BooleanField(default=False, verbose_name="Necessidade de transferência?")
    procedimentos_transferencia_confirmados = models.BooleanField(default=False, verbose_name="Procedimentos confirmados?")
    hospital_destino = models.CharField(max_length=200, blank=True, null=True, verbose_name="Hospital de destino")
    medico_destino = models.CharField(max_length=150, blank=True, null=True, verbose_name="Médico no destino")
    telefone_destino = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telefone no destino")
    colih_destino_informada = models.BooleanField(default=False, verbose_name="Colih de destino informada?")

    # --- 8. Resultado ---
    resultado_acompanhamento = models.TextField(blank=True, null=True, verbose_name="Resultado / Acompanhamento")
    anciaos_locais_acompanhamento = models.BooleanField(default=False, verbose_name="Anciãos locais contatados para acompanhamento?")

    # --- Novo Campo de Controle ---
    status_gvp = models.CharField(
        max_length=3,
        choices=STATUS_GVP_CHOICES,
        default='PEN',
        verbose_name="Situação do GVP",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome_paciente} - {self.data_hora_contato.strftime('%d/%m/%Y')}"

    class Meta:
        verbose_name = "Planilha de Emergência"
        verbose_name_plural = "Planilhas de Emergência"

class GvpVisit(models.Model):
    # 1. Vínculo com a Planilha de Emergência (Uma planilha pode ter vários acompanhamentos GVP)
    planilha = models.ForeignKey(
        'PlanilhaEmergencia', 
        on_delete=models.CASCADE, 
        verbose_name="Paciente (Planilha de Emergência)",
        related_name="gvp_followups"
    )

    # 2. Usuários Designados do GVP (ManyToManyField)
    # Permite escalar vários irmãos para o acompanhamento
    designated_members = models.ManyToManyField(
        User, 
        verbose_name="Membros do GVP Designados",
        related_name="gvp_assignments"
    )

    # 3. Campos de atuação do GVP (Texto para registro do que foi feito)
    action_taken = models.TextField(
        verbose_name="Ações realizadas / Resumo da visita", 
        help_text="Descreva como o GVP atuou junto ao paciente e equipe médica."
    )
    
    status_patient = models.CharField(
        max_length=100, 
        verbose_name="Status atual do paciente",
        help_text="Ex: Estável, em UTI, aguardando cirurgia..."
    )

    # 4. Data e Hora
    submission_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Data/Hora da Submissão"
    )

    class Meta:
        verbose_name = "Visita GVP"
        verbose_name_plural = "Visitas GVP"
        ordering = ['-submission_date']

    def __str__(self):
        return f"GVP: {self.planilha.nome_paciente} - {self.submission_date.strftime('%d/%m/%Y')}"