import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
class TestAutenticacion:
    """Pruebas funcionales formales para el CU-4: Autenticación Segura"""

    def test_registro_usuario_exitoso(self, client):
        url = reverse('registro')  
        
        # CORRECCIÓN: Usamos password1 y password2 tal como lo pide Django
        response = client.post(url, {
            'username': 'nuevo_estudiante',
            'email': 'estudiante@santotomas.cl',
            'password1': 'PasswordSegura123',
            'password2': 'PasswordSegura123'
        })
        
        # Validamos que el usuario se haya creado en la base de datos
        assert User.objects.filter(username='nuevo_estudiante').exists()
        assert response.status_code == 302

    def test_login_exitoso(self, client):
        # Preparación: Creamos un usuario de prueba
        User.objects.create_user(username='tomas_test', password='mipassword123')
        
        # Acción: Enviamos los datos al formulario de login
        url = reverse('login')
        response = client.post(url, {
            'username': 'tomas_test',
            'password': 'mipassword123'
        })
        
        # Validación: El usuario debería ser redirigido exitosamente
        assert response.status_code == 302
        assert response.url == reverse('home')  

    def test_login_fallido_credenciales_incorrectas(self, client):
        User.objects.create_user(username='tomas_test2', password='mipassword123')
        
        url = reverse('login')
        response = client.post(url, {
            'username': 'tomas_test2',
            'password': 'ClaveEquivocada'
        })
        
        # Como falló, la página debería recargar (código 200) mostrando el error
        assert response.status_code == 200