import requests
import os
import json
import logging
import configparser
import boto3

from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)

CREATE_ACCOUNT_URL = "https://tksmt2n35c.execute-api.eu-west-1.amazonaws.com/accounts/create"
LOGIN_URL = "https://tksmt2n35c.execute-api.eu-west-1.amazonaws.com/accounts/login"
PROVISION_URL = "https://ih2nm2q68j.execute-api.eu-west-1.amazonaws.com/prod/config"
PROFILE_NAME = "aero"
CLIENT_ID = "7qkl0rnt99f5nak775q1v99uv8"

class ComputeStatus():

    NO_VALUE = 0
    INIT = 1
    CREATING = 2
    CREATED = 3
    FAILED = 4

class Account():

    def __init__(self, email, auth_token):

        self.email = email
        self.auth_token = auth_token

        self.user_home = str(Path.home())


    def provision(self):
        data = dict(
            company="solo",
            project="default"
        )
        logger.debug("provision()")
        logger.debug(data)
        r = requests.post(PROVISION_URL,
            json=data,
            headers = {
                "x-api-key": self.auth_token
            }
        )
        logger.debug(r.status_code)
        
        if r.status_code == 202:
            return ComputeStatus.INIT
        elif r.status_code == 207:
            return ComputeStatus.CREATING
        elif r.status_code != 200:
            raise Exception(r.status_code, r.text)

        response_data = r.json()

        # Create Metaflow directory
        if not os.path.exists(f"{self.user_home}/.metaflowconfig"):
            os.mkdir(f"{self.user_home}/.metaflowconfig")

        with open(f"{self.user_home}/.metaflowconfig/config.json", 'w', encoding='utf-8') as f:
            json.dump(response_data['config'], f, ensure_ascii=False, indent=4)

        # Create AWS directory
        if not os.path.exists(f"{self.user_home}/.aws"):
            os.mkdir(f"{self.user_home}/.aws")

        config = configparser.ConfigParser()
        config.read(f"{self.user_home}/.aws/credentials")

        if PROFILE_NAME not in config:
            config.add_section(PROFILE_NAME)

        # Doesnt matter if profile already exists, we want to overwrite creds
        config[PROFILE_NAME]["aws_access_key_id"] = response_data['access_id']
        config[PROFILE_NAME]["aws_secret_access_key"] = response_data['access_secret']
        config[PROFILE_NAME]["aws_session_token"] = response_data['session_token']
        config[PROFILE_NAME]["region"] = response_data['region']

        with open(f"{self.user_home}/.aws/credentials", 'w') as configfile:
            config.write(configfile)

        return ComputeStatus.CREATED
        

    @classmethod
    def login(cls, email, password):

        token = cls._login(email, password)

        return Account(email, token)

    @classmethod
    def create(cls, email, password):

        outcome = cls._create_account(email, password)

        return outcome
    
    @classmethod
    def _hash(cls, password):

        return sha256(password.strip()).hexdigest()

    @classmethod
    def _create_account(cls, email, password):

        data = dict(
            username=email, 
            password=password
        )
        logger.debug("_create_account()")
        logger.debug(data)
        logger.info("Signup is currently not supported on the CLI")

        return True

    @classmethod
    def _login(cls, email, password):

        cognito = boto3.client('cognito-idp')

        data = dict(
            email=email, 
            password=password
        )
        logger.debug("_login()")
        response = cognito.initiate_auth(
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={
                "USERNAME": email,
                "PASSWORD": password
            },
            ClientId=CLIENT_ID
        )

        if 'AuthenticationResult' not in response:
            raise Exception("Error logging in")

        logger.debug(response['AuthenticationResult']['AccessToken'])

        return response['AuthenticationResult']['AccessToken']
