from django.contrib import admin

from .models import Doctor, City, Hospital, Specialty, MembroColih, MembroGvp

# Register your models here.

@admin.register(MembroColih)
class MembroColihAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'ativo', 'get_visitas_30_dias')
    list_filter = ('ativo',)
    search_fields = ('user__first_name', 'user__last_name')

    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Nome'

    def get_visitas_30_dias(self, obj):
        return obj.total_visitas_recentes
    get_visitas_30_dias.short_description = 'Visitas Médicas (30 dias)'

@admin.register(MembroGvp)
class MembroGvpAdmin(admin.ModelAdmin):
    # Colunas que aparecerão na lista principal
    list_display = ('get_full_name', 'get_email', 'ativo', 'get_total_visitas')
    
    # Filtros laterais para facilitar a gestão
    list_filter = ('ativo', 'user__is_active')
    
    # Campos de busca (nome do usuário e e-mail)
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    
    # Organização do formulário de edição
    fieldsets = (
        ('Identificação', {
            'fields': ('user',)
        }),
        ('Status no GVP', {
            'fields': ('ativo',),
            'description': 'Membros inativos não aparecerão na escala de visitas.'
        }),
    )

    # Métodos para exibir dados do modelo User na lista do MembroGvp
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = 'Nome Completo'
    get_full_name.admin_order_field = 'user__first_name'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'E-mail'

    def get_total_visitas(self, obj):
        # Utiliza a property que criamos no Model para mostrar no Admin
        return obj.total_visitas_recentes
    get_total_visitas.short_description = 'Visitas (30 dias)'

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    # Mostra o nome e a UF na lista principal
    list_display = ('name', 'uf')
    
    # Cria um filtro lateral por UF (útil quando tiveres muitas cidades)
    list_filter = ('uf',)
    
    # Permite pesquisar pelo nome da cidade ou pela UF
    search_fields = ('name', 'uf')

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    # Colunas que aparecem na tabela
    list_display = ('name', 'city', 'phone', 'register_date')
    
    # Filtros laterais
    list_filter = ('city',)
    
    # Barra de pesquisa. 
    # 'city__name' permite pesquisar um hospital escrevendo o nome da cidade dele!
    search_fields = ('name', 'city__name')
    
    # Como 'register_date' é auto_now_add, ele é somente leitura por padrão.
    # Se quiseres ver o campo dentro do formulário de edição, precisamos declará-lo aqui:
    readonly_fields = ('register_date',)

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    # Mostra o nome e a data na lista principal
    list_display = ('name', 'register_date')
    
    # Barra de pesquisa pelo nome da especialidade
    search_fields = ('name',)
    
    # Ordenação padrão alfabética
    ordering = ('name',)
    
    # Como 'register_date' é automático, precisamos disto para vê-lo no formulário
    readonly_fields = ('register_date',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'hospital', 'city', 'status')
    
    # Agora que Hospital tem cidade, podemos filtrar médicos pela cidade do hospital também
    list_filter = ('hospital', 'city', 'status')
    
    search_fields = ('name', 'crm', 'email')