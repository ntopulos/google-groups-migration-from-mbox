import socket
socket.setdefaulttimeout(10000)

import mailbox
import time

from google.oauth2 import service_account
import googleapiclient.discovery
import io



def query_yes_no(question, default='yes'):
  yes = {'yes','y', 'ye', ''}
  no = {'no','n'}

  print('\n{} [y|n]'.format(question))
  choice = input().lower()
  if choice in yes:
    return True
  elif choice in no:
    return False
  else:
    print("Please respond with 'yes' or 'no'")


def user_input(text):
  print()
  print(text)
  return input('> ')



print('Configuration...')

# https://developers.google.com/admin-sdk/groups-migration/v1/limits
sleep_time = 0.15

SCOPES = ['https://www.googleapis.com/auth/apps.groups.migration']
SERVICE_ACCOUNT_FILE = 'access-ggroups.json'

groupId = user_input('Enter the groupId (email address) of the target group:')
delegated_account_email = user_input('Enter the account id (email address) of the owner of the target group: ')
mbox_path = user_input('Enter the name/path to the mbox file: ')
mb = mailbox.mbox(mbox_path)
total_messages = len(mb)
print('The file contains {} messages.'.format(total_messages))

if not query_yes_no('Proceed with the import?'):
  print("Aborted")
  exit()


print()
print('Setting up the Google API service...')

credentials = service_account.Credentials.from_service_account_file(
  SERVICE_ACCOUNT_FILE,
  scopes=SCOPES)

delegated_credentials = credentials.with_subject(delegated_account_email)

service = googleapiclient.discovery.build(
  'groupsmigration',
  'v1',
  credentials=delegated_credentials)


print('Importing messages to {}...'.format(groupId))


i = 1
for msg in mb:
  stream = io.StringIO()
  stream.write(msg.as_string())
  media = googleapiclient.http.MediaIoBaseUpload(
    stream, mimetype='message/rfc822')
  response = service.archive().insert(
    groupId=groupId, media_body=media).execute()

  print('Message {} of {}: {}'.format(
    i,
    total_messages,
    response['responseCode'])
  )

  i = i + 1

  time.sleep(sleep_time)

print()
print('Import of {} completed ({} messages imported).'.format(
  mbox_path,
  i - 1)
)
