from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="home"),
    path('property/<int:id>', views.single,name="single"),
    #path('properties', views.propertiesView.as_view(),name="properties"),
    path('properties', views.list_properties,name="properties"),
    path('about', views.about,name="about"),

    path('add_house', views.add_house,name="add_house"),

    path('update_property/<int:pk>', views.update_property.as_view(),name="update_property"),

    path('delete_property/<int:pk>', views.delete_property.as_view(),name="delete_property"),

    path('userlogin', views.userlogin,name="userlogin"),
    path('userregister', views.userregister,name="userregister"),
    path('userlogout', views.userlogout,name="userlogout"),
    path('Profile', views.Profile,name="Profile"),
    path('messages', views.messages,name="messages"),


    path('search-for', views.search_for,name="search_for"),
    path('get-inquiry', views.get_inquiry,name="get_inquiry"),
    path('show-all-inquiry', views.show_all_inquiry,name="show_all_inquiry"),

    path('write-msg', views.write_msg,name="write_msg"),

    path('show-place/<str:place>', views.show_place,name="show_place"),
    path('show-type/<str:type_of_place>', views.show_type,name="show_type"),
]