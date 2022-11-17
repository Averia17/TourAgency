from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from hotels.views import HotelsViewSet, RoomViewSet
from locations.views import ContinentViewSet
from orders.views import OrderViewSet, OrderPriceView
from tour_agency import settings
from tours.arrival_dates.views import ArrivalDateViewSet
from tours.views import TourViewSet
from users.views import (
    UserViewSet,
    CustomTokenObtainPairView,
    GoogleLoginView,
    ResetPasswordViewSet,
)

router = SimpleRouter()
router.register("users", UserViewSet)
router.register("hotels", HotelsViewSet)
router.register("rooms", RoomViewSet)
router.register("tours", TourViewSet)
router.register("continents", ContinentViewSet)
router.register("arrivals", ArrivalDateViewSet)
router.register("orders", OrderViewSet)
router.register("reset-password", ResetPasswordViewSet, "reset-password")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token-verify/", TokenVerifyView.as_view(), name="token-verify"),
    path("api/login/google/", GoogleLoginView.as_view(), name="login-with-google"),
    path("api/order/price/", OrderPriceView.as_view(), name="order-price"),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
