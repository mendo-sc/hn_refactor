from operator import itemgetter

import requests

def check_status():
    """Make an API call and check the response.

    Returns:
        Response: Server data from url
    """
    url = "https://hacker-news.firebaseio.com/v0/topstories.json"
    r = requests.get(url)
    print(f"Status code: {r.status_code}")
    return r

def make_api_call(submission_id):
    """Make a new API call for each submission

    Args:
        submission_id (_type_): _description_
    """
    url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
    r = requests.get(url)
    print(f"id: {submission_id}\tstatus: {r.status_code}")
    response_dict = r.json()
    return response_dict
    
def build_article_dict(submission_dicts, submission_id, response_dict):
    """Build a dictionary for each article

    Args:
        submission_dicts (_type_): _description_
        submission_id (_type_): _description_
        response_dict (_type_): _description_
    """
    submission_dict = {
            'title': response_dict.get('title', 'None'),
            'hn_link': f"https://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict.get('descendants', -1),
        }
    submission_dicts.append(submission_dict)

def print_article_info(submission_dicts):
    for submission_dict in submission_dicts:
        print(f"\nTitle: {submission_dict['title']}")
        print(f"Discussion link: {submission_dict['hn_link']}")
        print(f"Comments: {submission_dict['comments']}")

def main():
    r = check_status()
    submission_ids = r.json()

    submission_dicts = []
    for submission_id in submission_ids[0:30]:
        response_dict = make_api_call(submission_id)
        build_article_dict(submission_dicts, submission_id, response_dict)

    submission_dicts = sorted(submission_dicts, key=itemgetter('comments'),
                            reverse=True)

    print_article_info(submission_dicts)

if __name__ == '__main__':
    main()