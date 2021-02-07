import requests
from requests_html import HTML
import json


def scrape_pick(file_name, category):
    list_universities = []
    URL = f'https://www.topuniversities.com/universities/level/undergrad/subject/{category}'
    MAIN_LINK_UNI = 'https://www.topuniversities.com'
    get_request = requests.get(URL)
    html_text = HTML(html=get_request.text)
    list_of_li_uni = html_text.find(".universities-search-result")[0].find("li.profile-result")

    for i in range(0, len(list_of_li_uni)):
        obj = {}
        single_element = list_of_li_uni[i].find("a")[0]
        name = single_element.find("h2")[0].text
        ranking = ''
        try:
            ranking = single_element.find(".orrange")[0].text
        except IndexError:
            pass
        link = single_element.attrs["href"]
        image_link = ''
        try:
            image_link = single_element.find("div.dp img")[0].attrs["src"]
        except IndexError:
            pass
        obj["name"] = name
        obj["ranking"] = ranking
        obj["link"] = MAIN_LINK_UNI + link
        obj["imageLink"] = image_link
        list_universities.append(obj)

    open_file = open(file_name, "w", encoding="utf8")
    json.dump(list_universities, open_file, ensure_ascii=False)
    open_file.close()


def scrape_final():
    new_file_final = "final_file.json"
    file_o = open(new_file_final, "w", encoding="utf8")

    file_open = "C:\\Users\\themg\\PycharmProjects\\Projects-For-Portfolio\\universities-data-scrape\\inital-list.json"
    pointer = open(file_open, "r", encoding="utf8")
    json_pointer = json.load(pointer)

    for i in range(0, len(json_pointer)):
        link = json_pointer[i]["link"]
        request_get = requests.get(link)
        html = HTML(html=request_get.text)

        sector = ''
        try:
            sector = html.find("div.uni_stats div.container div.pull-left")[1].find("div.val")[0].text
        except IndexError:
            pass

        research_output = ''
        try:
            research_output = html.find("div.uni_stats div.container div.pull-left")[2].find("div.val")[0].text
        except IndexError:
            pass

        students_currently_enrolled = ''
        try:
            students_currently_enrolled = html.find("div.uni_stats div.container div.pull-left")[3].find("div.val")[
                0].text
        except IndexError:
            pass

        faculty_numbers = ''
        try:
            faculty_numbers = html.find("div.uni_stats div.container div.pull-left")[4].find("div.val")[0].text
        except IndexError:
            pass

        under_graduate_list = []
        try:
            li_uni_under_depts = html.find("div.uni_under_depts")[0].find("li")

            for j in range(0, len(li_uni_under_depts)):
                under_graduate_list.append(li_uni_under_depts[j].text)
        except IndexError:
            pass

        post_graduate_list = []
        try:
            li_uni_post_depts = html.find("div.uni_post_depts")[0].find("li")
            for k in range(0, len(li_uni_post_depts)):
                post_graduate_list.append(li_uni_post_depts[k].text)
        except IndexError:
            pass

        json_pointer[i]["sector"] = sector
        json_pointer[i]["researchOutput"] = research_output
        json_pointer[i]["studentsCurrentlyEnrolled"] = students_currently_enrolled
        key = ""
        if faculty_numbers == "Yes":
            key = "scholarshipAvailable"
        else:
            key = "facultyCount"
        json_pointer[i][key] = faculty_numbers
        json_pointer[i]["underGraduateOfferedCourses"] = under_graduate_list
        json_pointer[i]["postGraduateOfferedCourses"] = post_graduate_list
        if i % 50 == 0:
            print(f'{i} records done')


scrape_pick(file_name="inital-list.json", category="computer-science-information-systems")
scrape_final()
