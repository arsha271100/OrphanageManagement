from . import views
from django.urls import path

urlpatterns = [
    path('orphanagehome/', views.orphanagehome,name='orphanagehome'),
    path('',views.index,name='index'),
    path('reg/', views.reg,name='reg'),
    path('login/', views.login,name='login'),
    path('donorhome/', views.donorhome,name='donorhome'),
    path('logout/', views.logout, name='logout'),
    path('selectdistrict',views.selectdistrict,name='selectdistrict'),
    path('load-orphanages/', views.load_orphanages, name='ajax_load_orphanages'),
    path('vol_chooseorphan',views.vol_chooseorphan,name='vol_chooseorphan'),
    path('vol_load-orphanages/', views.vol_load_orphanages, name='vol_load_orphanages'),
    path('vol_viewdonations',views.vol_viewdonations,name='vol_viewdonations'),
    path('vieworphanage',views.vieworphanage,name='vieworphanage'),
    path('viewdonations/',views.viewdonations,name='viewdonations'),
    path('donatehome/', views.donatehome,name='donatehome'),
    path('volunteerreg/', views.volunteerreg,name='volunteerreg'),
    path('volunteerhome/', views.volunteerhome,name='volunteerhome'),
    path('volunteer_login/', views.volunteer_login,name='volunteer_login'),
    path('donate/<int:id>/', views.donate,name='donate'),
    path('profile', views.profile,name='profile'),
    path('address/', views.address,name='address'),
    path('volunteer_logout/', views.volunteer_logout,name='volunteer_logout'),
    path('generateOTP',views.generateOTP,name='generateOTP'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('change_password',views.change_password,name='change_password'),
    path('deleteaddress/<int:id>/',views.deleteaddress,name='deleteaddress'),
    path('donate_approve/<int:id>/',views.donate_approve,name='donate_approve'),
    path('forgotpassword/', views.forgotpassword, name='forgotpassword'),
    path('verify_forgot_otp/', views.verify_forgot_otp, name='verify_forgot_otp'),
    path('new_password/', views.new_password, name='new_password'),
    path('Donate_Money/<int:id>/', views.Donate_Money, name='Donate_Money'),
    path('pay_money/<int:id>/', views.pay_money, name='pay_money'),

    
    
    # path('add/', views.orphanage_create_view, name='orphanage_add'),
    # path('<int:pk>/', views.orphanage_update_view, name='orphanage_change'),
    
    
    # path('ajax/load-cities/', views.load_cities, name='ajax_load_cities'), # AJAX
]
