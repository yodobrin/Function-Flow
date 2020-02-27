import json
import logging
import os

import azure.functions as func

import adal
from msrestazure.azure_active_directory import AdalAuthentication
from msrestazure.azure_cloud import AZURE_PUBLIC_CLOUD
from azure.mgmt.media import AzureMediaServices
from azure.mgmt.media.models import MediaService

LOGIN_ENDPOINT = AZURE_PUBLIC_CLOUD.endpoints.active_directory
RESOURCE = AZURE_PUBLIC_CLOUD.endpoints.active_directory_resource_id


RESOURCE = os.getenv('RESOURCE')
# Tenant ID for your Azure Subscription
TENANT_ID = os.getenv('TENANT_ID')
# Your Service Principal App ID
CLIENT = os.getenv('CLIENT')
# Your Service Principal Password
KEY = os.getenv('KEY')
# Your Azure Subscription ID
SUBSCRIPTION_ID = os.getenv('SUBSCRIPTION_ID')
# Your Azure Media Service (AMS) Account Name
ACCOUNT_NAME = os.getenv('ACCOUNT_NAME')
# Your Resource Group Name
RESOUCE_GROUP_NAME = os.getenv('RESOUCE_GROUP_NAME')

def main(event: func.EventGridEvent):
    result = json.dumps({
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
    })

    context = adal.AuthenticationContext(LOGIN_ENDPOINT + '/' + TENANT_ID)
    credentials = AdalAuthentication(
        context.acquire_token_with_client_credentials,
        RESOURCE,
        CLIENT,
        KEY
    )
    # You can now use this object to perform different operations to your AMS account.
    client = AzureMediaServices(credentials, SUBSCRIPTION_ID)
    logging.info("signed in to ams")
    logging.info ('assest list %s',client.assets.list(RESOUCE_GROUP_NAME, ACCOUNT_NAME).get(0))
    logging.info('Python EventGrid trigger processed an event: %s', result)
