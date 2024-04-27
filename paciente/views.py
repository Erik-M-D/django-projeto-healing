from django.shortcuts import render, redirect
from medico.models import DadosMedicos, Especialidades, DatasAbertas, is_medico
from datetime import datetime
from .models import Consulta, Documento
from django.contrib import messages
from django.contrib.messages import constants

from django.db import transaction #deixando atomico | CONCEITO ATOMICIDADE
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    if request.method == 'GET':
        medico_filtrar = request.GET.get('medico')
        # o metodo .get só pega 1 valor (o último), porem o getlist pega varios
        especialidades_filtrar = request.GET.getlist('especialidades')
        
        medicos = DadosMedicos.objects.all()

        if medico_filtrar:
            medicos = medicos.filter(nome__icontains=medico_filtrar)
        
        # filtrando uma lista! coloque depois do nome da propriedade "__in"
        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)
        especialidades = Especialidades.objects.all()
        return render(request, 'home.html', {'medicos':medicos, 'especialidades':especialidades, 'is_medico':is_medico(request.user)})

@login_required
def escolher_horario(request, id_dados_medicos):
    if request.method == 'GET':
        medico = DadosMedicos.objects.get(id=id_dados_medicos)
        # se acessou um determinado medico pode usar as propriedades dele, no caso o user
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gt=datetime.now())
        

        return render(request, 'escolher_horario.html', {'medico':medico, 'datas_abertas':datas_abertas, 'is_medico':is_medico(request.user)})

@login_required    
def agendar_horario(request, id_data_aberta):
    if request.method == 'GET':
        #TODO atomicidade aplicada!
        with transaction.atomic():
            data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

            horario_agendado = Consulta(
                paciente=request.user,
                data_aberta=data_aberta,
            )

            horario_agendado.save()
            
            #atualizando a propriedade desse usuario
            data_aberta.agendado = True
            data_aberta.save()

            #atomicidade | Caso der errado tem que ter um meio de prevençao | só altere caso tudo estiver tido sucesso

            messages.add_message(request, constants.SUCCESS, 'Consulta agendada com sucesso!')

            return redirect('/pacientes/minhas_consultas/')

@login_required 
def minhas_consultas(request):
    #TODO consertar o filtro
    data = request.GET.get('data')
    especialidade = request.GET.get('especialidade')
    # a data_aberta é um ForEynKey (relação com outra tabela) e para acessar a propriedade de outra tabela use "__"
    minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
    
    if data:
        minhas_consultas = minhas_consultas.filter(data_aberta__data__gte=data)
    if especialidade:
        # filtro complexo, dica pensa de trás para frente | query reversa "user__dadosmedico"
        #minhas_consultas = minhas_consultas.filter(data_aberta__user__dadosmedico__especialidade_id=especialidade)
        especialidade = minhas_consultas.filter(data_aberta__user__dadosmedico__especialidade__id=especialidade)
    especialidades = Especialidades.objects.all()
    return render(request, 'minhas_consultas.html', {'minhas_consultas':minhas_consultas, 'is_medico':is_medico(request.user), "especialidades":especialidades})

@login_required
def consulta(request, id_consulta):
    if request.method == 'GET':
        consulta = Consulta.objects.get(id=id_consulta)
        dado_medico = DadosMedicos.objects.get(user=consulta.data_aberta.user)

        documentos = Documento.objects.filter(consulta=consulta)
        return render(request, 'consulta.html', {'consulta': consulta, 'dado_medico':dado_medico, 'is_medico':is_medico(request.user), 'documentos':documentos})
    

@login_required
def cancelar_consulta(request, id_consulta):
    consulta = Consulta.objects.get(id=id_consulta)
    if not request.user == consulta.paciente:
        messages.add_message(request, constants.ERROR, 'Essa consulta não é sua')
        return redirect(f'/pacientes/home/')

    consulta.status = "C"
    consulta.save()
    return redirect(f'/pacientes/consulta/{id_consulta}')
