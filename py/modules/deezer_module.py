import requests



def get_content(url):
    response = requests.get(url)
    return response.content



def get_charts():
    endpoint = "https://api.deezer.com/chart"
    
    params = {
        "top": "RU"
    }
   
    response = requests.get(endpoint, params = params)

    if response.status_code != 200:
        return None

    data = response.json()
    
    return data



def search(query, type):
    endpoint = "https://api.deezer.com/search"
    params = {
        "q": query,
        "type": type
    }
    
    response = requests.get(endpoint, params = params)

    if response.status_code != 200:
        print("Не удалось получить данные")
        return None
    
    data = response.json()['data']

    for item in data:
        if type == "track" and type == item['type']:
            return item
        elif type == "artist" and type == item['artist']['type']:
            return item['artist']

    return None



if __name__ == "__main__":
    pass