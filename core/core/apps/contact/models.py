import datetime
from django.utils import timezone
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length = 150, verbose_name="nom")
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length = 150, verbose_name='objet')
    message = models.TextField()
    timestamp = models.DateTimeField("date", default= timezone.now)
    # phone = models.CharField('telephone', max_length=50, verbose_name='telephone')
    # address = models.TextField(verbose_name='adresse')
    
    # fbk = models.URLField(max_length = 200, verbose_name="lien facebook")
    # twitter = models.URLField(max_length = 200)
    # instagram = models.URLField(max_length = 200)
    
    
    

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("Contact_detail", kwargs={"pk": self.pk})
