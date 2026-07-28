from reportlab.lib import colors
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

    def test_pending_task_does_not_create_completed_history(self):
        from datetime import date
        from .models import TareaPorDesarrollar, TareasCompletadas

        tarea = TareaPorDesarrollar.objects.create(
            id='TASK-PENDING-NO-HISTORY',
            usuario=self.developer,
            proyecto=self.proyecto,
            titulo='Tarea pendiente sin historial',
            fecha_vencimiento=date.today(),
            estado='pendiente',
        )

        self.assertFalse(
            TareasCompletadas.objects.filter(
                tarea_original_id=tarea.id
            ).exists()
        )

    def test_completed_history_preserves_basic_task_data(self):
        from datetime import date
        from django.utils import timezone
        from .models import TareaPorDesarrollar, TareasCompletadas

        fecha_vencimiento = date.today()
        tarea = TareaPorDesarrollar.objects.create(
            id='TASK-HISTORY-DATA',
            usuario=self.developer,
            proyecto=self.proyecto,
            titulo='Tarea con datos históricos',
            fecha_vencimiento=fecha_vencimiento,
            estado='pendiente',
        )

        tarea.estado = 'completada'
        tarea.save()

        historial = TareasCompletadas.objects.get(
            tarea_original_id=tarea.id
        )

        self.assertEqual(historial.titulo, tarea.titulo)
        self.assertEqual(historial.estado, 'completada')
        self.assertEqual(historial.usuario, self.developer)
        self.assertEqual(
            timezone.localdate(historial.fecha_entrega),
            fecha_vencimiento,
        )

    def test_changing_completed_task_to_another_state_does_not_increment_again(
        self
    ):
        from datetime import date
        from .models import TareaPorDesarrollar, TareasCompletadas

        tarea = TareaPorDesarrollar.objects.create(
            id='TASK-COMPLETED-REVERTED',
            usuario=self.developer,
            proyecto=self.proyecto,
            titulo='Tarea completada y revertida',
            fecha_vencimiento=date.today(),
            estado='pendiente',
        )

        initial_counter = Usuario.objects.get(
            pk=self.developer.pk
        ).tareas_completadas

        tarea.estado = 'completada'
        tarea.save()

        counter_after_completion = Usuario.objects.get(
            pk=self.developer.pk
        ).tareas_completadas

        tarea.estado = 'en revision'
        tarea.save()

        final_counter = Usuario.objects.get(
            pk=self.developer.pk
        ).tareas_completadas

        self.assertEqual(
            counter_after_completion,
            initial_counter + 1,
        )
        self.assertEqual(
            final_counter,
            counter_after_completion,
        )
        self.assertEqual(
            TareasCompletadas.objects.filter(
                tarea_original_id=tarea.id
            ).count(),
            1,
        )

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


class SearchFilterModuleTests(TestCase):
    """Pruebas estructurales del módulo compartido de filtros."""

    def test_filter_helpers_live_in_filters_module(self):
        from .filters import (
            _parsear_fecha_filtro,
            _filtrar_usuarios,
            _filtrar_proyectos,
            _filtrar_tareas,
        )

        helpers = (
            _parsear_fecha_filtro,
            _filtrar_usuarios,
            _filtrar_proyectos,
            _filtrar_tareas,
        )

        for helper in helpers:
            with self.subTest(helper=helper.__name__):
                self.assertEqual(
                    helper.__module__,
                    'Reveloper.filters',
                )

    def test_views_import_filter_helpers(self):
        from pathlib import Path

        views_path = Path(__file__).resolve().parent / 'views.py'
        source = views_path.read_text(encoding='utf-8')

        self.assertIn('from .filters import (', source)
        self.assertNotIn(
            'def _parsear_fecha_filtro',
            source,
        )
        self.assertNotIn(
            'def _filtrar_usuarios',
            source,
        )
        self.assertNotIn(
            'def _filtrar_proyectos',
            source,
        )
        self.assertNotIn(
            'def _filtrar_tareas',
            source,
        )


class ProjectTaskDateFilterTests(TestCase):
    """Pruebas del Hito 9: filtros seguros de proyectos y tareas."""

    @classmethod
    def setUpTestData(cls):
        from datetime import date, datetime
        from django.utils import timezone
        from .models import Proyecto, TareaPorDesarrollar

        cls.admin = Usuario.objects.create_superuser(
            username='admin_date_filters',
            email='admin_date_filters@test.local',
            password='test-pass-123',
            nombre='Admin',
            apellido='Filtros',
        )
        cls.developer = Usuario.objects.create_user(
            username='developer_date_filters',
            email='developer_date_filters@test.local',
            password='test-pass-123',
            nombre='Developer',
            apellido='Filtros',
        )

        cls.proyecto_enero = Proyecto.objects.create(
            id='PROY-DATE-001',
            nombre='Proyecto Enero',
            descripcion='Proyecto de enero',
            fecha_inicio=date(2026, 1, 10),
            fecha_fin=date(2026, 1, 31),
            estado='activo',
        )
        cls.proyecto_febrero = Proyecto.objects.create(
            id='PROY-DATE-002',
            nombre='Proyecto Febrero',
            descripcion='Proyecto de febrero',
            fecha_inicio=date(2026, 2, 10),
            fecha_fin=date(2026, 2, 28),
            estado='activo',
        )

        cls.tarea_enero = TareaPorDesarrollar.objects.create(
            id='TASK-DATE-001',
            usuario=cls.developer,
            proyecto=cls.proyecto_enero,
            titulo='Tarea Enero',
            descripcion='Tarea de enero',
            fecha_vencimiento=date(2026, 1, 31),
            estado='pendiente',
        )
        cls.tarea_febrero = TareaPorDesarrollar.objects.create(
            id='TASK-DATE-002',
            usuario=cls.developer,
            proyecto=cls.proyecto_febrero,
            titulo='Tarea Febrero',
            descripcion='Tarea de febrero',
            fecha_vencimiento=date(2026, 2, 28),
            estado='pendiente',
        )

        TareaPorDesarrollar.objects.filter(
            pk=cls.tarea_enero.pk
        ).update(
            fecha_creacion=timezone.make_aware(
                datetime(2026, 1, 15, 10, 0)
            )
        )
        TareaPorDesarrollar.objects.filter(
            pk=cls.tarea_febrero.pk
        ).update(
            fecha_creacion=timezone.make_aware(
                datetime(2026, 2, 15, 10, 0)
            )
        )

        cls.tarea_enero.refresh_from_db()
        cls.tarea_febrero.refresh_from_db()

    def setUp(self):
        self.client = Client()
        self.assertTrue(
            self.client.login(
                username=self.admin.username,
                password='test-pass-123',
            )
        )

    def test_project_start_date_filters_results(self):
        response = self.client.get(
            reverse('buscar_proyectos'),
            {'fecha_inicio_desde': '2026-02-01'},
        )
        resultados = response.context['resultados']

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.proyecto_febrero, resultados)
        self.assertNotIn(self.proyecto_enero, resultados)

    def test_project_end_date_filters_results(self):
        response = self.client.get(
            reverse('buscar_proyectos'),
            {'fecha_inicio_hasta': '2026-01-31'},
        )
        resultados = response.context['resultados']

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.proyecto_enero, resultados)
        self.assertNotIn(self.proyecto_febrero, resultados)

    def test_invalid_project_date_returns_empty_without_error(self):
        response = self.client.get(
            reverse('buscar_proyectos'),
            {'fecha_inicio_desde': '2026-02-31'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            response.context['resultados'].exists()
        )

    def test_task_start_date_filters_results(self):
        response = self.client.get(
            reverse('buscar_tareas'),
            {'fecha_inicio_desde_tarea': '2026-02-01'},
        )
        resultados = response.context['resultados_tareas']

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tarea_febrero, resultados)
        self.assertNotIn(self.tarea_enero, resultados)

    def test_task_end_date_filters_results(self):
        response = self.client.get(
            reverse('buscar_tareas'),
            {'fecha_inicio_hasta_tarea': '2026-01-31'},
        )
        resultados = response.context['resultados_tareas']

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.tarea_enero, resultados)
        self.assertNotIn(self.tarea_febrero, resultados)

    def test_invalid_task_date_returns_empty_without_error(self):
        response = self.client.get(
            reverse('buscar_tareas'),
            {'fecha_inicio_desde_tarea': 'fecha-invalida'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            response.context['resultados_tareas'].exists()
        )

    def test_project_excel_accepts_invalid_dates(self):
        response = self.client.get(
            reverse('exportar_proyectos_excel'),
            {
                'fecha_inicio_desde': '2026-02-31',
                'fecha_inicio_hasta': 'fecha-invalida',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    def test_task_excel_accepts_invalid_dates(self):
        response = self.client.get(
            reverse('exportar_tareas_excel'),
            {
                'fecha_inicio_desde_tarea': '2026-02-31',
                'fecha_inicio_hasta_tarea': 'fecha-invalida',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    def test_searches_and_exports_reuse_shared_filters(self):
        import inspect
        from .views import (
            buscar_proyectos,
            buscar_tareas,
            exportar_proyectos_excel,
            exportar_tareas_excel,
        )

        expected_helpers = (
            (buscar_proyectos, '_filtrar_proyectos('),
            (exportar_proyectos_excel, '_filtrar_proyectos('),
            (buscar_tareas, '_filtrar_tareas('),
            (exportar_tareas_excel, '_filtrar_tareas('),
        )

        for view, helper_name in expected_helpers:
            with self.subTest(view=view.__name__):
                self.assertIn(
                    helper_name,
                    inspect.getsource(view),
                )

    def test_project_pdf_works_without_previous_search(self):
        response = self.client.get(
            reverse('generar_informe_pdf_busqueda'),
            {'fecha_inicio_desde': '2026-02-01'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/pdf',
        )

    def test_task_pdf_works_without_previous_search(self):
        response = self.client.get(
            reverse('generar_informe_pdf_tareas'),
            {'fecha_inicio_desde_tarea': '2026-02-01'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/pdf',
        )

    def test_project_pdf_reuses_shared_filter(self):
        import inspect
        from .views import generar_informe_pdf_busqueda

        source = inspect.getsource(
            generar_informe_pdf_busqueda
        )

        self.assertIn('_filtrar_proyectos(', source)
        self.assertNotIn('request.session', source)

    def test_task_pdf_reuses_shared_filter(self):
        import inspect
        from .views import generar_informe_pdf_tareas

        source = inspect.getsource(
            generar_informe_pdf_tareas
        )

        self.assertIn('_filtrar_tareas(', source)
        self.assertNotIn('request.session', source)

    def test_project_and_task_searches_do_not_store_results_in_session(self):
        import inspect
        from .views import buscar_proyectos, buscar_tareas

        for view in (buscar_proyectos, buscar_tareas):
            with self.subTest(view=view.__name__):
                source = inspect.getsource(view)
                self.assertNotIn('request.session', source)


class UserSearchFilterTests(TestCase):
    """Pruebas del Hito 6: búsqueda y exportación filtrada de usuarios."""

    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_superuser(
            username='admin_search',
            email='admin_search@test.local',
            password='test-pass-123',
            nombre='Administrador',
            apellido='Principal',
        )
        cls.developer = Usuario.objects.create_user(
            username='roberto_dev',
            email='roberto.gonzalez@test.local',
            password='test-pass-123',
            nombre='Roberto',
            apellido='González',
        )
        cls.other_developer = Usuario.objects.create_user(
            username='maria_code',
            email='maria.soto@test.local',
            password='test-pass-123',
            nombre='María',
            apellido='Soto',
        )
        from datetime import datetime
        from django.utils import timezone

        Usuario.objects.filter(pk=cls.admin.pk).update(
            fecha_creacion=timezone.make_aware(
                datetime(2026, 1, 5, 10, 0)
            )
        )
        Usuario.objects.filter(pk=cls.developer.pk).update(
            fecha_creacion=timezone.make_aware(
                datetime(2026, 1, 15, 10, 0)
            )
        )
        Usuario.objects.filter(pk=cls.other_developer.pk).update(
            fecha_creacion=timezone.make_aware(
                datetime(2026, 2, 10, 10, 0)
            )
        )

        cls.admin.refresh_from_db()
        cls.developer.refresh_from_db()
        cls.other_developer.refresh_from_db()

    def setUp(self):
        self.client = Client()

    def _login(self, user):
        self.assertTrue(
            self.client.login(
                username=user.username,
                password='test-pass-123',
            )
        )

    def _search(self, term):
        self._login(self.admin)
        return self.client.get(
            reverse('buscar_usuarios'),
            {'nombre_o_apellido': term},
        )

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse('buscar_usuarios'))

        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_developer_cannot_access_global_user_search(self):
        self._login(self.developer)

        response = self.client.get(reverse('buscar_usuarios'))

        self.assertEqual(response.status_code, 302)

    def test_admin_can_access_global_user_search(self):
        self._login(self.admin)

        response = self.client.get(reverse('buscar_usuarios'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'busqueda.html')

    def test_search_by_nombre(self):
        response = self._search('Roberto')
        usuarios = response.context['resultados_usuarios']

        self.assertIn(self.developer, usuarios)
        self.assertNotIn(self.other_developer, usuarios)

    def test_search_by_apellido(self):
        response = self._search('Soto')
        usuarios = response.context['resultados_usuarios']

        self.assertIn(self.other_developer, usuarios)
        self.assertNotIn(self.developer, usuarios)

    def test_search_by_username(self):
        response = self._search('roberto_dev')
        usuarios = response.context['resultados_usuarios']

        self.assertIn(self.developer, usuarios)
        self.assertNotIn(self.other_developer, usuarios)

    def test_search_by_email(self):
        response = self._search('maria.soto@test.local')
        usuarios = response.context['resultados_usuarios']

        self.assertIn(self.other_developer, usuarios)
        self.assertNotIn(self.developer, usuarios)

    def test_search_is_partial(self):
        response = self._search('bert')
        usuarios = response.context['resultados_usuarios']

        self.assertIn(self.developer, usuarios)

    def test_search_is_case_insensitive(self):
        response = self._search('rObErTo')
        usuarios = response.context['resultados_usuarios']

        self.assertIn(self.developer, usuarios)

    def test_empty_term_returns_all_users_without_error(self):
        response = self._search('')
        usuarios = response.context['resultados_usuarios']

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.admin, usuarios)
        self.assertIn(self.developer, usuarios)
        self.assertIn(self.other_developer, usuarios)

    def test_whitespace_term_returns_all_users_without_error(self):
        response = self._search('   ')
        usuarios = response.context['resultados_usuarios']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(usuarios.count(), Usuario.objects.count())

    def test_search_without_matches_returns_empty_queryset(self):
        response = self._search('usuario-inexistente')
        usuarios = response.context['resultados_usuarios']

        self.assertEqual(response.status_code, 200)
        self.assertFalse(usuarios.exists())
        self.assertContains(
            response,
            'No se encontraron usuarios con los criterios ingresados.',
        )

    def test_search_preserves_filter_value_in_template(self):
        response = self._search('Roberto')

        self.assertContains(
            response,
            'value="Roberto"',
            html=False,
        )

    def test_excel_uses_real_user_fields_and_filter(self):
        from io import BytesIO
        import openpyxl

        self._login(self.admin)

        response = self.client.get(
            reverse('exportar_usuarios_excel'),
            {'nombre_o_apellido': 'Roberto'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

        workbook = openpyxl.load_workbook(
            filename=BytesIO(response.content)
        )
        worksheet = workbook.active
        rows = list(worksheet.iter_rows(values_only=True))

        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1][1], self.developer.username)
        self.assertEqual(rows[1][2], self.developer.nombre)
        self.assertEqual(rows[1][3], self.developer.apellido)
        self.assertEqual(rows[1][4], self.developer.email)

    def test_valid_start_date_filters_users(self):
        self._login(self.admin)

        response = self.client.get(
            reverse('buscar_usuarios'),
            {'fecha_alta_desde': '2026-02-01'},
        )
        usuarios = response.context['resultados_usuarios']

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.other_developer, usuarios)
        self.assertNotIn(self.admin, usuarios)
        self.assertNotIn(self.developer, usuarios)

    def test_valid_end_date_filters_users(self):
        self._login(self.admin)

        response = self.client.get(
            reverse('buscar_usuarios'),
            {'fecha_alta_hasta': '2026-01-31'},
        )
        usuarios = response.context['resultados_usuarios']

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.admin, usuarios)
        self.assertIn(self.developer, usuarios)
        self.assertNotIn(self.other_developer, usuarios)

    def test_invalid_date_text_is_ignored(self):
        self._login(self.admin)

        response = self.client.get(
            reverse('buscar_usuarios'),
            {'fecha_alta_desde': 'fecha-invalida'},
        )
        usuarios = response.context['resultados_usuarios']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            usuarios.count(),
            Usuario.objects.count(),
        )

    def test_impossible_date_is_ignored(self):
        self._login(self.admin)

        response = self.client.get(
            reverse('buscar_usuarios'),
            {'fecha_alta_desde': '2026-02-31'},
        )
        usuarios = response.context['resultados_usuarios']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            usuarios.count(),
            Usuario.objects.count(),
        )

    def test_valid_date_is_applied_when_other_date_is_invalid(self):
        self._login(self.admin)

        response = self.client.get(
            reverse('buscar_usuarios'),
            {
                'fecha_alta_desde': '2026-02-01',
                'fecha_alta_hasta': 'fecha-invalida',
            },
        )
        usuarios = response.context['resultados_usuarios']

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.other_developer, usuarios)
        self.assertNotIn(self.admin, usuarios)
        self.assertNotIn(self.developer, usuarios)

    def test_invalid_dates_do_not_break_pdf_or_excel(self):
        self._login(self.admin)

        parameters = {
            'fecha_alta_desde': '2026-02-31',
            'fecha_alta_hasta': 'fecha-invalida',
        }

        pdf_response = self.client.get(
            reverse('generar_informe_pdf_usuarios'),
            parameters,
        )
        excel_response = self.client.get(
            reverse('exportar_usuarios_excel'),
            parameters,
        )

        self.assertEqual(pdf_response.status_code, 200)
        self.assertEqual(
            pdf_response['Content-Type'],
            'application/pdf',
        )
        self.assertEqual(excel_response.status_code, 200)
        self.assertEqual(
            excel_response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )

    def test_pdf_and_excel_reuse_shared_filter(self):
        import inspect
        from .views import (
            buscar_usuarios,
            generar_informe_pdf_usuarios,
            exportar_usuarios_excel,
        )

        for view in (
            buscar_usuarios,
            generar_informe_pdf_usuarios,
            exportar_usuarios_excel,
        ):
            source = inspect.getsource(view)
            self.assertIn('_filtrar_usuarios(', source)


class UserDisplayNameTests(TestCase):
    """Pruebas del Hito 7: uso coherente de nombre y apellido."""

    @classmethod
    def setUpTestData(cls):
        cls.admin = Usuario.objects.create_superuser(
            username='admin_names',
            email='admin_names@test.local',
            password='test-pass-123',
            nombre='Nombre Administrador',
            apellido='Apellido Administrador',
            first_name='LegacyAdmin',
            last_name='LegacySurname',
        )
        cls.developer = Usuario.objects.create_user(
            username='developer_names',
            email='developer_names@test.local',
            password='test-pass-123',
            nombre='Roberto',
            apellido='González',
            first_name='LegacyName',
            last_name='LegacyLastName',
        )

    def setUp(self):
        self.client = Client()

    def _login(self, user):
        self.assertTrue(
            self.client.login(
                username=user.username,
                password='test-pass-123',
            )
        )

    def test_views_and_templates_do_not_use_legacy_name_fields(self):
        from pathlib import Path

        app_path = Path(__file__).resolve().parent
        files = [
            app_path / 'views.py',
            app_path / 'templates' / 'busqueda.html',
            app_path / 'templates' / 'evaluaciones.html',
            app_path / 'templates' / 'home.html',
            app_path / 'templates' / 'proyectos.html',
            app_path / 'templates' / 'revisar_tareas.html',
            app_path / 'templates' / 'tareas.html',
            app_path / 'templates' / 'usuarios.html',
        ]

        for file_path in files:
            source = file_path.read_text(encoding='utf-8')

            self.assertNotIn(
                'first_name',
                source,
                f'{file_path.name} todavía usa first_name',
            )
            self.assertNotIn(
                'last_name',
                source,
                f'{file_path.name} todavía usa last_name',
            )

    def test_home_displays_custom_nombre(self):
        self._login(self.developer)

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.developer.nombre)
        self.assertNotContains(response, self.developer.first_name)

    def test_users_page_displays_custom_name_and_surname(self):
        self._login(self.admin)

        response = self.client.get(reverse('usuarios'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            f'{self.developer.nombre} {self.developer.apellido}',
        )
        self.assertNotContains(
            response,
            f'{self.developer.first_name} {self.developer.last_name}',
        )

    def test_global_users_excel_uses_custom_name_fields(self):
        from io import BytesIO
        import openpyxl

        self._login(self.admin)

        response = self.client.get(
            reverse('exportar_todos_usuarios_excel')
        )

        self.assertEqual(response.status_code, 200)

        workbook = openpyxl.load_workbook(
            filename=BytesIO(response.content)
        )
        worksheet = workbook.active
        rows = list(worksheet.iter_rows(values_only=True))

        developer_rows = [
            row for row in rows
            if row[1] == self.developer.username
        ]

        self.assertEqual(len(developer_rows), 1)

        row = developer_rows[0]
        self.assertEqual(row[2], self.developer.nombre)
        self.assertEqual(row[3], self.developer.apellido)
        self.assertNotEqual(row[2], self.developer.first_name)
        self.assertNotEqual(row[3], self.developer.last_name)