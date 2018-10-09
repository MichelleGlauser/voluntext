# Dependencies
import os
import gspread
import re
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
worksheet = gc.open_by_key(os.environ['VOLUNTEER_SPREADSHEET_KEY']).sheet1

# Get volunteer names
names_list = worksheet.col_values(4)

# Get volunteer phone numbers
numbers_list = worksheet.col_values(8)

# Format phone numbers
new_numbers_list = []
for number in numbers_list:
	# Remove special characters and spaces
	new_number = re.sub('\W+', '', number)
	# Add "+1" to the beginning of each stripped number
	formatted_number = "+1" + new_number
	# Add each formatted number to the new numbers list
	new_numbers_list.append(formatted_number)

# Zip names and formatted phone numbers lists
volunteers_dict = dict(zip(names_list, new_numbers_list))

# Create new dict without key-value pairs that have empty values
final_volunteers_dict = dict((k, v) for k, v in volunteers_dict.iteritems() if v != "+1")
# print final_volunteers_dict

# Iterate through dict and use key and value to text each person
# for name, number in final_volunteers_dict.items():
	# message = client.messages.create(
	# 	body = "Hi " + name + ", can you join our fundraiser brunch on Saturday? Sign up here: https://www.eventbrite.com/e/techtonicas-2018-fundraiser-brunch-and-auction-tickets-47969725741",
	# 	to = number,
	# 	from_ = os.environ['TWILIO_PHONE'],
	# )
	# print message.sid

# Test!
test_dict = { 'Michelle': os.environ['PHONE_NUMBER'], 'Techtonica': os.environ['TECHTONICA_PHONE'] }
for name, number in test_dict.items():
	message = client.messages.create(
		body = "Hi " + name + ", can you join our fundraiser brunch on Saturday? Sign up here: https://www.eventbrite.com/e/techtonicas-2018-fundraiser-brunch-and-auction-tickets-47969725741",
		to = number,
		from_ = os.environ['TWILIO_PHONE'],
	)
	print message.sid