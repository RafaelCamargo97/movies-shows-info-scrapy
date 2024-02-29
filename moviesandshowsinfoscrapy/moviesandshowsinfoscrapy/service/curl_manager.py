import os
import uncurl


def retrieve_curl_path(origin):
    """ Retrieves the curl path for a given origin """
    base_path = os.path.dirname(os.path.dirname(__file__))
    filename = 'curl_tasteio.txt' if origin == 1 else 'curl_imdb.txt'
    return os.path.join(base_path, 'file', filename)


def convert_to_request(path_file):
    """ Converts curl to request call """
    with open(path_file, "r+") as file:
        curl_command = file.read()
        file.truncate(0)
        file.seek(0)
        file.write(clean_curl_cmd(curl_command))
        os.fsync(file.fileno())
        file.seek(0)
        curl_command = file.read()

    return uncurl.parse(curl_command)


def clean_curl_cmd(curl):
    """ Receives a curl (cmd) and adjusts it to be converted by uncurl lib """
    return (curl.replace("^%^", "%").replace(r"^\^", r"\\").replace(" ^", "").replace("--compressed", "")
            .replace("\\\"", "'")).replace("\\'", "")
