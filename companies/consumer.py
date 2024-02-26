# from django.contrib.sites import requests
# from kafka import KafkaConsumer
# import json
#
# from models import Company
#
# # Configure o consumidor Kafka
# consumer = KafkaConsumer(
#     'company_updates',
#     bootstrap_servers=['localhost:29092'],  # Substitua pelo seu servidor Kafka
#     value_deserializer=lambda m: json.loads(m.decode('utf-8'))
# )
#
#
# def listen_for_company_updates():
#     for message in consumer:
#         data = message.value
#         update_company_data(data['company_id'], data['cnpj'])
#
#
# def update_company_data(company_id: int, cnpj: str):
#     response = requests.get(f'https://receitaws.com.br/v1/cnpj/{cnpj}')
#     if response.status_code == 200:
#         data = response.json()
#         company = Company.objects.get(id=company_id)
#         company.corporate_name = data['razao_social']
#         company.trade_name = data['nome_fantasia']
#         company.save()
