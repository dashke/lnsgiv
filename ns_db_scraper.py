import os
import requests
import json
import re

# Replace with your IGDB API credentials
client_id = ''
client_secret = ''

def get_igdb_token(client_id, client_secret):
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()['access_token']

def get_game_info(game_name, token):
    url = 'https://api.igdb.com/v4/games'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = f'search "{game_name}"; fields id, name, platforms; where platforms = (130);'
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

def get_detailed_game_info(game_id, token):
    url = 'https://api.igdb.com/v4/games'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = f'fields *; where id = {game_id};'
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()

def download_image(image_id, folder_path, image_type, token):
    url = f'https://api.igdb.com/v4/{image_type}'
    headers = {
        'Client-ID': client_id,
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    data = f'fields url; where id = {image_id};'
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    image_info = response.json()
    if image_info:
        image_url = 'https:' + image_info[0]['url']
        image_response = requests.get(image_url)
        image_response.raise_for_status()
        with open(os.path.join(folder_path, f"{image_id}.jpg"), 'wb') as f:
            f.write(image_response.content)
        print(f'Downloaded {image_type} image {image_id}')

def extract_game_name(folder_name):
    match = re.match(r'^\d* ?(.*?)( \[.*)?$', folder_name)
    if match:
        return match.group(1)
    return folder_name

def try_alternate_names(game_name, token):
    base_name = re.sub(r'\d.*', '', game_name).strip()
    variations = [base_name] + [f"{base_name} {i}" for i in range(1, 4)]
    for variation in variations:
        try:
            game_info = get_game_info(variation, token)
            if game_info:
                return game_info
        except Exception as e:
            print(f'Error retrieving info for {variation}: {e}')
    return None

def main(folder_path):
    token = get_igdb_token(client_id, client_secret)
    script_directory = os.path.dirname(os.path.abspath(__file__))
    info_file_path = os.path.join(script_directory, 'game_info.json')
    images_folder_path = os.path.join(script_directory, 'images')
    os.makedirs(images_folder_path, exist_ok=True)

    # Load existing game info if it exists
    if os.path.exists(info_file_path):
        with open(info_file_path, 'r') as f:
            existing_game_info = json.load(f)
    else:
        existing_game_info = []

    choice = input("Choose an option:\n1. Retrieve all data from the start\n2. Append/add new titles only\n3. Remove titles from the database that don't exist anymore\nEnter the number of your choice: ")

    if choice == '1':
        # Retrieve all data from the start
        game_info_list = []
        for folder_name in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, folder_name)):
                game_name = extract_game_name(folder_name)
                try:
                    game_info = get_game_info(game_name, token)
                    if not game_info:
                        print(f'No information found for {game_name}, trying variations...')
                        game_info = try_alternate_names(game_name, token)
                    if game_info:
                        detailed_info = get_detailed_game_info(game_info[0]['id'], token)
                        game_info_list.append({game_name: detailed_info})
                        print(f'Saved info for {game_name}')
                        
                        # Download cover image
                        if 'cover' in detailed_info[0]:
                            download_image(detailed_info[0]['cover'], images_folder_path, 'covers', token)
                        
                        # Download screenshots
                        if 'screenshots' in detailed_info[0]:
                            for screenshot_id in detailed_info[0]['screenshots']:
                                download_image(screenshot_id, images_folder_path, 'screenshots', token)
                    else:
                        print(f'No information found for {game_name} even after trying variations.')
                except Exception as e:
                    print(f'Error retrieving info for {game_name}: {e}')
        
        with open(info_file_path, 'w') as f:
            json.dump(game_info_list, f, indent=4)

    elif choice == '2':
        # Append/add new titles only
        existing_titles = {list(game.keys())[0] for game in existing_game_info}
        for folder_name in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, folder_name)):
                game_name = extract_game_name(folder_name)
                if game_name not in existing_titles:
                    try:
                        game_info = get_game_info(game_name, token)
                        if not game_info:
                            print(f'No information found for {game_name}, trying variations...')
                            game_info = try_alternate_names(game_name, token)
                        if game_info:
                            detailed_info = get_detailed_game_info(game_info[0]['id'], token)
                            existing_game_info.append({game_name: detailed_info})
                            print(f'Saved info for {game_name}')
                            
                            # Download cover image
                            if 'cover' in detailed_info[0]:
                                download_image(detailed_info[0]['cover'], images_folder_path, 'covers', token)
                            
                            # Download screenshots
                            if 'screenshots' in detailed_info[0]:
                                for screenshot_id in detailed_info[0]['screenshots']:
                                    download_image(screenshot_id, images_folder_path, 'screenshots', token)
                        else:
                            print(f'No information found for {game_name} even after trying variations.')
                    except Exception as e:
                        print(f'Error retrieving info for {game_name}: {e}')
        
        with open(info_file_path, 'w') as f:
            json.dump(existing_game_info, f, indent=4)

    elif choice == '3':
        # Remove titles from the database that don't exist anymore
        existing_folders = {extract_game_name(folder_name) for folder_name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, folder_name))}
        updated_game_info = []
        for game in existing_game_info:
            game_name = list(game.keys())[0]
            if game_name in existing_folders:
                updated_game_info.append(game)
            else:
                game_id = game[game_name][0]['id']
                # Remove associated images
                cover_image_path = os.path.join(images_folder_path, f"{game[game_name][0].get('cover', '')}.jpg")
                if os.path.exists(cover_image_path):
                    os.remove(cover_image_path)
                for screenshot_id in game[game_name][0].get('screenshots', []):
                    screenshot_image_path = os.path.join(images_folder_path, f"{screenshot_id}.jpg")
                    if os.path.exists(screenshot_image_path):
                        os.remove(screenshot_image_path)
                print(f'Removed info and images for {game_name}')
        
        with open(info_file_path, 'w') as f:
            json.dump(updated_game_info, f, indent=4)
        print("Updated game information to remove non-existing titles.")

if __name__ == '__main__':
    folder_path = input('Enter the path to the folder with your Nintendo Switch games: ')
    main(folder_path)