"""Chay trong container app: python - < scripts/test-web-auth.py. Khong ghi DB."""
import unittest
from unittest.mock import patch
from werkzeug.security import generate_password_hash
from app import app, USERS


class AuthorizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hashed = generate_password_hash('test-only-password')

    def setUp(self):
        self.client = app.test_client()
        self.users = patch.dict(USERS, {
            'test_admin': {'role': 'admin', 'password_hash': self.hashed},
            'test_staff': {'role': 'staff', 'password_hash': self.hashed},
        }, clear=True)
        self.users.start()
        self.addCleanup(self.users.stop)
        quiet_logger = patch.object(app.logger, 'disabled', True)
        quiet_logger.start()
        self.addCleanup(quiet_logger.stop)

    def session(self, user):
        with self.client.session_transaction() as session:
            session['username'] = user
            session['csrf_token'] = 'test-csrf'

    def test_anonymous_cannot_reach_business_routes(self):
        with patch('app.connect') as connection:
            for path in ['/', '/khach-hang', '/thu-cung', '/dich-vu', '/lich-hen', '/khach-hang/them', '/khach-hang/1/sua']:
                response = self.client.get(path)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.location.endswith('/dang-nhap'))
            self.assertEqual(self.client.post('/khach-hang/1/xoa').status_code, 401)
            connection.assert_not_called()

    def test_staff_delete_denied_before_database_even_with_forged_role(self):
        self.session('test_staff')
        with self.client.session_transaction() as session:
            session['role'] = 'admin'
        with patch('app.connect') as connection:
            for slug in ['khach-hang', 'thu-cung', 'dich-vu', 'lich-hen']:
                self.assertEqual(self.client.post('/' + slug + '/1/xoa', data={'csrf_token': 'test-csrf'}).status_code, 403)
            connection.assert_not_called()

    def test_admin_delete_route_is_permitted_with_mocked_database(self):
        self.session('test_admin')
        with patch('app.connect') as connection:
            connection.return_value.__enter__.return_value.execute.return_value.rowcount = 1
            self.assertEqual(self.client.post('/khach-hang/1/xoa', data={'csrf_token': 'test-csrf'}).status_code, 302)
            connection.assert_called_once()

    def test_staff_can_open_create_and_edit_forms_with_mocked_database(self):
        self.session('test_staff')
        with patch('app.connect') as connection:
            db = connection.return_value.__enter__.return_value
            db.execute.return_value.__iter__.return_value = iter([])
            db.execute.return_value.fetchone.return_value = {'id': 1, 'full_name': 'mock', 'phone': 'mock'}
            self.assertEqual(self.client.get('/khach-hang/them').status_code, 200)
            self.assertEqual(self.client.get('/khach-hang/1/sua').status_code, 200)

    def test_login_success_failure_and_logout(self):
        self.client.get('/dang-nhap')
        with self.client.session_transaction() as session:
            token = session['csrf_token']
        self.assertEqual(self.client.post('/dang-nhap', data={'username': 'test_admin', 'password': 'wrong', 'csrf_token': token}).status_code, 401)
        self.assertEqual(self.client.post('/dang-nhap', data={'username': 'test_admin', 'password': 'test-only-password', 'csrf_token': token}).status_code, 302)
        with self.client.session_transaction() as session:
            self.assertEqual(session['username'], 'test_admin')
            self.assertNotIn('csrf_token', session)
        self.assertEqual(self.client.post('/dang-xuat').status_code, 400)
        self.client.get('/dang-nhap')
        # Login redirects when already authenticated; create token through a rendered page.
        with self.client.session_transaction() as session:
            session['csrf_token'] = 'logout-csrf'
        self.assertEqual(self.client.post('/dang-xuat', data={'csrf_token': 'logout-csrf'}).status_code, 302)
        self.assertEqual(self.client.get('/khach-hang').status_code, 302)

    def test_health_is_public_but_business_post_requires_csrf(self):
        with patch('app.connect'):
            self.assertEqual(self.client.get('/health').status_code, 200)
        self.session('test_admin')
        with patch('app.connect') as connection:
            self.assertEqual(self.client.post('/khach-hang/1/xoa').status_code, 400)
            connection.assert_not_called()


unittest.main()
