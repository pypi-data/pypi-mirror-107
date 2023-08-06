# -*- coding: utf-8 -*-
import json
import urllib
import logging

from urbano.connector import Connector, ConnectorException
from urbano.settings import api_settings

logger = logging.getLogger(__name__)


class UrbanoHandler:
    """
        Handler to send shipping payload to Urbano
    """

    def __init__(self, base_url=api_settings.URBANO['BASE_URL'],
                 user=api_settings.URBANO['USER'],
                 password=api_settings.URBANO['PASSWORD'],
                 verify=True):

        self.base_url = base_url
        self.user = user
        self.password = password
        self.verify = verify
        self.connector = Connector(self._headers(), verify_ssl=self.verify)

    def _headers(self):
        """
            Here define the headers for all connections with Urbano.
        """
        return {
            'user': self.user,
            'pass': self.password,
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    def get_shipping_label(self):
        raise NotImplementedError(
            'get_shipping_label is not a method implemented for UrbanoHandler')

    def get_default_payload(self, instance):
        raise NotImplementedError(
            'get_default_payload is not a method implemented for UrbanoHandler')

    def create_shipping(self):
        raise NotImplementedError(
            'create_shipping is not a method implemented for UrbanoHandler')

    def get_tracking(self, identifier):
        """
            This method obtain a detail a shipping of Urbano.
        """
        try:
            data = {
                'guia': '',
                'docref': f'{identifier}',
                'vp_linea': '3'
            }
            params = {'json': json.dumps(data)}
            url = f'{self.base_url}ws/ue/tracking/?{urllib.parse.urlencode(params)}'
            response = self.connector.get(url)[0]
            logger.debug(response)

            if not response['sql_error'] == '1':
                raise ConnectorException(
                    response['msg_error'], 'Error requesting tracking', response['sql_error']
                )

            return response

        except ConnectorException as error:
            logger.error(error)
            raise ConnectorException(error.message, error.description, error.code) from error
