from rest_framework.routers import DefaultRouter

from apps.guest.views import ItemViewSet, CategoriesViewSet, OrderViewSet

router = DefaultRouter()
router.register('items', ItemViewSet, 'guest-items')
router.register('categories', CategoriesViewSet, 'guest-categories')
router.register('orders', OrderViewSet, 'guest-orders')

urlpatterns = router.urls
