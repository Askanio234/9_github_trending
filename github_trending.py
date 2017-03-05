import requests
import datetime


SEARCH_PERIOD_DAYS = 7

TOP_SIZE = 20


def get_trending_repositories(top_size, date_created):
    url_parameters = {"q": "created:>={}".format(date_created),
                        "sort": "stars", "order": "desc", "page": 0,
                        "per_page": top_size}
    response = requests.get("https://api.github.com/search/repositories",
                            params=url_parameters)

    if response.status_code == 200:
        return response.json()["items"]
    else:
        print("Нет ответа от сервера")


def sort_repos_based_on_issues_count(trending_repos):
    return sorted(trending_repos, key=lambda repo: repo["open_issues_count"],
                    reverse=True)


def print_sorted_repos(repos):
    number = 1
    for repo in repos:
        print("{} - {} with {} issues, link - {}".format(number,
                    repo["full_name"], repo["open_issues_count"],
                    repo["svn_url"]))
        number += 1


if __name__ == '__main__':
    date_today = datetime.date.today()
    repo_date_created = date_today - datetime.timedelta(SEARCH_PERIOD_DAYS)
    trending_repos = get_trending_repositories(TOP_SIZE, repo_date_created)
    print_sorted_repos(sort_repos_based_on_issues_count(trending_repos))
