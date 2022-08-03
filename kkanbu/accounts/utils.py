from django.core.mail import EmailMultiAlternatives


def send_email(context):
    email = EmailMultiAlternatives(
        subject=context["email_subject"],
        body=context["email_body"],
        to=[context["to_email"]],
        from_email=context["from_email"],
    )
    email.send()
