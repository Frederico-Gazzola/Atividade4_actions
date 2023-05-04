from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests
import csv

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

credentials_dict = {
  "type": "service_account",
  "project_id": "probable-quest-382223",
  "private_key_id": "3270d0d1d416b8b4b4453ad5212f2451b7f6c59f",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCblwaEHN8oIk72\nDuXhzFeFCjN0FViWqmDD3UTt5nLMUoqbDu6KzGXjQ1c4b3Jsw8/8J5YhC1Uz0HXC\n1H2/vEw+3xl3vAay+Hkfmhf9aygXiVDTIW9D3RwkjTvADJM10hz1l27zOSr2uOpq\nYV5gEvgGw63HrlfuLtZB7v4YDsVjZCfizcDZlfsViE48uY7gZ2NQR5NU7thAkr0V\nxVIM34q2/7C8e6ZF7pUStL/Rz3821u7PIanrgGq8Ga7IQZoLCcWjNwaLHJbcWaOQ\nY7/7Natn1jKwfCdVQMACIGJr/0dKKXuoA59Ub9VVo/0aVCAnVSzd6juWsrC279OK\n8P5BQkerAgMBAAECggEAAvwiByeryOJTCudqjL1oH9rXh9woZ6ON/a9hdQHK7kxE\nOna73s/OeJeJbBy/O/BeUho444f413rrCblll56ActF5K3ZzRU7YcJiffFdDyqM7\nCwHgfCXP7R5yOyVnL00AMYMdyjfjjGdQn/ax9GEIyDveOgqaoqy3o9h2oFGHFVQG\nKDL+FeQyoD2uW31iDh5g8GwRPSL+7H3fGusTXhJeKjYLNmODvVRpV4zteFA4UoKp\nEBZwKyCR5PYVNfGZtNUzjEwLkn0D8YHfdPHLls6YbU4CnRGvDfTNBZ30uK4qmWFG\nyfDs8a+tURxssiHqNJA35PJccVM72ADJpXKPUmGWQQKBgQDbq6VVCe4RGOyXPtYz\ny1J82mn0JorSmz6Ms0PZQMMYK/RQlR0kHisd6tg5FYHYCnPX8os8zv/0THXfgQUY\nPHapsFTzLacCTfounVKD/JwhIuP6Vh5kLXFSPnZRZ+lpkqHT3KdW8DM5HfZG0JpI\n5a6qakjwFtGjsaBR4H0ob5LjiwKBgQC1Ulp7KfkyHzfaAe0MH6sgPWfFCnLnEBBZ\n/mhXFXc9ZggW9/Qqx12UirvE/fzzcBPTQVUSiKUFd9FxNBsoGY1cCyq0db6AlTd/\nbdpajy+OL/jl2CrzQJ9Sgut5SCTn2DEG+53mETXrYQGrS7mY+ENuZ+KEbf94oDCZ\nf7W8jdAwYQKBgQC2Fg2x8802tuZGaHu96yew/osdKmWgNbcfgekXyKru+mBF+5Rw\nP+GVpvkcOEus/N0Rf6cS/LMFmeuLHLNQZ64k8lk4SftJ2cErqpSfe2EfxoAbHg+L\nEnAAsG37BJtiO32Q1DKRygFrsv5VrMx26IxkDj3vZbrYaYBu3hpgzjuACQKBgBht\nYM0o6W5sMD0Jd2LjvU0ZmKo97x7b1igZkvrwZGD8JujZPKaqtxu02Pj/8pzlI3aZ\nXZmimQC0lJ24lFQBpT6aLoWjOyfdcl2TchAzLAfuxIxKY/bjZNNb2dc79eTaBjjX\nmv0MooP0TKJEEFvgTk1IZ4bJvtoEUqfLQbOGM17hAoGAK31UxrHVzk7YDsbKFiqI\nBDi3MrGRrR99TviTWvIUK7uRIS90Yf3TtIGmOV2d2Tda1V5LHrkserJdjxwiJbL9\nry8ZdhQRTtVZBn0JMl64BLH4J5klmsF6yeRG0yx3YZaXMjcluREaVYhiKqHIQoGJ\n/r6eBO72ZF/OqLNtUzg3DzE=\n-----END PRIVATE KEY-----\n",
  "client_email": "myaccount@probable-quest-382223.iam.gserviceaccount.com",
  "client_id": "104503412617853275231",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/myaccount%40probable-quest-382223.iam.gserviceaccount.com"

}

try:

  """Uploads a file to the bucket."""
  credentials = service_account.Credentials.from_service_account_info(credentials_dict)
  storage_client = storage.Client(credentials=credentials)
  bucket = storage_client.get_bucket('artists_names') ### Nome do seu bucket
  blob = bucket.blob('artist-names.csv')

  pages = []
  names = "Name \n"

  for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + str(i) + '.htm'
    pages.append(url)

  for item in pages:
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'html.parser')

    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    artist_name_list = soup.find(class_='BodyText')
    artist_name_list_items = artist_name_list.find_all('a')

    for artist_name in artist_name_list_items:
      names = names + artist_name.contents[0] + "\n"

    blob.upload_from_string(names, content_type="text/csv")

except Exception as ex:
  print(ex) 
