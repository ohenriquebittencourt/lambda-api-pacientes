import json
import boto3
import pickle
from aws_lambda_powertools import Logger

class PacienteService():
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        self.s3_client = boto3.client('s3')
        self.cognito_client = boto3.client('cognito-idp')
   
    def inserir_dados_paciente(self, body):
        cpf = body.get('cpf', '')
        nome = body.get('nome', '')
        email = body.get('email', '')
        senha = body.get('senha', '')

        json_data = {
            'nome': nome,
            'cpf': cpf,
            'email': email, 
            'senha': senha,
            'agendamentos': []
            }
        
        pickled_obj = pickle.dumps(json_data)

        self.s3_client.put_object(
            Bucket="bucket-pacientes-fiap",
            Key=f"{cpf}.pkl",
            Body=pickled_obj
        )

        cognito_response = self.cognito_client.sign_up(
            ClientId="",
            Username=email,
            Password=senha
        )

        return 201

    def deletar_dados_paciente(self, body: dict):
        cpf = body.get('cpf', '')
        email = body.get('email', '')
        
        self.s3_client.delete_object(Bucket="bucket-pacientes-fiap", Key=f"{cpf}.pkl")

        response = self.cognito_client.admin_delete_user(
            UserPoolId="USER_POOL_ID",
            Username=email
        )

        self.logger.info(f"Dados do paciente cpf {cpf} foram deletados.")
        return 200

    def cadastrar_agendamento(self, body):
        cpf = body.get('cpf', '')
        medico = body.get('medico', '')
        horario = body.get('horario', '')
        agendamento = {
             'medico': medico,
             'horario': horario
             }
        response = self.s3_client.get_object(Bucket="bucket-pacientes-fiap", Key=f"{cpf}.pkl")
        json_data = response['Body'].read().decode('utf-8')
        json_data['agendamentos'].append(agendamento)
        
        pickled_obj = pickle.dumps(json_data)

        self.s3_client.put_object(
            Bucket="bucket-pacientes-fiap",
            Key=f"{cpf}.pkl",
            Body=pickled_obj
        )
        return 201
