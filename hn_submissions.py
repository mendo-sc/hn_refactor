from operator import itemgetter

import requests

def check_status(url):
    """Make an API call and check the response.

    Returns:
        Response: Server data from url
    """
    r = requests.get(url)
    print(f"Status code: {r.status_code}")
    return r

def make_api_call(url, submission_id):
    """Make a new API call for each submission

    Args:
        submission_id (_type_): _description_
    """
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()
    return response_dict
    
def build_article_dict(response_dict, url) -> dict:
    """Builds a dictionary for each article.

    Args:
        response_dict (_type_): _description_
        url (str): URL of Hacker News article
    """
    submission_dict = {
            'title': response_dict.get('title', 'None'),
            'hn_link': url,
            'comments': response_dict.get('descendants', -1),
        }
    return submission_dict

def print_article_info(submission_dicts):
    for submission_dict in submission_dicts:
        print(f"\nTitle: {submission_dict['title']}")
        print(f"Discussion link: {submission_dict['hn_link']}")
        print(f"Comments: {submission_dict['comments']}")

def main():
    main_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    r = check_status(main_url)
    submission_ids = r.json()

    submission_dicts = []
    for submission_id in submission_ids[0:30]:
        sub_url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
        response_dict = make_api_call(sub_url, submission_id)

        hn_link = f"https://news.ycombinator.com/item?id={submission_id}"
        submission_dict = build_article_dict(response_dict, hn_link)
        submission_dicts.append(submission_dict)

    submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                            reverse=True)

    print_article_info(submission_dicts)

if __name__ == '__main__':
    main()