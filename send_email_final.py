

import base64
import httplib2

from apiclient import discovery

import auth
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
SCOPES = 'https://mail.google.com/'
CREDENTIALS = 'credentials.json'
APPLICATION_NAME = 'NetworkProgProject'
authInst = auth.auth(SCOPES, CREDENTIALS, APPLICATION_NAME)
credentials = authInst.get_credentials()

http = credentials.authorize(httplib2.Http())
service = discovery.build('gmail', 'v1', http=http)

address_dictionary = {}
'''
Author: Google
This google came from the google documentation that I read to add attachments
this is due to the fact that to be compliant with the Google API it has to be
done in a specific way

'''


def add_attachment(message_function, lists):
    for file in lists:
        message_mime = MIMEBase('application', "octet-stream")
        message_mime.set_payload(open(file, "rb").read())
        encoders.encode_base64(message_mime)
        message_mime.add_header('Content-Disposition', 'attachment; filename=' + file)
        message_function.attach(message_mime)
    return message

# reads in a file and names it as file


with open("address") as file:
    # for loop which parses through the file one line at a time
    for line in file:
        # splits up the list
        (first_name, last_name, email_address) = line.split()
        # concatenates first name and last name
        full_name = first_name + last_name
        # makes all keys lowercase
        full_name = full_name.lower()
        # inserts name as key and address as value
        address_dictionary[str(full_name)] = email_address
# email which uses MIME to piece together different objects into one format
recipient_holder = input("Do you want to send the email to all contacts? Y/N\n")
# recipient_holder = int(recipient_holder)
# loop through dictionary and send email to all
if recipient_holder.lower() == 'y':
    # .values() returns a list of all values in the dictionary
    list_of_to_values = list(address_dictionary.values())
    # for MIME this field needs to be a string so the list is sent to a string separated by ,
    string_email = ', '.join(str(w) for w in list_of_to_values)
elif recipient_holder.lower() == 'n':
    recipient_input = input(
        "Please enter the first and last name of the people you want to send the email to, "
        "pressing space only after every last name.\n")
    # makes input keys lowercase to match dictionary
    recipient_input = recipient_input.lower()
    # creates a list of values which are the email addresses
    list_of_to_values = []
    # takes user input and separates the keys
    list_of_names = recipient_input.split()
    # for loop which takes inputted names and spits back email addresses
    for key in list_of_names:
        list_of_to_values.append(address_dictionary.get(key))
    # converts list of addresses to a string
    string_email = ', '.join(str(w) for w in list_of_to_values)
else:
    # used if input is not Y or N
    print("Invalid response try again.")
    quit()
message = MIMEMultipart()
message['to'] = string_email
CC_holder = input("Do you want to CC any contacts? Y/N\n")

if CC_holder.lower() == 'y':
    # prompts user who specifically should be CC'd
    CC_input = input(
        "Please enter the first and last name of the people you want to send the email to, "
        "pressing enter after every last name.\n")
    CC_input = CC_input.lower()
    list_of_CC_values = []
    list_of_names = CC_input.split()
    for key in list_of_names:
        list_of_CC_values.append(address_dictionary.get(key))
    string_CCd = ', '.join(str(w) for w in list_of_CC_values)
    CC_address = string_CCd
    list_of_all_values = list_of_to_values + list_of_CC_values
    message['CC'] = CC_address
elif CC_holder.lower() == 'n':
    list_of_all_values = list_of_to_values
else:
    print("Invalid response try again.")
    quit()

message['from'] = 'thisisatestnetwork@gmail.com'
email_subject = input("Please type the header of your email\n")
message['subject'] = email_subject
email_body = input("Please type the body of your email\n")
msg = MIMEText(email_body)
message.attach(msg)
files = input("Please type the name of the extension followed by the .type \"Image.png\" and separated by space"
              ". Press Enter when done\n")
if len(files) > 0:
    files = files.split(" ")

from email import encoders
message = add_attachment(message, files)
tweet_boolean = input('Do you wish to send a tweet? (Y/N)\n')
if tweet_boolean.lower() == 'y':
    # importing the tweepy module
    import tweepy

    # personal information
    consumer_key = "u4UWKsx7U1JDGhpYNNQb1c88j"
    consumer_secret = "olFggz3ROf4evwFgEj2pDhYk2lQ2THthf9vbEREHpIu6UROPSI"
    access_token = "1065394778802659328-IscQr8JTjseKVkXhuDY7xHGB7mFg4f"
    access_token_secret = "BGRZ53t61hJj7jyfJ6KWBRTZ54y740JxM32IYfvtCdXKG"

    # authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    tweet = input('Please enter what you want to tweet:\n')
    image_boolean = input('Do you wish to attach an image? (Y/N)\n')
    if image_boolean.lower() == 'y':
        image_boolean = True
    elif image_boolean.lower() == 'n':
        image_boolean = False
    else:
        print("Invalid response try again.")
        quit()
    if image_boolean:
        path_to_image = input('Please type the path of the image:\n')
        send_to_recipient = input('Would you like to send this tweet to all recipients chosen before? (Y/N)\n')
        if send_to_recipient.lower() == 'y':
            email_tweet = open('Tweeting.txt', 'w')
            email_tweet.write('Tweet:\n   ')
            email_tweet.write(tweet)
            email_tweet.close()
            lists_tweet = ['Tweeting.txt', path_to_image]
            message = add_attachment(message, lists_tweet)
            api.update_with_media(path_to_image, tweet)
        elif send_to_recipient.lower() == 'n':
            api.update_with_media(path_to_image, tweet)
        else:
            print("Invalid response try again.")
            quit()
    elif not image_boolean:
        send_to_recipient = input('Would you like to send this tweet to all recipients chosen before? (Y/N)\n')
        if send_to_recipient.lower() == 'y':
            email_tweet = open('Tweeting.txt', 'w')
            email_tweet.write(tweet)
            lists_tweet = ['Tweeting.txt']
            message = add_attachment(message, lists_tweet)
            api.update_status(status=tweet)
        elif send_to_recipient.lower() == 'n':
            api.update_status(status=tweet)
        else:
            print("Invalid response try again.")
            quit()
    else:
        print("Invalid response try again.")
        quit()


else:
    pass
complete_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
# Needed to be compliant with Google API


try:
    message = (service.users().messages().send(userId='me', body=complete_message).execute())
    print('Email Sent!')
except:
    print('An error has occurred')