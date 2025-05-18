from django.db import models
from django.contrib.auth import get_user_model

#creamos la tabla Lugar con sus atributos correspondientes
class Lugar(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    #obligamos al programa a que la tabla en la base de datos se llame "Lugar"
    class Meta:
        db_table = 'Lugar'

#creamos la tabla Animales con sus atributos correspondientes
class Animales(models.Model):
    user = get_user_model()

    usuario = models.ForeignKey(user, on_delete=models.CASCADE, related_name='animales')  # Relación many-to-one
    nombreAnimal = models.CharField(max_length=50)
    cantidad = models.IntegerField()
    lugarEncuentro = models.ForeignKey('Lugar', on_delete=models.CASCADE)  # Relación con la tabla Lugar
    fechaHora = models.DateTimeField(auto_now_add=True) 
    #obligamos al programa a que la tabla en la base de datos se llame "Animales"
    class Meta:
        db_table = 'Animales'



