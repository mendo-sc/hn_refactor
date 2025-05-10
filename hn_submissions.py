from operator import itemgetter

import requests

def main_api_call(url:str) -> requests.Response:
    """Makes an API call to top stories server. Returns response and prints status code.

    Args:
        url (str): URL of JSON data with Hacker News top stories IDs

    Returns:
        requests.Response: Response object of main data
    """
    r = requests.get(url)
    print(f"Status code: {r.status_code}")
    return r

def submission_api_call(url:str, submission_id:int) -> requests.Response:
    """Makes a API call to a submission server. Returns response and prints id and status code.

    Args:
        url (str): URL of JSON data with info of each article
        submission_id (int): ID of each article

    Returns:
        requests.Response: Response object of submission data
    """
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    return r

    
def build_article_dict(response_dict:dict, url:str) -> dict[str,str,int]:
    """Builds a custom dictionary for each article including title, link, and comments.

    Args:
        response_dict (dict): Dictionary of all information of each article
        url (str): URL of Hacker News article
    """
    submission_dict = {
            'title': response_dict.get('title', 'None'),
            'hn_link': url,
            'comments': response_dict.get('descendants', -1),
        }
    return submission_dict

def print_article_info(submission_dicts:list) -> None:
    """Prints title, discussion link, and comments of each submission dictionary.

    Args:
        submission_dicts (list): A list of all submission dictionaries
    """
    for submission_dict in submission_dicts:
        print(f"\nTitle: {submission_dict['title']}")
        print(f"Discussion link: {submission_dict['hn_link']}")
        print(f"Comments: {submission_dict['comments']}")

def main():
    main_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    main_r = main_api_call(main_url)
    submission_ids = main_r.json()

    submission_dicts = []
    for submission_id in submission_ids[0:30]:
        sub_url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
        submission_r = submission_api_call(sub_url, submission_id)
        response_dict = submission_r.json()

        hn_link = f"https://news.ycombinator.com/item?id={submission_id}"
        submission_dict = build_article_dict(response_dict, hn_link)
        submission_dicts.append(submission_dict)

    submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                            reverse=True)

    print_article_info(submission_dicts)

if __name__ == '__main__':
    main()