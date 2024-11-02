from apps.core.models import Restaurant, RestaurantUser

try:
    restaurant = Restaurant.objects.create(
        name='DEFAULT'
    )
    user = RestaurantUser.objects.create(
        username='admin',
        first_name='Roy',
        last_name='Manigley',
        is_superuser=True,
        is_staff=True,
        restaurant=restaurant
    )
    user.set_password('admin')
    user.save()
    print('[+] created user "admin" with password "admin"')
except Exception as e:
    print(f'[!] created user failed: {e}')
