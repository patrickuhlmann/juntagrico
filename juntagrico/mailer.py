# -*- coding: utf-8 -*-

import os
import re

from django.contrib.auth.models import Permission, User
from django.contrib.sites.shortcuts import get_current_site
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.conf import settings
from django.template.loader import get_template

from juntagrico.config import Config
from juntagrico.util.ical import *
def get_server(server):
    site_from_env = os.getenv("ORTOLOCO_TEMPLATE_SERVERURL")
    if site_from_env:
        return site_from_env
    site_from_db = get_current_site(None).domain
    if site_from_db:
        return site_from_db
    return server


# sends mail only to specified email-addresses if dev mode
def send_mail(subject, message, from_email, to_emails):
    okmails = []
    if settings.DEBUG is False:
        okmails = to_emails
    else:
        for email in to_emails:
            sent = False
            for entry in settings.WHITELIST_EMAILS:
                if sent is False and re.match(entry, email):
                    sent = True
                    okmails.append(email)
            if not sent:
                print "Mail not sent to " + ", " + email + ", not in whitelist"

    if len(okmails) > 0:
        for amail in okmails:
            mail.send_mail(subject, message, from_email, [amail], fail_silently=False)
        print "Mail sent to " + ", ".join(okmails) + (", on whitelist" if settings.DEBUG else "")

    return None


def send_mail_multi(email_multi_message):
    okmails = []
    if settings.DEBUG is False:
        okmails = email_multi_message.to
    else:
        for email in email_multi_message.to:
            sent = False
            for entry in settings.WHITELIST_EMAILS:
                if sent is False and re.match(entry, email):
                    sent = True
                    okmails.append(email)
            if not sent:
                print "Mail not sent to " + email + ", not in whitelist"

    if len(okmails) > 0:
        email_multi_message.to = []
        email_multi_message.bcc = okmails
        email_multi_message.send()
        print "Mail sent to " + ", ".join(okmails) + (", on whitelist" if settings.DEBUG else "")
    return None


def send_new_member_in_activityarea_to_operations(area, member):
    send_mail('Neues Mitglied im Taetigkeitsbereich ' + area.name,
              'Soeben hat sich ' + member.first_name + " " + member.last_name + ' in den Taetigkeitsbereich ' + area.name + ' eingetragen',
              Config.info_email(), [area.coordinator.email])


def send_contact_form(subject, message, member, copy_to_member):
    send_mail('Anfrage per ' + Config.adminportal_name() + ': ' + subject, message, member.email, [Config.info_email()])
    if copy_to_member:
        send_mail('Anfrage per ' + Config.adminportal_name() + ': ' + subject, message, member.email, [member.email])


def send_contact_member_form(subject, message, member, contact_member, copy_to_member, attachments):
    msg = EmailMultiAlternatives('Nachricht per ' + Config.adminportal_name() + ': ' + subject, message, member.email,
                                 [contact_member.email], headers={'Reply-To': member.email})
    for attachment in attachments:
        msg.attach(attachment.name, attachment.read())
    send_mail_multi(msg)
    if copy_to_member:
        send_mail('Nachricht per ' + Config.adminportal_name() + ': ' + subject, message, member.email, [member.email])


def send_welcome_mail(email, password, hash, server):
    plaintext = get_template('mails/welcome_mail.txt')
    htmly = get_template('mails/welcome_mail.html')

    # reset password so we can send it to him
    d = {
        'subject': 'Willkommen bei ' + Config.organisation_name(),
        'username': email,
        'password': password,
        'hash': hash,
        'serverurl': "http://" + get_server(server)
    }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives('Willkommen bei ' + Config.organisation_name(), text_content, Config.info_email(),
                                 [email])
    msg.attach_alternative(html_content, "text/html")
    send_mail_multi(msg)


def send_share_created_mail(share, server):
    plaintext = get_template('mails/share_created_mail.txt')
    htmly = get_template('mails/share_created_mail.html')

    # reset password so we can send it to him
    d = {
        'member': share.member,
        'share': share,
        'serverurl': "http://" + get_server(server)
    }
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    perm = Permission.objects.get(codename='is_book_keeper')
    users = User.objects.filter(Q(groups__permissions=perm) | Q(user_permissions=perm)).distinct()
    emails = []
    for user in users:
        emails.append(user.member.email)
    msg = EmailMultiAlternatives('Neuer Anteilschein erstellt', text_content, Config.info_email(), emails)
    msg.attach_alternative(html_content, "text/html")
    send_mail_multi(msg)


def send_been_added_to_subscription(email, password, name, shares, hash, server):
    plaintext = get_template('mails/welcome_added_mail.txt')
    htmly = get_template('mails/welcome_added_mail.html')

    # reset password so we can send it to him
    d = {
        'subject': 'Willkommen bei ' + Config.organisation_name(),
        'username': email,
        'name': name,
        'password': password,
        'hash': hash,
        'shares': shares,
        'serverurl': "http://" + get_server(server)
    }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives('Willkommen bei ' + Config.organisation_name(), text_content, Config.info_email(),
                                 [email])
    msg.attach_alternative(html_content, "text/html")
    send_mail_multi(msg)


def send_filtered_mail(subject, message, text_message, emails, server, attachments, sender):
    plaintext = get_template('mails/filtered_mail.txt')
    htmly = get_template('mails/filtered_mail.html')

    htmld = {
        'subject': subject,
        'content': message,
        'serverurl': "http://" + get_server(server)
    }
    textd = {
        'subject': subject,
        'content': text_message,
        'serverurl': "http://" + get_server(server)
    }

    text_content = plaintext.render(textd)
    html_content = htmly.render(htmld)

    msg = EmailMultiAlternatives(subject, text_content, sender, emails, headers={'Reply-To': sender})
    msg.attach_alternative(html_content, "text/html")
    for attachment in attachments:
        msg.attach(attachment.name, attachment.read())
    send_mail_multi(msg)


def send_mail_password_reset(email, password, server):
    plaintext = get_template('mails/password_reset_mail.txt')
    htmly = get_template('mails/password_reset_mail.html')
    subject = 'Dein neues ' + Config.organisation_name() + ' Passwort'

    d = {
        'subject': subject,
        'email': email,
        'password': password,
        'serverurl': "http://" + get_server(server)
    }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(subject, text_content, Config.info_email(), [email])
    msg.attach_alternative(html_content, "text/html")
    send_mail_multi(msg)


def send_job_reminder(emails, job, participants, server):
    plaintext = get_template('mails/job_reminder_mail.txt')
    htmly = get_template('mails/job_reminder_mail.html')
    coordinator = job.typeactivityarea.coordinator
    contact = coordinator.first_name + " " + coordinator.last_name + ": " + job.typeactivityarea.contact()

    d = {
        'job': job,
        'participants': participants,
        'serverurl': "http://" + get_server(server),
        'contact': contact
    }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(Config.organisation_name() + " - Job-Erinnerung", text_content, Config.info_email(),
                                 emails)
    msg.attach_alternative(html_content, "text/html")
    send_mail_multi(msg)


def send_job_canceled(emails, job, server):
    plaintext = get_template('mails/job_canceled_mail.txt')
    htmly = get_template('mails/job_canceled_mail.html')

    d = {
        'job': job,
        'serverurl': "http://" + get_server(server)
    }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(Config.organisation_name() + " - Job-Abgesagt", text_content, Config.info_email(),
                                 emails)
    msg.attach_alternative(html_content, "text/html")
    send_mail_multi(msg)


def send_job_time_changed(emails, job, server):
    plaintext = get_template('mails/job_time_changed_mail.txt')
    htmly = get_template('mails/job_time_changed_mail.html')

    d = {
        'job': job,
        'serverurl': "http://" + get_server(server)
    }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    #    ical_content = genecrate_ical_for_job(job)

    msg = EmailMultiAlternatives(Config.organisation_name() + " - Job-Zeit geändert", text_content, Config.info_email(),
                                 emails)
    msg.attach_alternative(html_content, "text/html")
    #   msg.attach("einsatz.ics", ical_content, "text/calendar")
    send_mail_multi(msg)


def send_job_signup(emails, job, server):
    plaintext = get_template('mails/job_signup_mail.txt')
    htmly = get_template('mails/job_signup_mail.html')

    d = {
        'job': job,
        'serverurl': "http://" + get_server(server)
    }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    ical_content = genecrate_ical_for_job(job)

    msg = EmailMultiAlternatives(Config.organisation_name() + " - für Job Angemeldet", text_content,
                                 Config.info_email(), emails)
    msg.attach_alternative(html_content, "text/html")
    msg.attach("einsatz.ics", ical_content, "text/calendar")
    print repr(msg.message().as_string())
    print repr(os.linesep)
    #   send_mail_multi(msg)


def send_depot_changed(emails, depot, server):
    plaintext = get_template('mails/depot_changed_mail.txt')
    htmly = get_template('mails/depot_changed_mail.html')

    d = {
        'depot': depot,
        'serverurl': "http://" + get_server(server)
    }

    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    msg = EmailMultiAlternatives(Config.organisation_name() + " - Depot geändert", text_content, Config.info_email(),
                                 emails)
    msg.attach_alternative(html_content, "text/html")
    send_mail_multi(msg)
