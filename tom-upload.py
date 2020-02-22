import os
import json
import requests
import re
import secrets
import config

def upload_episode(ep_number, ep):
  # CREATE EPISODE
  # build the data to upload
  payload = with_bot_token( {"number":            ep_number,
                             "title":             ep['title'],
                             "slug":              re.search(r'[^\/]+$', ep['slug'])[0],
                             "description":       ep['description'],
                             "publish_date":      ep['publish_date'],
                             "notes":             ep['notes'],
                             "draft":             'true',
                             "newsletter_status": 'not scheduled'} )
  print(f'Uploading episode {ep_number}')
  # send off the first request, creating the episode
  response = requests.post(config.create_url, data=json.dumps(payload), headers=config.headers)
  log_request_response(ep_number, payload, response)
  # UPLOAD IMAGES
  # figure out what images we'll be uploading for this episode
  image_filenames = []
  for file in os.listdir(config.files+ep_number):
    if not re.search(r'\.mp3$', file):
      image_filenames.append(file)
  # upload each image and its caption
  for index, image_filename in enumerate(image_filenames):
    with open(config.files+ep_number+'/'+image_filename, 'rb') as f:
      response = requests.request("patch", config.image_url+ep_number,
                                data=with_bot_token({'caption':ep['images'][index]['caption']}),
                                files={'file': f},
                                headers=config.headers_without_content)
  # UPLOAD AUDIO
  with open(f'{config.files}{ep_number}/Episode-{ep_number}.mp3', 'rb') as f:
    response = requests.request("patch", config.audio_url+ep_number,
                              data=with_bot_token(),
                              files={'file': f},
                              headers=config.headers_without_content)

def with_bot_token(payload):
  # loads bot_token into the payload.
  if payload is None
    payload = {}
  return {**payload, {'bot_token':secrets.bot_token}}

def log_request_response(ep_number, payload, response):
  # some data is spit out into the command line, but we also can make detailed logs
  if response is None:
    return
  with open(config.logs, 'a+') as f:
    f.write(f'\n\nEpisode #{ep_number} status: {response.status_code}')
    if response.status_code == 422:
      for error, reason in response.json()['errors'].items():
        f.write(f'\nServer didn\'t like {error}, and said {reason}.')
        if error in payload:
          f.write(f'\nI gave it: {payload[error]}')

# START UPLOADING
with open(config.scraped) as f:
  episodes_dict = json.load(f)
# if you want to test with only a few objects in the JSON, try for/in sorted(episodes_dict.items())[0:2]:
for ep_number, episode in episodes_dict:
  upload_episode(ep_number, episode)
