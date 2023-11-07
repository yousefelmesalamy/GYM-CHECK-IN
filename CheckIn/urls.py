from django.urls import path, re_path
from django.conf.urls.static import static
from rest_framework import routers
from .views import *
#knox
# from knox import views as knox_views
router = routers.DefaultRouter()

router.register(r'inmembership', InmemberShipViewSet, basename='inmembership')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
     # path('login/', LoginView.as_view(), name='knox_login'),
     # path('logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
     # path('logoutall/', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
     path('check_in/<int:subscriber_id>/', check_in, name='check_in'),
     path('id_ask/', ask_for_id, name='id_ask'),

]
urlpatterns += router.urls
