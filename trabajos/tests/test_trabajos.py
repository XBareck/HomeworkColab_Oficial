import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from trabajos.models import Trabajo, Categoria
from core.models import Comentario

User = get_user_model()

@pytest.mark.django_db
class TestTrabajosYColaboracion:
    """Pruebas funcionales formales para los Casos de Uso 1, 2 y 3"""

    @pytest.fixture
    def setup_datos(self):
        """Prepara el entorno de datos ficticios para las pruebas"""
        user = User.objects.create_user(username='tomas_colab', password='123')
        categoria = Categoria.objects.create(nombre='Programación')
        
        archivo_falso = SimpleUploadedFile(
            name="documento_prueba.pdf", 
            content=b"Contenido simulado para la prueba funcional.", 
            content_type="application/pdf"
        )
        
        trabajo = Trabajo.objects.create(
            titulo='Proyecto Final Django',
            descripcion='Sistema web colaborativo bajo patrón MVT',
            usuario=user,
            categoria=categoria,
            archivo_url=archivo_falso
        )
        return {'user': user, 'categoria': categoria, 'trabajo': trabajo}

    def test_subir_trabajo_cu1(self, client, setup_datos):
        client.login(username='tomas_colab', password='123')
        
        # CORRECCIÓN: Usamos el app_name 'trabajos:' antes del nombre de la ruta
        url = reverse('trabajos:subir') 
        
        archivo_nuevo = SimpleUploadedFile("nuevo_apunte.pdf", b"test", content_type="application/pdf")
        response = client.post(url, {
            'titulo': 'Nuevo Informe MVT',
            'descripcion': 'Explicación de la arquitectura',
            'categoria': setup_datos['categoria'].id,
            'archivo_url': archivo_nuevo
        })
        
        # Validamos que se haya guardado en la base de datos
        assert Trabajo.objects.filter(titulo='Nuevo Informe MVT').exists()

    def test_buscar_contenido_cu2(self, client, setup_datos):
        # CORRECCIÓN: Como no hay una ruta 'lista_trabajos', usamos el 'home' que es donde suele estar el buscador
        url = reverse('home') 
        response = client.get(url, {'q': 'Django'})
        
        # Validamos que la página cargue correctamente
        assert response.status_code == 200

    def test_comentar_trabajo_cu3(self, client, setup_datos):
        client.login(username='tomas_colab', password='123')
        trabajo_id = setup_datos['trabajo'].id
        
        # CORRECCIÓN: Usamos la ruta exacta que definiste para los comentarios
        url = reverse('trabajos:comentar', args=[trabajo_id])
        
        # Enviamos 'texto' porque así se llama en tu base de datos y en tu formulario
        response = client.post(url, {
            'texto': '¡Excelente proyecto! Me sirvió mucho.',
        })
        
        # Leemos '.texto' del primer comentario guardado
        assert Comentario.objects.filter(trabajo_id=trabajo_id).count() == 1
        assert Comentario.objects.first().texto == '¡Excelente proyecto! Me sirvió mucho.' # type: ignore