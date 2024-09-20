import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import event_source, APIGatewayProxyEvent

from src.services.paciente_service import PacienteService

logger = Logger(service="api-pacientes")
paciente_service = PacienteService(logger)

handlers = {
    ("POST", "/inserir_dados_paciente"): paciente_service.inserir_dados_paciente,
    ("POST", "/deletar_dados_paciente"): paciente_service.deletar_dados_paciente,
    ("POST", "/cadastrar_agendamento"): paciente_service.cadastrar_agendamento
}

@event_source(data_class=APIGatewayProxyEvent)
def lambda_handler(event: APIGatewayProxyEvent, context) -> dict:
    try:
        print(event)
        request = (event.http_method, event.path)
        if request in handlers:
            logger.info(f"Event: {event.body}")
            method = handlers[request]
            response = method(json.loads(event.body))
            return response
        else:
            return {
                "status_code": 404,
                "body": "Método/Rota não suportado"
            }
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {
            "status_code": 500,
            "body": f"An error occurred: {str(e)}"
        }


# event = {
#     "httpMethod": "POST",
#     "path": "/deletar_dados_paciente",
#     "body": json.dumps({
#         "cpf": "48863078822",
#         "nome": "Henrique Bittencourt Severo",
#         "endereco": "Rua Francisco da Costa Machado 301",
#         "telefone": "11953331048"
#     })
# }

# try:
#     result = lambda_handler(event, None)
#     print(result)
# except Exception as e:
#     print(f"An error occurred: {str(e)}")
