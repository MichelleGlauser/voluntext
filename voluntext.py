# Dependencies
import os
import gspread
import phonenumbers
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

# Authorize with Twilio
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
client = Client(TWILIO_ACCOUNT_SID, AUTH_TOKEN)

# Authorize with Google
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('voluntext-a5681f465e11.json', scope)
gc = gspread.authorize(credentials)

# Open first (responses) worksheet from volunteer application spreadsheet with one shot
worksheet = gc.open_by_key('1VPP0lU-AuO-zwCLdcSRBBX26rtkt0GcKhcG0G9SwSpg').sheet1

# Get volunteer names
names_list = worksheet.col_values(4)

# Get volunteer phone numbers
numbers_list = worksheet.col_values(8)

# Format phone numbers?
for number in numbers_list:
	formatted_number = phonenumbers.parse("+1" + number, None)
	print formatted_number
# phonenumbers.format_number(x, phonenumbers.PhoneNumberFormat.E164)
# print final_volunteers_dict

# Zip names and phone numbers
volunteers_dict = dict(zip(names_list, numbers_list))

# Create new dict without key-value pairs with empty values
final_volunteers_dict = dict((k, v) for k, v in volunteers_dict.iteritems() if v)

# test_dict = { 'JanetJackson': 8012148481, 'Techtonica': 4159641088 }
# # Iterate through dict and use key and value to text each person
# # for names, numbers in final_volunteers_dict.items():
# 	# Formulate text

# for name, number in test_dict.items():
# 	message = client.messages.create(
# 		body = "Hi, " + name + ", thanks for volunteering!", # Message body, if any
# 		to = number,
# 		from_ = "+14159641088",
# 	)
# 	print message.sid