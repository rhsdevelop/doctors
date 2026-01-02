from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives, get_connection
from .models import EmailConfiguration

def disparar_alerta_gvp(planilha, request):
    config = EmailConfiguration.objects.first()
    if not config:
        return False

    assunto = f"🚨 GVP: Acompanhamento Urgente - {planilha.nome_paciente}"
    
    # Contexto para o template
    context = {
        'planilha': planilha,
        'site_url': request.build_absolute_uri('/')[:-1] # Pega a URL base do sistema
    }

    # Renderiza o HTML e cria uma versão em texto simples (fallback)
    html_content = render_to_string('emails/alerta_gvp.html', context)
    text_content = strip_tags(html_content)

    try:
        connection = get_connection(
            host=config.smtp_server,
            port=config.smtp_port,
            username=config.email_user,
            password=config.email_password,
            use_tls=config.use_tls
        )

        # Usamos EmailMultiAlternatives para enviar HTML + Texto
        email = EmailMultiAlternatives(
            assunto, text_content, config.email_user, ['amigao.ituverava@gmail.com'], # Troque pelo e-mail da equipe
            connection=connection
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False