from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
# Create your models here.

choices2 = (('Any', 'Any'),
                ('Building', 'Building'),
                ('Clinic', 'Clinic'),
                ('Food & Beverage', 'Food & Beverage'),
                ('Office', 'Office'),
                ('Retail', 'Retail'),
                ('Shop', 'Shop'),
                ('Store', 'Store'),
                ('Apartment', 'Apartment'),
                ('Chalet', 'Chalet'),
                ('Condo', 'Condo'),
                ('Duplex', 'Duplex'),
                ('Ground Floor', 'Ground Floor'),
                ('iVilla', 'iVilla'),
                ('Multi Family Home', 'Multi Family Home'),
                ('Penthouse', 'Penthouse'),
                ('S Villa', 'S Villa'),
                ('Serviced Apartment', 'Serviced Apartment'),
                ('Single Family Home', 'Single Family Home'),
                ('Sky Loft', 'Sky Loft'),
                ('Studio', 'Studio'),
                ('Townhouse', 'Townhouse'),
                ('Twin House', 'Twin House'),
                ('Villa', 'Villa'))
choices3 = (("Ain Shokana","Ain Shokana"),
                ("Ain Sokhna","Ain Sokhna"),
                ("Alexandria","Alexandria"),
                ("East Cairo","East Cairo"),
                ("Mostakbal City","Mostakbal City"),
                ("New Cairo","New Cairo"),
                ("New Capital","New Capital"),
                ("North Coast","North Coast"),
                ("Sheik Zayed","Sheik Zayed"),
                ("West Cairo","West Cairo"),
                ("6th of October","6th of October"),
                ("New Zayed","New Zayed"))

class Amenity(models.Model):
    status_choices = (
        (_("Balcony"), _("Balcony")),
        (_("Cable TV"), _("Cable TV")),
        (_("Internet"), _("Internet")),
        (_("Tennis Courts"), _("Tennis Courts")),
        (_("Parking"), _("Parking")),
    )
    name = models.CharField(max_length=100,choices=status_choices,verbose_name=_("name"))
    def __str__(self):
        return f"{self.name}"

class Image_of_house(models.Model):
    img = models.ImageField(upload_to="images")
    house = models.ForeignKey("House",on_delete=models.CASCADE,related_name="other_imgs")
    def __str__(self):
        return f"image({self.img})"
"""
class Agent(models.Model):
    name = models.CharField(_("name"),max_length=50)
    age = models.IntegerField(_("age"),)
    email = models.EmailField(_("email"),null=True,blank=True)
    phone = models.CharField(_("phone"),max_length=50,null=True,blank=True)
    skype = models.CharField(_("skype"),null=True,blank=True,max_length=100)
    img = models.ImageField(_("img"),null=True,blank=True,upload_to="images")
    def __str__(self):
        return f"agent ({self.name})"
"""
class House(models.Model):
    status_choices = (
        (_("sale"), _("sale")),
        (_("rent"), _("rent")),
    )

    img = models.ImageField(_("img"),upload_to="images")
    type = models.CharField(max_length=50,choices=choices2,default="Apartment")
    address = models.CharField(_("address"),max_length=50)
    location = models.CharField(max_length=50,choices=choices3,null=True,blank=True)
    status = models.CharField(_("status"),max_length=100,choices=status_choices)
    area = models.IntegerField(_("area"),)
    beds = models.IntegerField(_("beds"),)
    bathrooms = models.IntegerField(_("bathrooms"),)
    garages = models.IntegerField(_("garages"),)
    price = models.IntegerField(_("price"),)
    #agent = models.ForeignKey(Agent,on_delete=models.CASCADE,verbose_name=_("agent"))
    description = models.TextField(_("description"),)
    amenities = models.ManyToManyField(Amenity,verbose_name=_("amenities"))
    company = models.ForeignKey('Company',on_delete=models.CASCADE,blank=True,null=True)
    project = models.ForeignKey('Project',on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return f"House ({self.id})==>{self.price}EGP"




class Company(models.Model):
    name = models.CharField(max_length=500)
    location = models.CharField(max_length=500,choices=choices3,default='Ain Shokana')
    logo = models.ImageField(upload_to="images",default='houses/real_estate_logo.jpg')
    def __str__(self):
        return f"{self.name}"

class Project(models.Model):
    name = models.CharField(max_length=500)
    company = models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    type = models.CharField(max_length=50, choices=choices2, default="Apartment")
    location = models.CharField(max_length=500, choices=choices3,default='Ain Shokana')
    number_of_units = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name}"



class Message(models.Model):
    user_name = models.CharField(max_length=50,verbose_name=_("user_name"))
    content = models.TextField(verbose_name=_("content"))
    email = models.EmailField(verbose_name=_("email"))
    #agent = models.ForeignKey(Agent,on_delete=models.CASCADE,verbose_name=_("agent"),null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=30,null=True,blank=True)
    project = models.ForeignKey(Project,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return f"message from agent({self.user_name})"

class Inquiry(models.Model):
    choices1 = (('buyer','buyer'),
                ('seller','seller'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=User.objects.all()[0].id)
    buyer_or_seller = models.CharField(max_length=20,choices=choices1,default='buyer')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=30)
    location = models.CharField(max_length=50, choices=choices3, null=True, blank=True,default='Ain Shokana')
    type = models.CharField(max_length=50, choices=choices2, default="Apartment")
    max_price = models.IntegerField()
    min_size = models.IntegerField()
    beds = models.IntegerField()
    bathrooms = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True,null=True,blank=True)

