from django.contrib.auth.models import User

# Create your models here.



class skmerUser(User):
    class Meta:
        proxy = True
        ordering = ('username','password','email')

    def __str__(self):
        return str(self.pk) +'--'+ self.username


