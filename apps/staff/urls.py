from rest_framework.routers import DefaultRouter

from apps.staff.views import ItemViewSet, \
    OccupationViewSet, \
    OrderViewSet, \
    RestaurantViewSet, \
    RestaurantUserViewSet, \
    TableViewSet

router = DefaultRouter()

router.register(
    'items', ItemViewSet, 'staff-items'
)
router.register(
    'occupations', OccupationViewSet, 'staff-occupations'
)
router.register(
    'orders', OrderViewSet, 'staff-orders'
)
router.register(
    'restaurants', RestaurantViewSet, 'staff-restaurants'
)
router.register(
    'restaurant-users', RestaurantUserViewSet, 'staff-restautant-users'
)
router.register(
    'tables', TableViewSet, 'staff-tables'
)

urlpatterns = router.urls
