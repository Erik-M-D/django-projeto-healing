from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

def is_medico(user):
    # isso vai retornar TRUE se o usuario já fez o cadastro médico e FALSE se não estiver feito
    return DadosMedicos.objects.filter(user=user).exists()

# Create your models here.
class Especialidades(models.Model):

    especialidade = models.CharField(max_length=100)

    def __str__(self):
        return self.especialidade

class DadosMedicos(models.Model):
    crm = models.CharField(max_length=30)
    nome = models.CharField(max_length=100)
    cep = models.CharField(max_length=15)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.IntegerField()
    # pdf? | armazena o arquivo em uma pasta da aplicação e depois referencia
    rg = models.ImageField(upload_to='rgs')
    cedula_identidade_medica = models.ImageField(upload_to='cim')
    foto = models.ImageField(upload_to='fotos_perfil')
    descricao = models.TextField()
    valor_consulta = models.FloatField(default=100)
    # relação com outra model
    # on_delete caso o usuario seja excluido oq fazer com este cadastros
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.user.username
    
    # o @property faz com que seja considerado uma propriedade do DadosMedicos
    @property
    def proxima_data(self):
        proxima_data = DatasAbertas.objects.filter(user=self.user).filter(data__gt=datetime.now()).filter(agendado=False).order_by('data').first()
        
        return proxima_data
        
    

class DatasAbertas(models.Model):
    data = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    agendado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.data)
    