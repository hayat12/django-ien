from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from myapp import helper


def ienproductvariation_dir_path(instance, filename):
    return '__{0}__/{1}'.format(instance.id, filename)


def get_picture_dir(self):
    j = None
    try:
        i = helpers.get_wsproduct_dir()
        j = os.path.join(i, '__{0}__'.format(self.id))
    except:
        pass
    return j


def get_picture_upload_path(self, filename):
    r = None
    try:
        k = helper.get_ws_dir()
        helper.ensure_dir(k)
        i = helper.get_wsproduct_dir()
        helper.ensure_dir(i)
        j = self.get_picture_dir()
        helper.ensure_dir(j)
        r = os.path.join(j, filename)
    except:
        raise
    return r


class UserProfile(models.Model):

    class Meta:
        db_table = 'ien_user'

    picture = models.ImageField(
        max_length=255, blank=True, null=True, upload_to='media')
    company_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254, blank=True, null=True)
    fax = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=254, blank=True, null=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user')

    steps = models.IntegerField(null=True, default=0)
    designation = models.CharField(max_length=250, null=True)
    about_me = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    dob = models.CharField(max_length=50, null=True, blank=True)
    # address = models.TextField(blank=True, null=True)
    organization_name = models.CharField(blank=True, null=True, max_length=250)
    position_held = models.CharField(blank=True, null=True, max_length=250)
    passport = models.CharField(blank=True, null=True, max_length=250)
    account_no = models.CharField(blank=True, null=True, max_length=250)
    bank_name = models.CharField(null=True, blank=True, max_length=250)
    main_interest = models.CharField(max_length=250, null=True, blank=True)
    sub_interest = models.CharField(max_length=250, null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='created_by')
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')


class Event(models.Model):
    class Meta:
        verbose_name = "Event"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user')
    event_name = models.CharField(max_length=250, null=True, blank=True)
    category = models.CharField(max_length=250, null=True, blank=True)
    location = models.TextField(blank=True, null=True)
    selected_address = models.TextField(blank=True, null=True)
    about_event = models.TextField(blank=True, null=True)
    event_image = models.FileField(blank=True, null=True)
    start_time = models.TextField(blank=False, null=False)
    start_date = models.TextField(blank=False, null=False)
    end_time = models.TextField(blank=False, null=False)
    end_date = models.TextField(blank=False, null=False)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='created_by')
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')


class Connection(models.Model):
    class Meta:
        verbose_name = "Connection"
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user'),
    invited_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user'),
    created_date = models.DateTimeField(auto_now_add=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')


class Adgenda(models.Model):
    class Meta:
        verbose_name = "Adgenda"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user')
    title = models.CharField(max_length=250, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    start_time = models.CharField(blank=False, null=False, max_length=250)
    start_date = models.CharField(blank=False, null=False, max_length=250)

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='created_by')
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')


class AdgendaInvites(models.Model):
    class Meta:
        verbose_name = "AdgendaInvites"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='user'),
    invite_id = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='invite_id')
    status = models.IntegerField(blank=True, null=True)
    adg_id = models.ForeignKey(
        Adgenda, on_delete=models.CASCADE, related_name='AdgendaInvites', db_column='adg_id')

    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='+', db_column='created_by')
    modified_date = models.DateTimeField(auto_now=True, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='+', db_column='modified_by')
