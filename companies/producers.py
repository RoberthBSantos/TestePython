# from kafka import KafkaProducer
# import json
# from celery import shared_task, signature
# from datetime import timedelta
# from django.utils import timezone
#
# producer = KafkaProducer(
#     bootstrap_servers=['localhost:29092'],
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )
#
#
# def send_company_data(company_id: int, cnpj: str):
#     print("CHAMAAAAAAAAAA")
#     data = {
#         'company_id': company_id,
#         'cnpj': cnpj
#     }
#     producer.send('company_updates', value=data)
#     producer.flush()
#
#
# @shared_task()
# def schedule_company_update(company_id: int, cnpj: str):
#     # Chamar a função send_company_data após 30 dias
#     print(company_id)
#     s = signature('send_company_data', args=[company_id, cnpj], eta=timezone.now() + timedelta(minutes=2))
#     s.apply_async()
