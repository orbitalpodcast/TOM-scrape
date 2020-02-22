# CONFIGURE HTTP
# What domain are we scraping?
scrape_domain = 'http://www.theorbitalmechanics.com'

# What domain are we posting to?
upload_domain = 'http://localhost:3000/'

# what path are we posting to?
create_path = 'episodes/'
create_url = upload_domain+create_path

# What path are we patching to?
image_path = 'episodes/upload_image/'
audio_path = 'episodes/upload_audio/'
# make it easy
image_url = upload_domain+image_path
audio_url = upload_domain+audio_path

# What headers to use while uploading?
headers = {'user-agent': 'TOM-upload V1.0', 'Accept': 'application/json', 'Content-Type': 'application/json'}
headers_without_content = headers.copy()
headers_without_content.pop('Content-Type')

# How many seconds should we sleep between requests (to avoid throttling)?
sleep_interval = 5

# CONFIGURE LOCAL FILES
# Where to output text? Be sure to initialize this file with {}.
scraped = 'scraped.json'

# Where to store detailed logs?
logs = 'log.txt'

# What folder to store images and audio in?
files = 'files/'


# Be sure to create a file secrets.py that sets bot_token!
