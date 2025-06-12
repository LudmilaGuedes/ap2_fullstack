from ninja import Router
from administracao.models import TbAlunos, TbCarros, TbEnderecos
from administracao.schemas import TbAlunosSchema, TbAlunosSchemaIn
from typing import List
from django.shortcuts import get_object_or_404

router = Router()

# GET: Listar todos os alunos
@router.get("/alunos",
            response=List[TbAlunosSchema],
            summary="Api para listar os alunos da escola",
            description="Retorna todos os registros da tabela tb_alunos"
            )
def pegar_alunos(request):
    return TbAlunos.objects.select_related("cep", "carro").all()


# GET: Buscar aluno por ID
@router.get("/alunos/{aluno_id}",
            response=TbAlunosSchema,
            summary="Api para buscar aluno por ID",
            description="Retorna os dados de um aluno específico pelo ID"
            )
def pegar_aluno_por_id(request, aluno_id: int):
    return get_object_or_404(TbAlunos.objects.select_related("cep", "carro"), id=aluno_id)


# POST: Criar novo aluno
@router.post("/alunos",
             response=TbAlunosSchema,
             summary="Api para criar um novo aluno",
             description="Insere um novo aluno na tabela tb_alunos"
             )
def criar_aluno(request, data: TbAlunosSchemaIn):

    cep_obj = TbEnderecos.objects.filter(pk=data.cep).first() if data.cep else None
    carro_obj = TbCarros.objects.filter(pk=data.carro).first() if data.carro else None

    if data.cep and not cep_obj:
        return {"erro": "CEP não encontrado."}, 400
    if data.carro and not carro_obj:
        return {"erro": "Carro não encontrado."}, 400

    aluno = TbAlunos.objects.create(
        nome_aluno=data.nome_aluno,
        email=data.email,
        cep=cep_obj,
        carro=carro_obj
    )

    return aluno



# PUT: Atualizar aluno por ID
@router.put("/alunos/{aluno_id}",
            response=TbAlunosSchema,
            summary="Api para atualizar um aluno",
            description="Atualiza os dados de um aluno existente"
            )
def atualizar_aluno(request, aluno_id: int, data: TbAlunosSchemaIn):
    aluno = get_object_or_404(TbAlunos, id=aluno_id)
    aluno.nome_aluno = data.nome_aluno
    aluno.email = data.email
    aluno.cep = TbEnderecos.objects.get(pk=data.cep) if data.cep else None
    aluno.carro = TbCarros.objects.get(pk=data.carro) if data.carro else None
    aluno.save()
    return aluno


# DELETE: Remover aluno por ID
@router.delete("/alunos/{aluno_id}",
               response=dict,
               summary="Api para deletar um aluno",
               description="Remove um aluno com base no ID informado"
               )
def deletar_aluno(request, aluno_id: int):
    aluno = get_object_or_404(TbAlunos, id=aluno_id)
    aluno.delete()
    return {"detail": "Aluno deletado com sucesso"}
