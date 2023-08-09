import os
import requests
from bs4 import BeautifulSoup

url = "https://songs.bardmusicplayer.com"

response = requests.get(url)
html = response.text

soup = BeautifulSoup(html, 'html.parser')
midi_entries = soup.find_all('div', class_='midi-entry')

download_directory = "songs"  # Directory to save the downloaded MIDI files

if not os.path.exists(download_directory):
    os.makedirs(download_directory)
for i in range(5):
    for entry in midi_entries:
        title_element = entry.find('a', class_='mtitle')
        if title_element:
            title = title_element.get_text(strip=True)
            sanitized_title = "".join(c if c.isalnum() or c in ' -_' else '' for c in title)
            download_link = f'https://songs.bardmusicplayer.com/{title_element["href"]}'
            response = requests.get(download_link)
            
            if response.status_code == 200:
                file_extension = download_link.split('.')[-1]
                filename = f"{sanitized_title}.{file_extension}"
                filename = f"{filename.split('.com')[0]}.midi"
                filepath = os.path.join(download_directory, filename)
                
                with open(filepath, 'wb') as file:
                    file.write(response.content)
                
                print(f"Downloaded: {filename}")
            else:
                print(f"Failed to download: {title}")
