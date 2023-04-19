import requests
from bs4 import BeautifulSoup


class Hanime_Brain:
    def __init__(self):
        self.url = "https://hentaihaven.xxx"
        r = requests.get(self.url)
        response = r.content
        self.soup = BeautifulSoup(response, "html.parser")

    def main_page(self):
        items = self.soup.find_all("div", class_="page-item-detail")

        # * Main Page Content
        page_items = []
        for i in items:
            a_tag = i.a
            a_tag_link = (a_tag["href"]).replace(
                "https://hentaihaven.xxx/watch/", "")
            a_tag_link = a_tag_link.replace("/", "")
            img_tag = str(a_tag.img)
            img_link = img_tag.replace(
                '<img alt="" class="img-responsive" decoding="async"', "")
            img_link = img_link.replace('data-src="', "")
            img_link = img_link.replace('src="', "")
            img_link = img_link.replace(
                '<img alt="" class="img-responsive owl-lazy"', "")
            img_link = img_link.replace('"/>', "")
            info = {
                "title": a_tag["title"],
                "img": img_link,
                "page_link": a_tag_link
            }
            page_items.append(info)

        # * Main Page Genres
        genres = self.soup.find("div", class_="tagcloud")
        genres_tags = []
        genres_links = genres.find_all("a")

        for i in genres_links:
            tags = {
                'genre': i.text,
                'genre_link': (i['href']).replace("https://hentaihaven.xxx/series/", "")
            }
            genres_tags.append(tags)

        full_mpage_info = {
            "contents": page_items,
            "genres": genres_tags
        }
        return full_mpage_info

    def hanime_page(self, name):
        url = f"https://hentaihaven.xxx/watch/{name}"
        r = requests.get(url)
        response = r.content
        soup = BeautifulSoup(response, "html.parser")

        title = soup.find("h1")
        page_title = title.text.replace("\n", "")

        main_img = (soup.find("img", class_="img-fluid"))["src"]

        info = soup.find("div", class_="post-content")
        rating = info.find_all("div", class_="post-content_item")
        info_list = []
        for i in rating:
            r = i.find("div", class_="summary-content").text
            r = r.replace("\n", "")
            info_list.append(r)

        episodes = soup.find_all("li", class_="wp-manga-chapter")
        episodes_info = []
        for ep in episodes:
            ep_info = {
                "ep_num": (ep.a.text).replace("\n", ""),
                "ep_thumbnail": ep.img["src"],
                "ep_link": (ep.a["href"]).replace("https://hentaihaven.xxx/watch/", ""),
                "ep_date": ep.span.text
            }
            episodes_info.append(ep_info)

        summary = soup.find("div", class_="description-summary")
        all_summary = summary.find_all("p")
        all_summary[0] = (all_summary[0].text).replace("\n", "")
        try:
            all_summary[1] = (all_summary[1].text).replace("\n", "")
        except IndexError:
            pass
        main_summary = (str(all_summary)).replace("[", "")
        main_summary = main_summary.replace("]", "")
        full_page_details = {
            'title': page_title,
            'img': main_img,
            'details': info_list,
            'summary': main_summary,
            'episodes': episodes_info
        }
        return full_page_details

    def watch_page(self, name, ep_num):
        url = f"https://hentaihaven.xxx/watch/{name}/{ep_num}/"

        r = requests.get(url)
        response = r.content

        soup = BeautifulSoup(response, "html.parser")
        video = soup.find("div", class_="player_logic_item")

        episode = soup.find("div", class_="c-selectpicker")
        episode = episode.text.replace("\n", "")

        heading = soup.find("h1")
        heading = heading.text.replace("\n", "")

        data = {
            'title': heading,
            'episode_num': episode,
            'video_link': video.iframe["src"]
        }
        return data

    def pick_your_poison(self):
        url = "https://hentaihaven.xxx/pick-your-poison"
        r = requests.get(url)
        response = r.content
        soup = BeautifulSoup(response, "html.parser")

        genres_list = []
        years_list = []
        tags_list = []
        temp = soup.find_all("div", class_="zterms")

        # * Genres
        temp_g_list = []
        for i in temp[0]:
            if i == '\n':
                pass
            else:
                temp_g_list.append(i)

        for s in temp_g_list:
            info = {
                'genre': (s.text).replace("\n", ""),
                'genre_link': (s["href"]).replace("https://hentaihaven.xxx/", "")
            }
            genres_list.append(info)

        # * Years
        temp_years = temp[1]
        temp_y_list = []
        for i in temp_years:
            if i == '\n':
                pass
            else:
                temp_y_list.append(i)

        for year in temp_y_list:
            info = {
                'year': (year.text).replace("\n", ""),
                'year_link': year["href"].replace("https://hentaihaven.xxx/", "")
            }
            years_list.append(info)

        # * Tags
        temp_tags = temp[2]
        temp_t_list = []
        for i in temp_tags:
            if i == '\n':
                pass
            else:
                temp_t_list.append(i)

        temp_t_list[-1] = None

        for tags in temp_t_list:
            if tags != None:
                y = tags["href"].replace("https://hentaihaven.xxx/", "")
                text = (tags.text).replace("\n", "")
            info = {
                'tags': text,
                'tags_link': y
            }
            tags_list.append(info)

        pyp_full_info = {
            'genres': genres_list,
            'years': years_list,
            "tags": tags_list
        }
        return pyp_full_info

    def series_page(self, tag):
        url = f"https://hentaihaven.xxx/series/{tag}/"

        r = requests.get(url)
        response = r.content

        soup = BeautifulSoup(response, "html.parser")

        all_content = soup.find("div", class_="page-content-listing")

        main_contents = all_content.find_all("div", class_="page-listing-item")
        series_list = []
        for content in main_contents:
            data = content
            data_list = data.find_all("div", class_="item-thumb")
            for i in data_list:
                info = {
                    'title': i.a["title"],
                    'img': i.a.img["src"],
                    'page_link': (i.a["href"]).replace(
                        "https://hentaihaven.xxx/watch/", "")
                }
                series_list.append(info)
        return series_list
