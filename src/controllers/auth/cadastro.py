from src.schemas.cadastro_schema import CadastroSchema
from src.models.empresa import Empresa
from src.models.usuario import Usuario, RoleUsuario
from src.schemas.usuario_schema import UsuarioSchema
from flask import request, jsonify
from db import db
from werkzeug.security import generate_password_hash, check_password_hash


# Controlador de cadastro de ADMIN e empresa
def cadastrar():
    try:
        schema = CadastroSchema()

        dados = schema.load(request.json)

        slug_gerado = dados["nome_empresa"].lower().replace(" ", "-")

        empresa = Empresa(
            nome=dados["nome_empresa"], slug=slug_gerado, cnpj=dados.get("cnpj")
        )

        db.session.add(empresa)
        db.session.flush()

        senha_hash = generate_password_hash(dados["senha"])

        usuario = Usuario(
            empresa_id=empresa.id,
            nome=dados["nome_usuario"],
            email=dados["email"],
            senha_hash=senha_hash,
            role=RoleUsuario.ADMIN,
        )

        db.session.add(usuario)
        db.session.commit()

        return (
            jsonify(
                {"mensagem": "Usuario cadastrado com sucesso", "empresa_id": empresa.id}
            ),
            201,
        )

    except Exception as e:
        print(e)
        return jsonify({"mensagem": "Erro inesperado no sistema", "erro": str(e)}), 500
