import requests, json, logging
from .models.authentication import MicrovixAuthentication
from .utils import xml_to_dict_array

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(threadName)-11s %(levelname)-10s %(message)s")


class MicrovixController:

	url = 'http://webapi.microvix.com.br/1.0/api/integracao'

	@classmethod
	def get_stock(self, authentication, start_mov_date= None, end_mov_date=None):

		logging.info(f"Getting stock info...")

		authentication.setCommandName('LinxProdutosDetalhes')
		authentication.data_mov_ini = start_mov_date
		authentication.data_mov_fim = end_mov_date

		return self.__post(authentication)


	@classmethod
	def get_products(self, authentication, start_update_date=None, end_update_date=None):

		logging.info(f"Getting products...")

		authentication.setCommandName('LinxProdutos')
		authentication.dt_update_inicio = start_update_date
		authentication.dt_update_fim = end_update_date

		return self.__post(authentication)


	def __post(authentication):

		payload = str(authentication)

		headers = { 'Content-Type': 'application/xml' }

		r = requests.post(MicrovixController.url, headers=headers, data=payload)

		if not r:
			raise Exception('Request returned nothing', authentication)

		return xml_to_dict_array(r.content)
