# -*- coding: utf-8 -*-
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from abonne.models import Abonne


def abonneNewsLetter(request):
    email=request.POST["email"]
    is_error = 0
    if email=="":
        error_email="veuillez remplir ce champs"
        is_error = 1
    if is_error==1:
        return HttpResponse("error", status=403)
    else:
        try:
            abon=Abonne.objects.filter(email=email)[0]
            return HttpResponse(u"désolé, vous vous êtes déjà inscrit", status=406)
        except:
            abonne=Abonne()
            abonne.email=email
            abonne.save()

            # envoie d'email de vérification
            author = formataddr((str(Header(u'Teranga-Food', 'utf-8')), "yavouckolye@gmail.com"))
            me = "yavouckolye@gmail.com"
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Inscription"
            msg['From'] = author
            msg['To'] = email
            html = "<html> " \
                   "<p>Félicitation!</p>" \
                   "<p>Votre inscription au Newsletters de Teranga-Food a été bien prise en compte</p>"+\
                   "<p>Vous serez tenu(e) informé de toutes les activités de Teranga-Food à partir de l'instant.</p>"+\
                   "</html>"
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(me, "nkjqsajyzgkbueyy")
            text = msg.as_string()
            server.sendmail(me, email, text)
            server.quit()
            return HttpResponse("good")
