import json
import requests

class OlistController:

	def get_access_token(url, code, client_id, client_secret, redirect_uri):
		payload = f"code={code}&client_id={client_id}&client_secret={client_secret}&redirect_uri={redirect_uri}&grant_type=authorization_code"

		return requests.post(f"{url}/openid/token", data=payload)


	def refresh_access_token(url, client_id, client_secret, refresh_token):
		payload = f"client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token"

		r = requests.post(f"{url}/openid/token", data=payload)
		return r


	def create_product(url, access_token, products):
		headers = {
			"Authorization": f"JWT {access_token}",
			"Accept": "application/json",
			"Content-Type": "application/json"
		}

		payload = json.dumps(products, ensure_ascii=False)

		r = requests.post(f"{url}/v1/seller-products/", headers=headers, data=payload)
		return r


	def update_product(url, access_token, product, product_sku):
		headers = {
			"Authorization": f"JWT {access_token}",
			"Accept": "application/json",
			"Content-Type": "application/json"
		}

		payload = json.dumps(product)

		r = requests.patch(f"{url}/v1/seller-products/{product_sku}/", headers=headers, data=payload)
		return r
