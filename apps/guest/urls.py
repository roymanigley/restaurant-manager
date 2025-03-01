from rest_framework.routers import DefaultRouter

from apps.guest.views import ItemViewSet, CategoriesViewSet, OrderViewSet, OccupationViewSet

router = DefaultRouter()
router.register('items', ItemViewSet, 'guest-items')
router.register('categories', CategoriesViewSet, 'guest-categories')
router.register('orders', OrderViewSet, 'guest-orders')
router.register('occupations', OccupationViewSet, 'guest-occupations')

urlpatterns = router.urls
