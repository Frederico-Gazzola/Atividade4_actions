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
  "private_key_id": "2ab785a4062921946e3f09241b94b1cbfcbd806b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxLx2GIFkCOL9Z\nWzO9cLZaVajZS0mEBM4JVOXsG4zT8SwOSLP/cQTqnp4fSCpTyzL2nNO4W1/y/XcI\ntZRJvuihTFyvNG4qz0MLR3ay5xl48ut5JztGM+eM0O/xVyr/IrSBLtzfjrmLH//J\n+G2NmeeVaZpGNpuH5/JNx7lwPCcpZFBA6hnbwTVaxG/8Sd6LRgjaWILs+IjeW3wd\nmUJBJBzfq0QxGfJvzOuipFk4/0KV8OdqmWKbfyxUcrdMzuzdYeqybeSQxWUgJuc3\nkpMRq5COTTe2W7UZECzRZbLqxxWCNYZX0I9u/+Y3gqhJoCBH9gSHv5wH8FcJNYOI\nGcv51DuLAgMBAAECggEAG7XxrnYaqu/zGpIv9Qh5YdwUbJTgv4ang+rE4XisPW1y\nOshWFl+M/vX7EYtjdfgeqqvQ/6aSyq780d420z3J+4gKKtX5W4qkwqZ/mEVFGkHB\nCrv/AjYV7akJDbwDRnnICeLUD8auRWWmHJFU7kN2u6BozLhiT2QQOj0/8Z9cGes1\nYFgSKWLeVmJ1y80lUWIaKISef0XoEX7f/T4CfAT9prSfahHePqfmGb5ji1pj7Fba\nyKnOcOcZBm/uNz4XRQyCw5F3ii8yJQpWz+QVMLAiACx7WBr+huGPZDTiNPdVWsaB\nJs1WL8qVMDXQ75rDfFtIwRZA1/SQTJoZNvyHDTJXKQKBgQDfvSeZioyryDyV2533\nLckO8XaxESVA+Mg5yae/K0Y2Kf2dU8rzP8xRpOOh6dYY4g9LKI1EIYcO5WSKBcau\ny0R+fy/cQVssUmpKnNSlou6UZOn/NpzLbhJ9NF/H/CSJ2qsp8p6svNrDiK21LqRj\nXFLESs3UGx2KTYVDMthMTieZ1QKBgQDKu3zWcxBtqtq8aFBLrIcvtccPsdaT2S4V\nitEOz6Vt7mja/VilglIwXdVMOZ/aLzqOgg40xWBPYbGwhBNCy8/RODCxPieNNbF1\nk8SNchGUYIG+38esCZ26ZHHUm2RFc4sHXi5Sj+Q45oVUWEINe6pzH1bBCOMC62Zx\nNbNOlyrP3wKBgB9dIcb5UBzole2f+rXiujOZD71knOdNuKu5JAW9aDtBiabbTzDo\nOZkcVzikUfns/p3Xkm4BkTA6YeyjQKXSIsjkxW3Hz6MX7oSFFZ4eh/lPaCn5muM9\ni+P3SpH7O5gDikj4FNw8ISKV71vdrPeswoF3xwC7yFlR4qN35jBUKGL9AoGBAJG8\nhdmDjePIVsXqFw7PT780ZY0awq42CbLiv7Zt/vYv1KDYTslsDblHOvY41nj6SpX3\nWE8HNFzcVegWieISsaotQpOnorcYSiHDwCAOSCTp21tjcx5xKzm6yzmTG1nx3ZfG\nVHZ1ihJ9ZItlhtY6eCWZ+bt6r/aBUns/p05vzQ7xAoGBAKZFlOewXhcDzCjypLs+\ng9nFq5WCSK/JrNcqirpw5C2+jI9fAuX/en9aqhestvfPKd1jJRWJTtUL8i+iFEWn\nZdqo86BKR05bIwd+3AAZDGlUDp8iTEQMJjHZE+edxiydYUMzcEXVCwnNmRElWt30\nkIi5t7sMXQdhY2DOKivX49XP\n-----END PRIVATE KEY-----\n",
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
