import re
import moviesandshowsinfoscrapy.service.curl_manager as curl_manager
import requests

CATEGORIES = [
    'coming-soon',
    'new-releases',
    'comedy',
    'romance',
    'science-fiction',
    'war'
]


def get_tasteio(category=None, limit=5):
    """ Retrieves movies and tv shows data from taste.io website """
    try:
        curl_path = curl_manager.retrieve_curl_path(1)
        request_obj = curl_manager.convert_to_request(curl_path)
        if category is None:
            return get_all(request_obj=request_obj, limit=str(limit))
        else:
            request_adj, category = get_category(request_obj=request_obj, limit=str(limit), category=category)
            return execute_api([(request_adj, category)])

    except Exception as e:
        return {
            "message": "An exception was caught during the execution of the program",
            "error": f'{e}'
        }


def get_all(request_obj, limit):
    """ Adjusts the parameters from a request object for every category """
    list_request_adj = [get_category(request_obj, limit, category) for category in CATEGORIES]

    return execute_api(list_request_adj)


def get_category(request_obj, limit, category):
    """ Adjusts the parameters from a request object for a specific category """
    request_adj, _ = adjust_curl_params(request_obj, '0', limit, category)
    return request_adj, category


def execute_api(list_request_adj):
    """ Calls taste.io's api and selects only the desired data from the response """
    movies_and_shows_dic = {}
    for request_adj, category in list_request_adj:
        response = eval(request_adj).json()["items"]
        list_movies_and_shows = []
        for item in response:
            item_dict = {
                "name": item["name"],
                "category": item["category"],
                "poster_image": item["poster"],
                "title_image": item["backdropTitle"],
                "description": item["description"],
                "trailer_site": item["trailer"].get("site") if item["trailer"] else None,
                "trailer_key": item["trailer"].get("key") if item["trailer"] else None,
                "genre": item.get("genre")
            }
            list_movies_and_shows.append(item_dict)
        movies_and_shows_dic.update({f'{category}': list_movies_and_shows})
    return movies_and_shows_dic


def adjust_curl_params(request_obj, offset, limit, category):
    """ Adjusts the parameters from a request object """
    pattern = r'(?<=id=)[^&]*'
    request_obj = re.sub(pattern, category, request_obj)

    return request_obj.replace("&offset=20", "".join(["&offset=", offset])).replace("&limit=20", "".join(
        ["&limit=", limit])).replace("", ""), category


#print(get_tasteio())
