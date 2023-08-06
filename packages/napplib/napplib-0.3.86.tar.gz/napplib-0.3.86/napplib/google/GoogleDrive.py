import gspread
from google.oauth2.service_account import Credentials

class GoogleDriveController:

	@staticmethod
	def get_spreadsheet(google_secret_file, spreadsheet):
		# use creds to create a client to interact with the Google Drive API
		scope = ['https://spreadsheets.google.com/feeds',
				'https://www.googleapis.com/auth/drive']

		creds = Credentials.from_service_account_file(google_secret_file, scopes=scope)
		client = gspread.authorize(creds)

		# Find a workbook by name and open the first shpwdeet
		# Make sure you use the right name here.
		sheet = client.open(spreadsheet).sheet1

		# Extract and print all of the values
		return sheet.get_all_records()
 
		
	@staticmethod
	def get_spreadsheet_by_url(google_secret_file, spreadsheet_url, sheet_index = 0):
		# use creds to create a client to interact with the Google Drive API
		scope = ['https://spreadsheets.google.com/feeds',
				'https://www.googleapis.com/auth/drive']

		creds = Credentials.from_service_account_file(google_secret_file, scopes=scope)
		client = gspread.authorize(creds)

		sheet = client.open_by_url(spreadsheet_url).get_worksheet(sheet_index)

		# Extract and print all of the values
		return sheet.get_all_records()

	@staticmethod
	def update_cell_spreadsheet(google_secret_file, spreadsheet, cell, value):
		# use creds to create a client to interact with the Google Drive API
		scope = ['https://spreadsheets.google.com/feeds',
				'https://www.googleapis.com/auth/drive']

		creds = Credentials.from_service_account_file(google_secret_file, scopes=scope)
		client = gspread.authorize(creds)

		# Find a workbook by name and open the first shpwdeet
		# Make sure you use the right name here.
		sheet = client.open(spreadsheet).sheet1

		sheet.update(cell, value)

		# Extract and print all of the values
		return sheet.get_all_records()