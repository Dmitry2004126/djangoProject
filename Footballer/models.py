from django.db import models
from django.contrib.auth.models import User


class Side(models.Model):
    name = models.CharField(max_length=50, verbose_name="Side of the project",
                            help_text="Input your side", null=False, blank=False)

    def __str__(self):
        return "Side: " + self.name


class Seller(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    date_birth = models.DateField()
    experience = models.CharField(max_length=200, default="")
    side = models.ForeignKey(Side, on_delete=models.CASCADE, verbose_name="id Side",
                                help_text="Choose side", null=False, blank=False, default=1)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id пользователя",
                                help_text="Выберите id пользователя", null=True, blank=True)

    class Meta:
        app_label = "Footballer"

    def __str__(self):
        return "Seller Name: " + self.first_name + " Last name: " + self.last_name


class Buyer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=100)
    date_birth = models.DateField(default="2018-01-10")
    company_experience = models.CharField(max_length=200, default="")
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="id пользователя",
                                help_text="Выберите id пользователя", null=True, blank=True)


    def __str__(self):
        return "Buyer: " + self.first_name


class Project(models.Model):
    number = models.IntegerField()
    project_name = models.CharField(max_length=200, default="")
    date_start = models.DateField(default="2018-01-10")
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)



    def __str__(self):
        return "Project with worker: " + self.seller.first_name + " and buyer: " + self.buyer.last_name


