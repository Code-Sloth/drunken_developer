from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.conf import settings
import os

# Create your models here.

class User(AbstractUser):
    birthday = models.DateField(null=True)

    gender_Choices = (('choose','성별 선택'), ('man','남') ,('woman','여'))
    gender = models.CharField(max_length=20, choices=gender_Choices, default='choose')

    followings = models.ManyToManyField('self', symmetrical=False,related_name='followers')

    def profile_image_path(instance, filename):
        return f'products/{instance.pk}/{filename}'

    image = ProcessedImageField(
        upload_to=profile_image_path,
        processors=[ResizeToFill(100,100)],
        format='JPEG',
        options={'quality' : 100},
        blank=True,
        null=True,
    )

    def delete(self, *args, **kargs):
        if self.image:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.image.path))
            dir_path = os.path.dirname(os.path.join(settings.MEDIA_ROOT, self.image.name))
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
        super(User, self).delete(*args, **kargs)

    def save(self, *args, **kwargs):
        if self.id:
            old_user = User.objects.get(id=self.id)
            if self.image != old_user.image:
                if old_user.image:
                    os.remove(os.path.join(settings.MEDIA_ROOT, old_user.image.path))
        super(User, self).save(*args, **kwargs)
