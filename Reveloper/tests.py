from django.test import TestCase, Client
from django.urls import reverse

from .models import Usuario


class ExportEndpointSecurityTests(TestCase):
    """Pruebas mínimas de autenticación y autorización en exportaciones."""

    GLOBAL_ADMIN_URL_NAMES = [
        'generate_pdf',
        'generate_user_pdf',
        'generar_informe_grafico_pdf_admin',
        'exportar_tareas_excel',
        'exportar_proyectos_excel',
        'exportar_usuarios_excel',
        'exportar_todos_usuarios_excel',
        'exportar_todos_proyectos_excel',
        'exportar_todas_tareas_excel',
        'exportar_todas_evaluaciones_excel',
        'generar_informe_pdf_busqueda',
        'generar_informe_pdf_tareas',
        'generar_informe_pdf_usuarios',
    ]

    DEVELOPER_OWN_URL_NAMES = [
        'generate_task_pdf',
        'generate_evaluation_pdf',
        'generar_informe_grafico_pdf',
    ]

    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_superuser(
            username='admin_test',
            email='admin@test.local',
            password='test-pass-123',
            nombre='Admin',
            apellido='Test',
        )
        cls.developer = Usuario.objects.create_user(
            username='dev_test',
            email='dev@test.local',
            password='test-pass-123',
            nombre='Dev',
            apellido='Test',
        )

    def setUp(self):
        self.client = Client()

    def _login(self, user):
        self.assertTrue(
            self.client.login(username=user.username, password='test-pass-123')
        )

    def test_anonymous_redirects_to_login_on_global_exports(self):
        for url_name in self.GLOBAL_ADMIN_URL_NAMES:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 302)
                self.assertIn('/accounts/login/', response.url)

    def test_anonymous_redirects_to_login_on_developer_exports(self):
        for url_name in self.DEVELOPER_OWN_URL_NAMES:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 302)
                self.assertIn('/accounts/login/', response.url)

    def test_developer_cannot_access_global_exports(self):
        self._login(self.developer)
        for url_name in self.GLOBAL_ADMIN_URL_NAMES:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 302)
                self.assertIn('/accounts/login/', response.url)

    def test_developer_can_access_own_scoped_exports(self):
        self._login(self.developer)
        for url_name in self.DEVELOPER_OWN_URL_NAMES:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)

    def test_admin_can_access_global_exports(self):
        self._login(self.admin)
        for url_name in self.GLOBAL_ADMIN_URL_NAMES:
            with self.subTest(url_name=url_name):
                response = self.client.get(reverse(url_name))
                self.assertEqual(response.status_code, 200)

    def test_print_template_dirs_route_removed(self):
        response = self.client.get('/reveloper/print-template-dirs/')
        self.assertEqual(response.status_code, 404)
