from rest_framework.routers import DefaultRouter

from coderockr.core import views

app_name = "core"

router = DefaultRouter()
router.register(r"investments", views.InvestmentViewSet, basename="investment")
urlpatterns = router.urls
