from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
import os

# Create your models here.

class User(AbstractUser):
    birthday = models.DateField()

    gender_Choices = (('남','남') ,('여','여'))
    gender = models.CharField(max_length=20, choices=gender_Choices)

    followings = models.ManyToManyField('self', symmetrical=False,related_name='followers')

    def profile_image_path(instance, filename):
        return f'products/{instance.pk}/{filename}'

    profile_image = ProcessedImageField(
        upload_to=profile_image_path,
        processors=[ResizeToFill(100,100)],
        format='JPEG',
        options={'quality' : 100},
        blank=True,
        null=True,
    )

    def delete(self, *args, **kargs):
        if self.profile_image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.profile_image.path))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(User, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_user = User.objects.get(id=self.id)
            if self.profile_image != old_user.profile_image:
                if old_user.profile_image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_user.profile_image.path))
        super(User, self).save(*args, **kwargs)