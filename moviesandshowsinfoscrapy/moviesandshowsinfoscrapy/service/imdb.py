import moviesandshowsinfoscrapy.service.curl_manager as curl_manager
import requests

def get_top_ten_this_week():
    """ Retrieves the top 10 movies and tv shows on imdb website """
    try:
        curl_path = curl_manager.retrieve_curl_path(0)
        response = eval(curl_manager.convert_to_request(curl_path))
        top_ten = obtain_top_ten_from_json(response.json())
    except Exception as e:
        return {
            "message": "An exception was caught during the execution of the program",
            "error": f'{e}'
        }

    return top_ten

def obtain_top_ten_from_json(json):
    """ Selects only the desired data from the api response """
    list_top_ten = []
    items = json["data"]["topMeterTitles"]["edges"]
    for item in items:
        item = item["node"]
        item_dict = {
            "ranking": item["meterRanking"]["currentRank"],
            "name": item["titleText"]["text"],
            "rating": item["ratingsSummary"]["aggregateRating"],
            "id": item["id"],
            "category": item["titleType"]["text"],
            "img_url": item["primaryImage"]["url"],
            "genre": ", ".join([genre["genre"]["text"] for genre in item["titleGenres"]["genres"]])
        }
        list_top_ten.append(item_dict)
    return list_top_ten

#print(get_top_ten_this_week())
