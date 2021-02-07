import os

import pandas as pd
import requests
from requests_html import HTML


def get_previous_ten_years(from_year=2011, to_year=2020, directory_name="movie-data-from-last-10-yrs"):
    absolute_path = os.path.abspath(directory_name)
    os.mkdir(absolute_path)
    for i in range(from_year, to_year + 1):
        url = f"https://www.boxofficemojo.com/year/world/{i}/"
        request = requests.get(url)
        if request.status_code == 200:
            r_html = HTML(html=request.text)
            table = r_html.find("table")
            if len(table) == 1:
                table = table[0]
                tr_s = table.find("tr")
                if len(tr_s) > 0:
                    header = tr_s[0].text.split("\n")
                    final_matrix = []
                    for j in tr_s[1:]:
                        final_matrix.append(j.text.split("\n"))
                    df = pd.DataFrame(final_matrix, columns=header)
                    path = os.path.join(absolute_path, f"movie-data-{i}.csv")
                    df.to_csv(path, index=False)
        print(f'{i}: done!')


get_previous_ten_years()
print("All Done")
