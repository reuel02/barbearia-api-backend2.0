from marshmallow import Schema, fields, validate


class CadastroSchema(Schema):

    nome_empresa = fields.Str(required=True, validate=validate.Length(min=2, max=100))
    # Não é obrigatório (pode iniciar a barbearia sem CNPJ inicialmente)
    cnpj = fields.Str(required=False, validate=validate.Length(max=14))

    # --- Dados do Dono (Admin) ---
    nome_usuario = fields.Str(required=True, validate=validate.Length(min=2, max=100))

    # O field 'Email' já valida internamente se a pessoa digitou um '@' e um '.' !
    email = fields.Email(required=True)

    # Garante que a senha tenha uma segurança mínima
    senha = fields.Str(required=True, validate=validate.Length(min=6))
