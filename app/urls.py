from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views
from django.urls import path
from .views import logout_view
from .forms import LoginForm,MyPasswordChangeForm
from django.urls import path
from . import views
urlpatterns = [
    path('',views.ProductView.as_view(), name="home"),
    #path('product-detail/<int:pk>', views.productdetailView.as_view(), name='product-detail'),
    path('product/<int:pk>/',views.ProductDetailView.as_view(), name='product-detail'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart, name='showcart'),
    path('pluscart/',views.plus_cart),

    path('buy/', views.buy_now, name='buy-now'),
    path('contactus/', views.contactus, name='contactus'),
    path('aboutus/', views.aboutus, name='aboutus'),

    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    #path('paymentdone/',views.my_view, name='my_view'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),

    #path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
     path('logout/', logout_view, name='logout'),
     path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'), name='passwordchange'),

     path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'), name='passwordchangedone'),


    
    path('registration/',views.customerRegistrationView.as_view(), name="customerregistration")
    ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

