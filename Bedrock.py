import boto3
from botocore.exceptions import ClientError

class Converse:

    def __init__(self, region='us-east-1', access_key_id='', secret_key=''):
        self.bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_key
        )

    def converse_with_model(self,model_id, messages, system_text ='You are a chatbot.', top_k=200, temperature=0.5):
        response = ''
        # Base inference parameters to use.
        inference_config = {"temperature": temperature}
        # Additional inference parameters to use.
        additional_model_fields = {"top_k": top_k}
        system_prompts = [{"text": system_text}]

        try:
            print (model_id)
            response = self.bedrock_client.converse(modelId=model_id, messages=messages, system=system_prompts,
                                                     inferenceConfig=inference_config,
                                                     additionalModelRequestFields=additional_model_fields)
            return response['output']['message']["content"][0]["text"]
        except ClientError as err:
            message = err.response['Error']['Message']
            print("A client error occured: " + format(message))
            return f"Sorry, I am unable to converse with you at this time. {message}"
