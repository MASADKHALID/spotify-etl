import datetime
import json
import requests
import base64
import boto3

# Your Spotify app credentials
client_id = '9e89545cfd634552a45bf253b007dade'
client_secret = '4d96012eca894cfcaa1a20db695b8cc0'

# Spotify's token endpoint URI
token_url = 'https://accounts.spotify.com/api/token'

# Encode client ID and client secret
client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

# Headers for the POST request
headers = {
    'Authorization': f'Basic {client_creds_b64.decode()}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Body of the POST request
data = {
    'grant_type': 'client_credentials'
}

# Send the POST request to the token endpoint
response = requests.post(token_url, headers=headers, data=data)

# Check if the request was successful
if response.status_code == 200:
    token_info = response.json()
    access_token = token_info['access_token']
    print(f"Access token: {access_token}")
else:
    print(f"Failed to get access token. Status code: {response.status_code}")
    print(response.text)
    exit()

# Now use the access token to get data from the Spotify API
# Example: Get information about an artist
artist_id = '3Nrfpe0tUJi4K4DXYWgMUX'  # Example artist ID (BTS)
artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'

# Headers for the GET request
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Send the GET request to the artist endpoint
response = requests.get(artist_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    artist_info = response.json()
    print("Artist Information:")
    print(f"Name: {artist_info['name']}")
    print(f"Genres: {', '.join(artist_info['genres'])}")
    print(f"Popularity: {artist_info['popularity']}")
    print(f"Followers: {artist_info['followers']['total']}")
else:
    print(f"Failed to get artist information. Status code: {response.status_code}")
    print(response.text)

artist_id = '3Nrfpe0tUJi4K4DXYWgMUX'  # Example artist ID (BTS)
artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'

# Headers for the GET request
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Send the GET request to the artist endpoint
response = requests.get(artist_url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    artist_info = response.json()
    artist_data = {
        "Name": artist_info['name'],
        "Genres": artist_info['genres'],
        "Popularity": artist_info['popularity'],
        "Followers": artist_info['followers']['total']
    }
    print("Artist Information:", artist_data)
else:
    print(f"Failed to get artist information. Status code: {response.status_code}")
    print(response.text)
    exit()

# Upload artist data to S3 bucket
s3 = boto3.client('s3')

# Your S3 bucket name
bucket_name = 'spotify-bucket-asad'
# File name to save the data as in S3
file_name = f"spotify_artist_data_{artist_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"

# Convert artist data to JSON
artist_data_json = json.dumps(artist_data)

# Upload JSON data to S3
try:
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=artist_data_json)
    print(f"Successfully uploaded artist data to S3 bucket {bucket_name} with file name {file_name}")
except Exception as e:
    print(f"Failed to upload artist data to S3. Error: {e}")


