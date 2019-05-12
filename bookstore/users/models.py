from django.db import models, transaction
from django.contrib.auth.models import User
from PIL import Image
from localflavor.us.models import USStateField  # To shows list of US states on address form
from django.urls import reverse # to return url when clicking on address
from .payments import MONTHS, YEARS, JAN, THIS_YEAR


# All user data is/should be linked to this profile, so when user gets deleted, all data deletes as well
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nick_name = models.CharField('Nick name', max_length=30, blank=True, default='')
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # Address = models.ForeignKey('Address', on_delete=models.CASCADE)

    # If we don't have this, it's going to say profile object only
    def __str__(self):
        return self.user.username
        #return f'{self.user.username}'  # it's going to print username Profile

    def save(self, *args, **kwargs):
            super().save(*args, **kwargs)

            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Address(models.Model):
    name = models.CharField(max_length=100, blank=False)
    address1 = models.CharField("Address lines 1", max_length=128)
    address2 = models.CharField("Address lines 2", max_length=128, blank=True)
    city = models.CharField("City", max_length=64)
    state = USStateField("State", default='FL')
    zipcode = models.CharField("Zipcode", max_length=5)
    slug = models.SlugField(max_length=150, db_index=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)
    primaryAddress = models.BooleanField()

    class Meta:

        verbose_name = 'Address'            # How we'll refer to a single Address
        verbose_name_plural = 'Addresses'   # How we'll refer to multiple Address

    def __str__(self):
        return self.name

    @transaction.atomic
    def save(self, *args, **kwargs):
        if self.primaryAddress:
            Address.objects.filter(
                primaryAddress=True).update(primaryAddress=False)
        super(Address, self).save(*args, **kwargs)

    # Got the idea from: https://docs.djangoproject.com/en/2.1/ref/models/instances/#get-absolute-url
    def get_absolute_url(self):
        return reverse('settings:edit-address', args=[self.id])


class CreditCard(models.Model):
    name = models.CharField(max_length=100, blank=False)
    number = models.CharField(max_length=16, blank=False, unique=True)
    expdate_month = models.IntegerField(choices=MONTHS, default=JAN)
    expdate_year = models.IntegerField(choices=YEARS, default=THIS_YEAR)
    securitycode = models.IntegerField(blank=False)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=False)

    class Meta:
        verbose_name = 'Credit Card'            # How we'll refer to a single Address
        verbose_name_plural = 'Credit Cards'   # How we'll refer to multiple Address

    def __str__(self):
        return self.name

    # Got the idea from: https://docs.djangoproject.com/en/2.1/ref/models/instances/#get-absolute-url
    def get_absolute_url(self):
        return reverse('settings:edit-creditcard', args=[self.id])
