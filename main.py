import pprint
import boto3

cognito_pool_id = {
    'account_id': 'xxxxxxxxxxxx',
    'identity_pool_id': 'ap-northeast-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
    'region': 'ap-northeast-1'
}


class CognitoPoolId:
    def __init__(self, pool_id: cognito_pool_id) -> None:
        self.account_id = pool_id['account_id']
        self.identity_pool_id = pool_id['identity_pool_id']
        self.region = pool_id['region']

        boto3_client = boto3.client('cognito-identity', pool_id['region'])
        resp = boto3_client.get_id(IdentityPoolId=self.identity_pool_id)
        resp = boto3_client.get_credentials_for_identity(IdentityId=resp['IdentityId'])

        self.secret_key = resp['Credentials']['SecretKey']
        self.access_key = resp['Credentials']['AccessKeyId']
        self.session_token = resp['Credentials']['SessionToken']


class Boto3DynamoDBSession:

    def __init__(self, cognito_id: CognitoPoolId) -> None:
        self.session = boto3.session.Session(
            aws_access_key_id=cognito_id.access_key,
            aws_secret_access_key=cognito_id.secret_key,
            aws_session_token=cognito_id.session_token,
            region_name=cognito_id.region)

    def boto3_resource(self):
        return self.session.resource('dynamodb')

    def boto3_client(self):
        return self.session.client('dynamodb')


cognito = CognitoPoolId(cognito_pool_id)
boto3_session = Boto3DynamoDBSession(cognito)
dynamodb_client = boto3_session.boto3_client()

res = dynamodb_client.list_tables()
pprint.pprint(res)
