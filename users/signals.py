"""Signals for the CusDeb API Users application. """

from urllib.parse import urljoin

from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django_rest_passwordreset.models import get_password_reset_token_expiry_time
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(
        sender,  # pylint: disable=unused-argument
        reset_password_token, *_args, **_kwargs
):
    """Handles password reset tokens.
    When a token is created, an e-mail needs to be sent to the user.
    """

    reset_password_base_url = urljoin(settings.BASE_SITE_URL, '/reset-password/confirm/')
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        'reset_password_url': f'{reset_password_base_url}?token={reset_password_token.key}',
        'base_site_url': settings.BASE_SITE_URL,
        'site_name': settings.DEFAULT_SITE_NAME,
        'token_expiry_time': get_password_reset_token_expiry_time(),
    }
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        subject=f'Password reset for {settings.DEFAULT_SITE_NAME}',
        body=email_plaintext_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        bcc=[reset_password_token.user.email],
        headers={
            'From': f'{settings.DEFAULT_SITE_NAME} <{settings.DEFAULT_FROM_EMAIL}>',
            'To': reset_password_token.user.email,
        }
    )
    msg.attach_alternative(email_html_message, 'text/html')
    msg.send()
