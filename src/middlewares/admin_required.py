from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # 1. Primeiro verifica se TÊM o token (igual o jwt_required faz)
            verify_jwt_in_request()

            # 2. Abre o pacote de dados do Token
            pacote = get_jwt()

            # 3. Faz a validação da porta VIP
            if pacote.get("role") != "ADMIN":
                return (
                    jsonify(
                        {
                            "erro": "Acesso negado. Apenas Administradores podem acessar esta rota."
                        }
                    ),
                    403,
                )

            # Deixa passar para o Controlador!
            return fn(*args, **kwargs)

        return decorator

    return wrapper
