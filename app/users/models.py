from django.db import models
from django.urls import reverse
from django.contrib.auth import base_user, models as auth_models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from django.core.files.base import ContentFile
from django.db.models.signals import post_save

from PIL import Image


class CustomUserManager(base_user.BaseUserManager):
    """
    CustomUser manager for CustomUser for authentication using email and
    password
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create a user with given email and password
        """

        if email:
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)

            return user

        raise ValueError(_("Email must entered to create a user"))

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a superuser with given email, password and other credentials
        """

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError(_("Superuser must have is_staff=True"))
        if not extra_fields.get("is_superuser"):
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(email, password, **extra_fields)


def save_image(instance, filename):
    user_id = instance.id
    extension = filename.rsplit(".", 1)[-1]
    timestamp = str(now().date())
    filename = f"{timestamp}.{extension}"
    return "/".join(("profile", str(user_id), filename))


def save_thumb(instance, filename):
    user_id = instance.id
    timestamp = str(now().date())
    extension = filename.rsplit(".", 1)[-1]
    filename = f"{timestamp}.{extension}"
    return "/".join(("profile", str(user_id), "thumb", filename))


class CustomUser(auth_models.AbstractUser):
    """
    CustomUser model with email and password for authentication
    """
    username = None
    email = models.EmailField(_("email address"), unique=True)
    image = models.ImageField(upload_to=save_image, blank=True, null=True)
    image_thumb = models.ImageField(upload_to=save_thumb,
                                    blank=True,
                                    null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def __init__(self, *args, **kwargs):
        super(CustomUser, self).__init__(*args, **kwargs)

        # Store the current image to check for a change while updating image
        self._curr_image = self.image

    @staticmethod
    def get_absolute_url():
        return reverse("profile")

    def save(self, *args, **kwargs):
        created = self._state.adding        # created or updated
        image_updated = False

        if not created:

            # Store the new image
            image = self.image

            if image and image.name != self._curr_image.name:
                image_updated = True

                # Deleting the previous image and its thumnail
                self._curr_image.delete(False)
                self.image_thumb.delete(False)

                # Assigning the image field with the new image
                self.image = image

                image_name = image.name.rsplit("/", 1)[-1]

                # Create a new image for thumbnail
                thumb_image = ContentFile(image.read())

                # Save the thumbnail but do not commit to the database
                self.image_thumb.save(image_name, thumb_image, False)

        # Save the model
        super(CustomUser, self).save(*args, **kwargs)

        if image_updated:
            # Get the thumbnail image from its path to resize it
            thumb_image = Image.open(self.image.path)

            if thumb_image.height > 140 or thumb_image.height > 140:
                output_size = (140, 140)
                thumb_image.thumbnail(output_size)

                # Save the resized image to its path
                thumb_image.save(self.image_thumb.path)

    def delete(self, *args, **kwargs):
        # Delete the user image or anything after object is deleted

        if self.image:
            self.image.delete(False)
            self.image_thumb.delete(False)
        super(CustomUser, self).delete(*args, **kwargs)


class GlobalInfo(models.Model):
    """Model to store extra user information accecible by everyone"""

    logo = models.ImageField(upload_to="logo/", blank=True, null=True)
    address = models.CharField(max_length=350, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        super(GlobalInfo, self).__init__(*args, **kwargs)
        self._current_logo = self.logo

    def save(self, *args, **kwargs):
        """
        - Overriding save to enforce only single instance of the model
        - Delete the previous image files on update
        """

        if self.__class__.objects.count():
            self.pk = self.__class__.objects.first().pk

        created = self._state.adding    # Whether object created or updated
        logo_updated = False

        if not created:
            logo = self.logo

            if logo and self._current_logo.name != logo.name:
                self._current_logo.delete(False)
                self.logo = logo

                logo_updated = True
        super(GlobalInfo, self).save(*args, **kwargs)

        if logo_updated:
            logo = Image.open(self.logo.path)

            if logo.width > 300 or logo.height > 300:
                output_size = (300, 300)
                logo.thumbnail(output_size)
                logo.save(self.logo.path)

    @staticmethod
    def get_absolute_url():
        return reverse("global_settings")


def create_global_info(sender, instance, created, *args, **kwargs):
    if created:
        GlobalInfo.objects.get_or_create()


post_save.connect(create_global_info, sender=CustomUser)
