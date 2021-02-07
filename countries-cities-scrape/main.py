# script to scrape a list of countries from "https://unece.org/cefact/unlocode-code-list-country-and-territory"
import requests
from requests_html import HTML

URL = "https://unece.org/cefact/unlocode-code-list-country-and-territory"


def get_file():
    response = requests.get(URL)
    html = HTML(html=response.text)
    tbody = html.find("thead")
    all_rows = tbody[0].find("tr")
    file = open("../job-portal-countries-list-dump.csv", "w")
    for i in range(1, (len(all_rows))):
        single_row = all_rows[i].text.split("\n")
        country_code = single_row[0]
        country_name = single_row[1]
        file.write(country_code + "," + country_name + "\n")
    file.close()


get_file()

file_input_countries = open("job-portal-countries-list-dump.csv", "r")
all_countries = file_input_countries.readlines()
file_input_countries.close()
final_json_file = open("job-portal-countries.json", "w")
final_list = []

def create_final_json():
    MAIN_URL = "https://service.unece.org/trade/locode/"
    for i in range(1, len(all_countries)):
        current_country_data = all_countries[i].split(",")
        country_code_input = current_country_data[0].lower()
        country_name_input = current_country_data[1]
        final_url = f'{MAIN_URL}{country_code_input}.htm'
        print(f'Processing: {final_url}')
        response = requests.get(final_url)
        if response.status_code == 200:
            html_text = HTML(html=response.text)
            all_rows = html_text.find("table[border='1']")[0]
            all_rows = all_rows.find("tr")
            list_of_cities = []
            for i in range(1, len(all_rows)):
                single_row = all_rows[i].find("td")
                city_code = single_row[1].text
                city_name = single_row[2].text
                single_state_object = {"cityCode": city_code, "cityName": city_name}
                list_of_cities.append(single_state_object)
            current_dict_country = {"countryName": country_name_input, "countryCode": country_code_input, "link": final_url, "cities": list_of_cities}
            final_list.append(current_dict_country)
json.dump(final_list, final_json_file)
create_final_json()
json.dump(final_list, final_json_file)