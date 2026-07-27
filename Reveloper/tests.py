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


class SettingsSecurityTests(TestCase):
    """Pruebas para verificar la externalización de la configuración sensible."""

    def test_debug_conversion_from_string(self):
        test_cases = [
            ('True', True),
            ('true', True),
            ('1', True),
            ('False', False),
            ('false', False),
            ('0', False),
            ('', False),
        ]
        for val, expected in test_cases:
            with self.subTest(val=val):
                res = val.lower() in ('true', '1', 't', 'yes')
                self.assertEqual(res, expected)

    def test_allowed_hosts_parsing(self):
        raw_hosts = 'localhost, 127.0.0.1, example.com '
        parsed = [host.strip() for host in raw_hosts.split(',') if host.strip()]
        self.assertEqual(parsed, ['localhost', '127.0.0.1', 'example.com'])

    def test_test_settings_uses_sqlite_in_memory(self):
        from django.conf import settings
        from django.db import connection

        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')
        self.assertTrue(
            ':memory:' in settings.DATABASES['default']['NAME'] or 'memory' in settings.DATABASES['default']['NAME']
        )
        self.assertEqual(connection.vendor, 'sqlite')

    def test_env_example_does_not_contain_real_secrets(self):
        from django.conf import settings

        env_example_path = settings.BASE_DIR / '.env.example'
        self.assertTrue(env_example_path.exists(), '.env.example debe existir')
        content = env_example_path.read_text(encoding='utf-8')

        self.assertIn('DJANGO_SECRET_KEY=', content)
        self.assertNotIn('DJANGO_SECRET_KEY=django-insecure', content)
        self.assertNotIn(settings.SECRET_KEY, content)
        self.assertIn('DB_PASSWORD=', content)


class TaskLifecycleTests(TestCase):
    """Pruebas automatizadas para el ciclo de vida de tareas (Hito 4)."""

    @classmethod
    def setUpTestData(cls):
        from datetime import date
        from .models import Proyecto, TareaPorDesarrollar, TareasCompletadas

        cls.admin = Usuario.objects.create_superuser(
            username='admin_lifecycle',
            email='admin_lifecycle@test.local',
            password='test-pass-123',
            nombre='Admin',
            apellido='Lifecycle',
        )
        cls.developer = Usuario.objects.create_user(
            username='dev_lifecycle',
            email='dev_lifecycle@test.local',
            password='test-pass-123',
            nombre='Dev',
            apellido='Lifecycle',
        )
        cls.staff_user = Usuario.objects.create_user(
            username='staff_lifecycle',
            email='staff_lifecycle@test.local',
            password='test-pass-123',
            nombre='Staff',
            apellido='Lifecycle',
            is_staff=True,
        )
        cls.inactive_user = Usuario.objects.create_user(
            username='inactive_lifecycle',
            email='inactive_lifecycle@test.local',
            password='test-pass-123',
            nombre='Inactive',
            apellido='Lifecycle',
            is_active=False,
        )
        cls.proyecto = Proyecto.objects.create(
            id='PROY-001',
            nombre='Proyecto Prueba',
            descripcion='Descripción del proyecto',
            fecha_inicio=date.today(),
            fecha_fin=date.today(),
            estado='activo',
        )
        cls.tarea_text_id = 'TASK-TEXT-1001'
        cls.tarea = TareaPorDesarrollar.objects.create(
            id=cls.tarea_text_id,
            usuario=cls.developer,
            proyecto=cls.proyecto,
            titulo='Tarea Texto Inicial',
            descripcion='Descripción inicial',
            fecha_vencimiento=date.today(),
            estado='pendiente',
        )


    def setUp(self):
        self.client = Client()

    def _login(self, user):
        self.assertTrue(
            self.client.login(username=user.username, password='test-pass-123')
        )

    def test_editar_tarea_accepts_string_id(self):
        self._login(self.admin)
        url = reverse('editar_tarea', kwargs={'tarea_id': self.tarea_text_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_edit_task(self):
        url = reverse('editar_tarea', kwargs={'tarea_id': self.tarea_text_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_developer_cannot_edit_task(self):
        self._login(self.developer)
        url = reverse('editar_tarea', kwargs={'tarea_id': self.tarea_text_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_admin_can_open_edit_task_get(self):
        self._login(self.admin)
        url = reverse('editar_tarea', kwargs={'tarea_id': self.tarea_text_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'editar_tarea.html')

    def test_valid_post_modifies_task(self):
        from datetime import date
        self._login(self.admin)
        url = reverse('editar_tarea', kwargs={'tarea_id': self.tarea_text_id})
        post_data = {
            'titulo': 'Tarea Texto Modificada',
            'descripcion': 'Descripción modificada',
            'fecha_vencimiento': str(date.today()),
            'estado': 'en progreso',
            'proyecto': self.proyecto.id,
            'usuario': self.developer.id,
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 302)
        self.tarea.refresh_from_db()
        self.assertEqual(self.tarea.titulo, 'Tarea Texto Modificada')
        self.assertEqual(self.tarea.estado, 'en progreso')

    def test_invalid_post_shows_errors_and_does_not_save(self):
        from datetime import date
        self._login(self.admin)
        url = reverse('editar_tarea', kwargs={'tarea_id': self.tarea_text_id})
        post_data = {
            'titulo': '',
            'descripcion': 'Sin título',
            'fecha_vencimiento': str(date.today()),
            'estado': 'pendiente',
            'proyecto': self.proyecto.id,
            'usuario': self.developer.id,
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('titulo', response.context['form'].errors)
        self.tarea.refresh_from_db()
        self.assertNotEqual(self.tarea.descripcion, 'Sin título')

    def test_crear_tarea_assigns_to_selected_developer(self):
        from datetime import date
        from .models import TareaPorDesarrollar
        self._login(self.admin)
        url = reverse('crear_tarea')
        post_data = {
            'id': 'TASK-NEW-200',
            'titulo': 'Tarea para desarrollador',
            'descripcion': 'Detalle tarea',
            'fecha_vencimiento': str(date.today()),
            'estado': 'pendiente',
            'proyecto': self.proyecto.id,
            'usuario': self.developer.id,
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 302)
        nueva_tarea = TareaPorDesarrollar.objects.filter(titulo='Tarea para desarrollador').first()
        self.assertIsNotNone(nueva_tarea)
        self.assertEqual(nueva_tarea.usuario, self.developer)

    def test_completing_task_creates_exactly_one_tareas_completadas(self):
        from datetime import date
        from .models import TareaPorDesarrollar, TareasCompletadas
        tarea_to_complete = TareaPorDesarrollar.objects.create(
            id='TASK-COMPLETABLE-1',
            usuario=self.developer,
            proyecto=self.proyecto,
            titulo='Tarea a completar',
            fecha_vencimiento=date.today(),
            estado='pendiente',
        )
        self.assertEqual(TareasCompletadas.objects.filter(tarea_original_id=tarea_to_complete.id).count(), 0)

        tarea_to_complete.estado = 'completada'
        tarea_to_complete.save()

        count = TareasCompletadas.objects.filter(tarea_original_id=tarea_to_complete.id).count()
        self.assertEqual(count, 1)

    def test_completing_task_increments_tareas_completadas_counter_once(self):
        from datetime import date
        from .models import TareaPorDesarrollar
        initial_counter = Usuario.objects.get(pk=self.developer.pk).tareas_completadas
        tarea_to_complete = TareaPorDesarrollar.objects.create(
            id='TASK-COMPLETABLE-2',
            usuario=self.developer,
            proyecto=self.proyecto,
            titulo='Tarea contador',
            fecha_vencimiento=date.today(),
            estado='pendiente',
        )

        tarea_to_complete.estado = 'completada'
        tarea_to_complete.save()

        updated_counter = Usuario.objects.get(pk=self.developer.pk).tareas_completadas
        self.assertEqual(updated_counter, initial_counter + 1)

    def test_resaving_completed_task_does_not_duplicate_history_or_counter(self):
        from datetime import date
        from .models import TareaPorDesarrollar, TareasCompletadas
        tarea_completed = TareaPorDesarrollar.objects.create(
            id='TASK-COMPLETABLE-3',
            usuario=self.developer,
            proyecto=self.proyecto,
            titulo='Tarea a resguardar',
            fecha_vencimiento=date.today(),
            estado='pendiente',
        )
        tarea_completed.estado = 'completada'
        tarea_completed.save()

        history_count_before = TareasCompletadas.objects.filter(tarea_original_id=tarea_completed.id).count()
        counter_before = Usuario.objects.get(pk=self.developer.pk).tareas_completadas

        tarea_completed.descripcion = 'Descripción actualizada post completado'
        tarea_completed.save()

        history_count_after = TareasCompletadas.objects.filter(tarea_original_id=tarea_completed.id).count()
        counter_after = Usuario.objects.get(pk=self.developer.pk).tareas_completadas

        self.assertEqual(history_count_after, history_count_before)
        self.assertEqual(counter_after, counter_before)

    def test_superuser_not_in_user_form_queryset(self):
        from .forms import TareaPorDesarrollarForm
        form = TareaPorDesarrollarForm()
        self.assertNotIn(self.admin, form.fields['usuario'].queryset)

    def test_staff_user_not_in_user_form_queryset(self):
        from .forms import TareaPorDesarrollarForm
        form = TareaPorDesarrollarForm()
        self.assertNotIn(self.staff_user, form.fields['usuario'].queryset)

    def test_active_normal_user_in_user_form_queryset(self):
        from .forms import TareaPorDesarrollarForm
        form = TareaPorDesarrollarForm()
        self.assertIn(self.developer, form.fields['usuario'].queryset)

    def test_inactive_user_not_in_user_form_queryset(self):
        from .forms import TareaPorDesarrollarForm
        form = TareaPorDesarrollarForm()
        self.assertNotIn(self.inactive_user, form.fields['usuario'].queryset)

    def test_post_without_user_does_not_create_task(self):
        from datetime import date
        from .models import TareaPorDesarrollar
        self._login(self.admin)
        url = reverse('crear_tarea')
        post_data = {
            'id': 'TASK-NO-USER',
            'titulo': 'Tarea sin usuario',
            'descripcion': 'Detalle',
            'fecha_vencimiento': str(date.today()),
            'estado': 'pendiente',
            'proyecto': self.proyecto.id,
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('usuario', response.context['form'].errors)
        self.assertFalse(TareaPorDesarrollar.objects.filter(id='TASK-NO-USER').exists())

    def test_post_assigning_staff_user_does_not_create_task(self):
        from datetime import date
        from .models import TareaPorDesarrollar
        self._login(self.admin)
        url = reverse('crear_tarea')
        post_data = {
            'id': 'TASK-STAFF-USER',
            'titulo': 'Tarea para staff',
            'descripcion': 'Detalle',
            'fecha_vencimiento': str(date.today()),
            'estado': 'pendiente',
            'proyecto': self.proyecto.id,
            'usuario': self.staff_user.id,
        }
        response = self.client.post(url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('usuario', response.context['form'].errors)
        self.assertFalse(TareaPorDesarrollar.objects.filter(id='TASK-STAFF-USER').exists())


class EvaluationFlowTests(TestCase):
    """Pruebas para el Hito 5: unificar y corregir el flujo de evaluaciones."""

    @classmethod
    def setUpTestData(cls):
        from datetime import date
        from django.utils import timezone
        from .models import Proyecto, Evaluacion

        cls.admin = Usuario.objects.create_superuser(
            username='admin_eval',
            email='admin_eval@test.local',
            password='test-pass-123',
            nombre='Admin',
            apellido='Eval',
        )
        cls.developer = Usuario.objects.create_user(
            username='dev_eval',
            email='dev_eval@test.local',
            password='test-pass-123',
            nombre='Dev',
            apellido='Eval',
        )
        cls.other_developer = Usuario.objects.create_user(
            username='other_dev_eval',
            email='other_dev_eval@test.local',
            password='test-pass-123',
            nombre='Other',
            apellido='Eval',
        )
        cls.proyecto = Proyecto.objects.create(
            id='PROY-EVAL-001',
            nombre='Proyecto Evaluaciones',
            descripcion='Para pruebas de evaluaciones',
            fecha_inicio=date.today(),
            fecha_fin=date.today(),
            estado='activo',
        )
        cls.evaluacion = Evaluacion.objects.create(
            titulo='Evaluación de prueba',
            comentarios='Comentario de prueba',
            fecha_evaluacion=timezone.now(),
            proyecto=cls.proyecto,
            usuario=cls.developer,
            calificacion=80,
        )
        cls.other_evaluacion = Evaluacion.objects.create(
            titulo='Evaluación de other_developer',
            comentarios='Comentario other',
            fecha_evaluacion=timezone.now(),
            proyecto=cls.proyecto,
            usuario=cls.other_developer,
            calificacion=70,
        )

    def setUp(self):
        self.client = Client()

    def _login(self, user):
        self.assertTrue(
            self.client.login(username=user.username, password='test-pass-123')
        )

    # T1 — Existe exactamente una entrada en urlpatterns con name='evaluaciones'
    def test_single_evaluaciones_route_exists(self):
        from Reveloper.urls import urlpatterns
        matches = [p for p in urlpatterns if getattr(p, 'name', None) == 'evaluaciones']
        self.assertEqual(
            len(matches), 1,
            f"Se esperaba exactamente 1 ruta con name='evaluaciones', se encontraron {len(matches)}",
        )

    # T2 — La URL principal resuelve a la vista `evaluaciones`
    def test_evaluaciones_url_resolves_to_correct_view(self):
        from django.urls import resolve
        match = resolve('/reveloper/evaluaciones/')
        self.assertEqual(match.func.__name__, 'evaluaciones')

    # T3 — Un usuario anónimo es redirigido al login
    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(reverse('evaluaciones'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    # T4 — El administrador ve ambas evaluaciones (global)
    def test_admin_sees_all_evaluaciones(self):
        self._login(self.admin)
        response = self.client.get(reverse('evaluaciones'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'evaluaciones.html')
        qs = response.context['evaluaciones']
        self.assertIn(self.evaluacion, qs)
        self.assertIn(self.other_evaluacion, qs)

    # T5 — developer ve su propia evaluación y no la de other_developer
    def test_developer_sees_only_own_evaluaciones(self):
        self._login(self.developer)
        response = self.client.get(reverse('evaluaciones'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'evaluaciones.html')
        qs = response.context['evaluaciones']
        self.assertIn(self.evaluacion, qs)
        self.assertNotIn(self.other_evaluacion, qs)

    # T6 — No existe ruta parametrizada de evaluaciones por ID que exponga datos ajenos
    def test_no_parametrized_evaluaciones_route(self):
        from django.urls import NoReverseMatch
        try:
            reverse('evaluaciones', kwargs={'user_id': self.other_developer.pk})
            self.fail('No debe existir ruta evaluaciones parametrizada por ID de usuario')
        except NoReverseMatch:
            pass  # Correcto: la ruta no existe parametrizada

    # T7 — other_developer ve únicamente su propia evaluación
    def test_other_developer_sees_only_own_evaluaciones(self):
        self._login(self.other_developer)
        response = self.client.get(reverse('evaluaciones'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'evaluaciones.html')
        qs = response.context['evaluaciones']
        self.assertIn(self.other_evaluacion, qs)
        self.assertNotIn(self.evaluacion, qs)

    # T8 — developer no puede ver evaluaciones de other_developer (aislamiento)
    def test_developer_cannot_see_other_developer_evaluaciones(self):
        self._login(self.developer)
        response = self.client.get(reverse('evaluaciones'))
        self.assertEqual(response.status_code, 200)
        qs = response.context['evaluaciones']
        ids_visible = list(qs.values_list('usuario_id', flat=True))
        for uid in ids_visible:
            self.assertEqual(uid, self.developer.pk,
                             'developer no debe ver evaluaciones de otro usuario')

    # T9 — generar_grafico_evaluaciones recibe un desarrollador válido (no un request)
    def test_generar_grafico_evaluaciones_requires_desarrollador_arg(self):
        import inspect
        from .views import generar_grafico_evaluaciones
        sig = inspect.signature(generar_grafico_evaluaciones)
        params = list(sig.parameters.keys())
        self.assertIn('desarrollador', params,
                      'generar_grafico_evaluaciones debe aceptar el parámetro desarrollador')
        self.assertEqual(params[0], 'request')
        self.assertEqual(params[1], 'desarrollador')

    # T10 — No queda ninguna llamada con firma incorrecta (sin desarrollador)
    def test_no_incompatible_calls_to_graph_function(self):
        """Verifica que no existe ninguna llamada a generar_grafico_evaluaciones(request)
        sin el argumento desarrollador en views.py."""
        import re
        import os
        views_path = os.path.join(os.path.dirname(__file__), 'views.py')
        with open(views_path, encoding='utf-8') as f:
            source = f.read()
        bad_calls = re.findall(
            r'generar_grafico_evaluaciones\s*\(\s*request\s*\)',
            source
        )
        self.assertEqual(bad_calls, [],
                         f'Llamadas incompatibles encontradas: {bad_calls}')

    # T11 — El nombre vista_evaluaciones no existe en el sistema de rutas
    def test_vista_evaluaciones_route_does_not_exist(self):
        from django.urls import NoReverseMatch
        with self.assertRaises(NoReverseMatch):
            reverse('vista_evaluaciones')
