from django.shortcuts import render,redirect
from .models import Amenity,House,Message,Image_of_house,Inquiry,Project,Company
from .forms import HouseForm,SearchForm,MessageForm,InquiryForm,ProjectForm,CompanyForm
from django.db.models import Q
from django.views.generic import ListView
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse,reverse_lazy
from django.core.paginator import Paginator
from django.contrib.auth.models import User
# Create your views here.
#https://www.redww.com/wp-content/uploads/2021/02/Untitled-2-17-07.jpg
#https://www.redww.com/wp-content/uploads/2021/02/artboards_06.jpg
#https://www.redww.com/wp-content/uploads/2021/02/artboards_08-copy-5-1.jpg
#https://www.redww.com/wp-content/uploads/2021/02/artboards_06-copy-2-8.jpg
#https://www.redww.com/wp-content/uploads/2021/02/artboards_03-copy-2-7.jpg
#https://www.redww.com/wp-content/uploads/2021/02/IL-BOSCO-City-12.jpg
def index(request):
    if request.method=="POST":
        print("FOOOOOOOOOOOOOOOOOOORM")
        print(request.POST)
        pass
    all_houses = House.objects.all()
    buildings = 0
    clinics = 0
    food_beverages = 0
    offices = 0
    apartments = 0
    stores = 0
    total = []
    backgrounds = list()
    names = list()

    ain_shokana = 0
    ain_sokhna = 0
    alex = 0
    east_cairo = 0
    mostakbal = 0
    total_locations = []
    location_names = []
    location_names.append("Ain Shokana")
    location_names.append("Ain Sokhna")
    location_names.append("Alexandria")
    location_names.append("East Cairo")
    location_names.append("Mostakbal City")

    names.append("buildings")
    names.append("clinics")
    names.append("food & beverages")
    names.append("offices")
    names.append("apartments")
    names.append("stores")
    backgrounds.append("https://www.redww.com/wp-content/uploads/2021/02/Untitled-2-17-07.jpg")
    backgrounds.append("https://www.redww.com/wp-content/uploads/2021/02/artboards_06.jpg")
    backgrounds.append("https://www.redww.com/wp-content/uploads/2021/02/artboards_08-copy-5-1.jpg")
    backgrounds.append("https://www.redww.com/wp-content/uploads/2021/02/artboards_06-copy-2-8.jpg")
    backgrounds.append("https://www.redww.com/wp-content/uploads/2021/02/artboards_03-copy-2-7.jpg")
    backgrounds.append("https://www.redww.com/wp-content/uploads/2021/02/IL-BOSCO-City-12.jpg")
    for house in all_houses:
        if house.location == "Ain Shokana":
            ain_shokana += 1
        if house.location == "Ain Sokhna":
            ain_sokhna += 1
        if house.location == "Alexandria":
            alex += 1
        if house.location == "East Cairo":
            east_cairo += 1
        if house.location == "Mostakbal City":
            mostakbal += 1


        if house.type == "Building":
            buildings += 1
        if house.type == "Clinic":
            clinics += 1
        if house.type == "Food & Beverage":
            food_beverages += 1
        if house.type == "Office":
            offices += 1
        if house.type == "Apartment":
            apartments += 1
        if house.type == "Store":
            stores += 1
    total.append(buildings)
    total.append(clinics)
    total.append(food_beverages)
    total.append(offices)
    total.append(apartments)
    total.append(stores)

    total_locations.append(ain_shokana)
    total_locations.append(ain_sokhna)
    total_locations.append(alex)
    total_locations.append(east_cairo)
    total_locations.append(mostakbal)
    context = {"all_houses": all_houses[:6],
               "SearchForm":SearchForm,

               "total":total,
               "all_data":zip(total,backgrounds,names),
               "location_names":location_names,
               "location_counts":total_locations,
               "inquiry_form":InquiryForm}
    return render(request,"houses/index.html",context)

def search_for(request):
    if request.method == "POST":
        order_index = request.POST.get("order_by")
        print("/  . . .   . .. ",order_index,type(order_index))
    else:
        order_index = request.GET.get("order_by")
    form = SearchForm(request.POST)
    print(f"0     .      0 order_index = {order_index}")
    keyword = request.GET.get("keyword")
    locations = request.GET.get("locations")
    house_type = request.GET.get("type")
    bedrooms = request.GET.get("bedrooms")
    bathrooms = request.GET.get("bathrooms")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    min_area = request.GET.get("min_area")
    max_area = request.GET.get("max_area")
    property_id = request.GET.get("property_id")
    if property_id != "":
        all_houses = House.objects.get(id=property_id)
        context = {"all_houses":[all_houses],
                   "SearchForm": SearchForm,
                   "one_house":True}
        return render(request, 'houses/search_results.html', context)
    if locations == "Any":
        locations = ""
    if house_type == "Any":
        house_type = ""
    all_houses = House.objects.filter(area__lte=max_area,
                                      area__gte=min_area,
                                      price__lte=max_price,
                                      price__gte=min_price,
                                      beds__lte=bedrooms,
                                      bathrooms__lte=bathrooms,
                                      location__icontains=locations,
                                      type__icontains=house_type,
                                      address__icontains=keyword)
    try:
        if int(order_index) == 1:
            print("order               price")
            all_houses = all_houses.order_by("price")
        elif order_index == "2":
            all_houses = all_houses.order_by("-price")
        elif order_index == "3":
            all_houses = all_houses.order_by("area")
        elif order_index == "4":
            all_houses = all_houses.order_by("-area")
    except:
        pass
    paginator = Paginator(all_houses, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if order_index is not None:
        context = {"all_houses":all_houses,
                   "order_value":order_index,
                   "SearchForm":SearchForm,
                   'page_obj': page_obj,
                   "one_house":False}
    else:
        context = {"all_houses": all_houses,
                   "order_value": order_index,
                   "SearchForm": SearchForm,
                   'page_obj': page_obj,
                   "one_house":False}
    return render(request,'houses/search_results.html',context)

def get_inquiry(request):
    form = InquiryForm(request.GET)
    if form.is_valid():
        form.save()
    return redirect('home')

def show_all_inquiry(request):
    all_inqures = Inquiry.objects.all()
    context = {"all_inqures":all_inqures}
    return render(request,'houses/show_all_inquiry.html',context)

def show_all_projects(request):#Project,Company
    form = ProjectForm()
    all_projects = Project.objects.all()
    context = {"all_projects":all_projects,
               "form":form}
    return render(request,'houses/show_projects.html',context)

def add_project(request):
    form = ProjectForm()
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_all_projects')
    context = {"form":form}
    return render(request,'houses/add_project.html',context)

def add_company(request):
    form = CompanyForm()
    if request.method == "POST":
        form = CompanyForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('show_all_companies')
    context = {"form": form}
    return render(request, 'houses/add_company.html', context)
def show_all_companies(request):
    all_companies = Company.objects.all()
    context = {"all_companies":all_companies}
    return render(request,'houses/show_companies.html',context)
###########################################################################
def show_single_company(request,id):
    order_index = 0
    if request.method == "POST":
        order_index = request.POST["order_by"]
    else:
        order_index = request.GET.get("order_by")
    company = Company.objects.get(pk=id)
    houses = House.objects.all()
    all_houses_old = houses
    try:
        if order_index == "1":
            all_houses_old = all_houses_old.order_by("price")
            print("              1")
        if order_index == "2":
            all_houses_old = all_houses_old.order_by("-price")
            print("              2")
        if order_index == "3":
            all_houses_old = all_houses_old.order_by("area")
            print("              3")
        if order_index == "4":
            all_houses_old = all_houses_old.order_by("-area")
            print("              4")
        if order_index == "0":
            pass
    except Exception as inst:
        print("order_index does not exist yet")
        print(inst)
    all_houses = []
    for house in all_houses_old:
        if house.company == company:
            all_houses.append(house)
    paginator = Paginator(all_houses, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"all_houses":all_houses,
               "order_value":order_index,
               "company":company,
               "page_obj":page_obj}
    return render(request,'houses/show_single_company.html',context)

def show_single_project(request,id):
    order_index = 0
    if request.method == "POST":
        order_index = request.POST["order_by"]
    else:
        order_index = request.GET.get("order_by")
    project = Project.objects.get(pk=id)
    houses = House.objects.all()
    all_houses_old = houses
    try:
        if order_index == "1":
            all_houses_old = all_houses_old.order_by("price")
            print("              1")
        if order_index == "2":
            all_houses_old = all_houses_old.order_by("-price")
            print("              2")
        if order_index == "3":
            all_houses_old = all_houses_old.order_by("area")
            print("              3")
        if order_index == "4":
            all_houses_old = all_houses_old.order_by("-area")
            print("              4")
        if order_index == "0":
            pass
    except Exception as inst:
        print("order_index does not exist yet")
        print(inst)
    all_houses = []
    for house in all_houses_old:
        if house.project == project:
            all_houses.append(house)
    paginator = Paginator(all_houses, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"all_houses":all_houses,
               "order_value":order_index,
               "page_obj":page_obj}
    return render(request,'houses/show_single_company.html',context)

"""
class SearchView(ListView):
    model = House
    template_name = 'houses/search_results.html'
    paginate_by = 3
    context_object_name = "all_houses"
    ordering = ["price"]

    def post(self,request):
        order_index = request.POST.get("order_by")
        if order_index == 0:
            pass
        if order_index == 1:
            self.ordering = ["price"]
        if order_index == 2:
            self.ordering

    def get_context_data(self):
        base = super().get_context_data()
        base["SearchForm"] = SearchForm
        return base
"""
def write_msg(request):
    form = MessageForm()
    if request.method == "POST":
        user = User.objects.all()[0]
        name = request.POST["user_name"]
        email = request.POST["email"]
        message = request.POST["content"]
        new_msg = Message(user_name=name, content=message, email=email,user=user)
        new_msg.save()
        return redirect('home')
    context = {"form":form}
    return render(request,'houses/write_new_message.html',context)

def single(request,id):
    single_house = House.objects.get(id=id)
    form = MessageForm()
    if request.method=="POST":
        print("##########################")
        print(request.POST)
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    context = {"house":single_house,
               "form":form}
    return render(request,"houses/property-single.html",context)

#######################
class propertiesView(ListView):
    model = House
    paginate_by = 6
    template_name = "houses/property-grid.html"
    context_object_name = "all_houses"

def list_properties(request):
    if request.method == "POST":
        order_index = request.POST.get("order_by")
        print("/  . . .   . .. ",order_index,type(order_index))
    else:
        order_index = request.GET.get("order_by")
    all_houses = House.objects.all()
    try:
        if order_index == "1":
            all_houses = all_houses.order_by("price")
        elif order_index == "2":
            all_houses = all_houses.order_by("-price")
        elif order_index == "3":
            all_houses = all_houses.order_by("area")
        elif order_index == "4":
            all_houses = all_houses.order_by("-area")
    except:
        pass
    paginator = Paginator(all_houses, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj":page_obj,
               "order_value":order_index}
    return render(request,"houses/property-grid.html",context)
####################
def about(request):
    return render(request,"houses/about.html")


def userlogin(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            pass
    return render(request,"houses/login.html")

def userregister(request):
    form = UserCreationForm()
    if request.method=="POST":
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        form = UserCreationForm(request.POST)
        form.username = username
        form.password1 = password1
        form.password2 = password2
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
    context = {"form":form}
    return render(request,"houses/register.html",context)

def userlogout(request):
    logout(request)
    return redirect('home')

def Profile(request):
    user = request.user
    context = {"user":user}
    return render(request,"houses/profile.html",context)

def messages(request):
    all_msg = Message.objects.all()
    context = {"all_msgs": all_msg}
    return render(request, "houses/messages.html", context)

def add_house(request):
    form = HouseForm()
    if request.method == "POST":
        list = []  # files is the key of a multi value dictionary, values are the uploaded files
        for f in request.FILES.getlist('files'):  # files is the name of your html file button
            filename = f.name
            list.append(filename)
        print("0000000000000000000000")
        print(list)
        form = HouseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            house = House.objects.all()[House.objects.all().count()-1]
            for other_img in list:
                new_img = Image_of_house(img="images/"+other_img,house=house)
                new_img.save()
            return redirect('properties')
    context = {"form":form}
    return render(request,"houses/add_house.html",context)

"""
def update_property(request,pd):
    form = HouseForm()
    house_to_update = House.objects.get(id=pd)
    if request.method == "POST":
        form = HouseForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('properties')
    context = {"form":form}
    return render(request,"houses/update_property.html",context)
"""

def show_place(request,place):
    if request.method == "POST":
        order_index = request.POST.get("order_by")
        print("------------**/// ",order_index,type(order_index))
    else:
        order_index = request.GET.get("order_by")
    all_in_place = []
    all_houses = House.objects.all()
    try:
        if order_index == "1":
            all_houses = all_houses.order_by("price")
        elif order_index == "2":
            all_houses = all_houses.order_by("-price")
        elif order_index == "3":
            all_houses = all_houses.order_by("area")
        elif order_index == "4":
            all_houses = all_houses.order_by("-area")
    except:
        pass
    for house in all_houses:
        if house.location == place:
            all_in_place.append(house)
    paginator = Paginator(all_in_place, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj,
               "order_value": order_index}
    return render(request,'houses/show_some_places.html',context)

def show_type(request,type_of_place):
    print("                   ,,,",type_of_place)
    if request.method == "POST":
        order_index = request.POST.get("order_by")
        print("------------**/// ",order_index,type(order_index))
    else:
        order_index = request.GET.get("order_by")
    all_in_place = []
    all_houses = House.objects.all()
    try:
        if order_index == "1":
            all_houses = all_houses.order_by("price")
        elif order_index == "2":
            all_houses = all_houses.order_by("-price")
        elif order_index == "3":
            all_houses = all_houses.order_by("area")
        elif order_index == "4":
            all_houses = all_houses.order_by("-area")
    except:
        pass
    for house in all_houses:
        if house.type == type_of_place:
            all_in_place.append(house)
    paginator = Paginator(all_in_place, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj,
               "order_value": order_index}
    return render(request,'houses/show_some_places.html',context)

class update_property(UpdateView):
    model = House
    fields = "__all__"
    template_name = "houses/update_property.html"

    def get_form(self, *args, **kwargs):
        form = super(update_property, self).get_form(*args, **kwargs)
        form.fields["img"].widget.attrs["class"] = "form-control"
        form.fields["type"].widget.attrs["class"] = "form-control"
        form.fields["address"].widget.attrs["class"] = "form-control"
        form.fields["location"].widget.attrs["class"] = "form-control"
        form.fields["status"].widget.attrs["class"] = "form-control"
        form.fields["area"].widget.attrs["class"] = "form-control"
        form.fields["beds"].widget.attrs["class"] = "form-control"
        form.fields["bathrooms"].widget.attrs["class"] = "form-control"
        form.fields["garages"].widget.attrs["class"] = "form-control"
        form.fields["price"].widget.attrs["class"] = "form-control"
        form.fields["description"].widget.attrs["class"] = "form-control"
        form.fields["amenities"].widget.attrs["class"] = "form-control"
        return form

    def get_success_url(self):
        my_property = self.object
        print("#######################")
        print(self.object)
        print(self.request)
        return reverse("single",args=[my_property.id])

class delete_property(DeleteView):
    model = House
    success_url = reverse_lazy('properties')