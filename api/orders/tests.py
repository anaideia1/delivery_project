import datetime

from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse

from api.orders.models import Order
from api.orders.services import delayed_orders_change_status


def get_user_access_token(client, email, password):
    User = get_user_model()
    user = User.objects.create_user(
        email=email, password=password
    )
    credentials = {'email': user.email, 'password': password}
    response = client.post(
        reverse('user-login'),
        data=credentials
    )
    return response.json().get('access')

class OrderNewTests(TestCase):
    url_name = 'order-new'

    def setUp(self):
        client = Client()
        self.access_token = get_user_access_token(
            client,
            'test@user.com',
            'password',
        )
        self.order_data = {
            'sku': '1qwerty2',
            'name': 'example',
            'price': 12.33,
            'delivery_date': datetime.date.today().strftime(
                settings.DATE_FORMAT
            ),
        }

    def _order_objects_count(self, orders_number):
        orders = Order.objects.all()
        self.assertEqual(orders.count(), orders_number)

    def test_create_order_200(self):
        response = self.client.post(
            reverse(self.url_name),
            data=self.order_data,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 201)
        self._order_objects_count(1)

    def test_create_order_sku(self):
        self.order_data['sku'] = '1qwerty'
        response = self.client.post(
            reverse(self.url_name),
            data=self.order_data,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 400)
        self._order_objects_count(0)

    def test_create_order_sku_unique(self):
        self.client.post(
            reverse(self.url_name),
            data=self.order_data,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        response = self.client.post(
            reverse(self.url_name),
            data=self.order_data,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 400)
        self._order_objects_count(1)

    def test_create_order_name(self):
        self.order_data.pop('name')
        response = self.client.post(
            reverse(self.url_name),
            data=self.order_data,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 400)
        self._order_objects_count(0)

    def test_create_order_price(self):
        self.order_data.pop('price')
        response = self.client.post(
            reverse(self.url_name),
            data=self.order_data,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 400)
        self._order_objects_count(0)

    def test_create_order_price_decimal_places(self):
        self.order_data['price'] = 12.3333
        response = self.client.post(
            reverse(self.url_name),
            data=self.order_data,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 400)
        self._order_objects_count(0)

    def test_create_order_delivery_date(self):
        self.order_data.pop('delivery_date')
        response = self.client.post(
            reverse(self.url_name),
            data=self.order_data,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 400)
        self._order_objects_count(0)

    def test_create_order_delivery_date_format(self):
        self.order_data['delivery_date'] = datetime.datetime.now().strftime(
            '%Y-%m-%d'
        )
        response = self.client.post(
            reverse(self.url_name),
            data=self.order_data,
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 400)
        self._order_objects_count(0)

    def test_create_order_401(self):
        response = self.client.post(
            reverse(self.url_name),
            data=self.order_data,
        )
        self.assertEqual(response.status_code, 401)
        self._order_objects_count(0)


class OrderDetailTests(TestCase):
    url_name = 'order-detail'

    def setUp(self):
        client = Client()
        self.access_token = get_user_access_token(
            client,
            'test@user.com',
            'password',
        )
        self.order_data = {
            'sku': '1qwerty2',
            'name': 'example',
            'price': 12.33,
            'delivery_date': datetime.date.today()
        }
        self.order = Order.objects.create(**self.order_data)

    def test_create_order_200(self):
        response = self.client.get(
            reverse(self.url_name, args=(self.order.id, )),
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data.get('id'), int)
        self.assertEqual(data.get('sku'), self.order_data.get('sku'))
        self.assertEqual(data.get('example'), self.order_data.get('example'))
        self.assertEqual(
            float(data.get('price')), self.order_data.get('price')
        )
        self.assertIsNotNone(data.get('delivery_date'))
        self.assertEqual(data.get('status'), Order.CREATED)

    def test_create_order_404(self):
        response = self.client.get(
            reverse(self.url_name, args=(self.order.id + 1, )),
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        self.assertEqual(response.status_code, 404)

    def test_create_order_401(self):
        response = self.client.get(
            reverse(self.url_name, args=(self.order.id, )),
        )
        self.assertEqual(response.status_code, 401)


class DelayedOrdersStatusChangeTests(TestCase):
    def setUp(self):
        self.old_order_data = {
            'sku': '12prev34',
            'name': 'fromage',
            'price': 9.99,
            'delivery_date': datetime.date.today() - datetime.timedelta(days=1)
        }
        self.order_data = {
            'sku': '1qwerty2',
            'name': 'example',
            'price': 12.33,
            'delivery_date': datetime.date.today()
        }
        self.old_order = Order.objects.create(**self.old_order_data)
        self.order = Order.objects.create(**self.order_data)

    def test_delayed_orders_status_change(self):
        self.assertEqual(self.old_order.status, Order.CREATED)
        self.assertEqual(self.order.status, Order.CREATED)
        delayed_orders_change_status()
        self.old_order.refresh_from_db()
        self.order.refresh_from_db()
        self.assertEqual(self.old_order.status, Order.DELAYED)
        self.assertEqual(self.order.status, Order.CREATED)
