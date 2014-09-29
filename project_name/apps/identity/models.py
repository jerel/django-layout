"""
Identity models
"""
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class IdentityManager(BaseUserManager):
    """
    User manager
    """
    def create_identity(self, email, password=None, **extra_fields):
        """
        Create a new user
        """
        now = timezone.now()

        if not email:
            raise ValueError("An email address must be set.")

        extra = {
            'is_staff': False,
            'is_superuser': False,
            'is_active': True,
            'last_login': now,
            'date_joined': now
        }
        extra.update(extra_fields)

        email = IdentityManager.normalize_email(email)
        identity = self.model(
            email=email,
            **extra
        )
        identity.set_password(password)
        identity.save(using=self._db)
        return identity

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a superuser
        """
        u = self.create_identity(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


def avatar_upload_path(instance, filename):
    """
    Identity avatar file location
    """
    return u'avatars/{0}/{1}'.format(instance.pk, filename)


class Identity(AbstractBaseUser, PermissionsMixin):
    """
    User identity model.

    The main change between this and the default django user model is that we
    don't have a username. We'll use email addresses for login.
    """
    first_name = models.CharField(
        _('first name'), max_length=50, blank=True
    )
    last_name = models.CharField(
        _('last name'), max_length=50, blank=True
    )
    email = models.EmailField(
        _('email'), max_length=254, unique=True, db_index=True
    )
    is_staff = models.BooleanField(
        _('is staff'), default=False,
        help_text=_('Designates if the user is a staff member'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    avatar = models.ImageField(
        _('avatar'), upload_to=avatar_upload_path,
        blank=True, null=True)

    objects = IdentityManager()
    legacy_user_id = models.PositiveIntegerField(blank=True, null=True)

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('identity')
        verbose_name_plural = _('identities')

    def __unicode__(self):
        if self.get_full_name() != '' and self.get_full_name() != None:
            return self.get_full_name()
        else:
            return self.email

    @models.permalink
    def get_absolute_url(self):
        return '/'

    def get_full_name(self):
        full_name = '{0} {1}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name.strip()

    def email_user(self, subject, message, from_email=None):
        return send_mail(subject, message, from_email, [self.email])

