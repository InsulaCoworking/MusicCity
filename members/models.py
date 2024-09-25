
from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from bands.helpers import RandomFileName
from bands.models import Tag, Event

help_choices = (
    ("comunicacion","Comunicación y marketing"),
    ("diseno","Diseño gráfico"),
    ("produccion","Producción de eventos"),
    ("fotovideo","Foto/vídeo"),
    ("administracion","Administración y gestión"),
    ("otro","Otros (especificar)")
)

class Member(models.Model):
    dni = models.CharField(null=False, verbose_name='DNI/NIE', max_length=40, unique=True)
    first_name = models.CharField(null=False, verbose_name='Nombre', max_length=240)
    last_name = models.CharField(null=False, verbose_name='Apellidos', max_length=240)
    birth_date = models.DateField(null=False, blank=False, verbose_name="Fecha de nacimiento")
    register_date = models.DateField(null=False, blank=True, verbose_name="Fecha de registro", auto_now_add=True)
    address = models.CharField(null=True, blank=True, max_length=100, verbose_name='Dirección')
    email = models.EmailField(null=False, blank=True, verbose_name="Correo electrónico", help_text="Sólo lo utilizaremos para las notificaciones de asambleas generales y avisar de eventos en los que puedas participar")
    phone = models.CharField(null=True, blank=True, verbose_name="Teléfono de contacto", max_length=50, help_text="introdúcelo si quieres que te incluyamos en el grupo de Whatsapp general de la asociación, donde os mantendremos informados del desarrollo de nuestros proyectos, y donde podrás solicitar participar en el desarrollo de actividades.")
    favourite_genre = models.TextField(null=True, blank=True, verbose_name="Género musical favorito")

    help = models.TextField(null=True, blank=True, choices=help_choices, verbose_name="En qué te gustaría colaborar")
    help_other = models.TextField(null=True, blank=True, verbose_name="Otro tipo de colaboración")
    comments_extra = models.TextField(null=True, blank=True, verbose_name="Cuéntanos lo que quieras")

    class Meta:
        verbose_name = 'Socia'
        verbose_name_plural = 'Socias'
        ordering = ['last_name']


    def __str__(self):
        return self.first_name + '' + self.last_name

