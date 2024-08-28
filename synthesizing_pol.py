import base64
import fire
from pathlib import Path
import re
import csv
import time
import gzip
import vertexai
from vertexai.generative_models import (
    GenerativeModel,
    GenerationConfig,
    Part,
    # SafetySetting,
)
import vertexai.generative_models


def generate(location: str):
    vertexai.init(project="versatile-hub-433711-g9", location="europe-west2")
    model = GenerativeModel("gemini-1.5-pro-001", system_instruction=[system_prompt])
    responses = model.generate_content(
        [
            intro_to_qol_matrix,
            intro_to_housing_crisis,
            housing_crisis_statistic_figure_1,
            housing_crisis_statistic_figure_2,
            geographic_overview,
            electoral_district_population_chart_1,
            """</electoral_district_population_table_snippet>
<electoral_district_population_chart>""",
            electoral_district_population_chart_2,
            """</electoral_district_population_chart>
</geographic_facts>

<public_transportation_statistics>""",
            public_transport_csv_as_text,
            task_instruction_prompt.format(location),
        ],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )

    return "".join([response.text for response in responses])


def main(only_retry: bool = False):
    # input csv input column name: Electoral Divisions
    # output csv output column name: Quality of Life

    # load input csv into list of dicts
    with gzip.open("ed_dataset/irl_ed.csv.gz", "rt") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    if only_retry:
        # load erroneous files
        erroneous_files = Path("erroneous_files.txt").read_text().splitlines()
        erroneous_entries = [
            re.search(
                r"qol_dataset/batch_record_bs10_batch_(?P<batch_start>[0-9]+)\.json",
                file_name,
            ).group("batch_start")
            for file_name in erroneous_files
        ]
        # retry with only the erroneous entries
        retry = list(map(int, erroneous_entries))
    else:
        retry = list(range(len(data)))
    # generate quality of life for each batch of 100 electoral division
    # the responses are in csv format, need to parse them into json format and assign each record to original record
    # the output context size is 8192 to the max, we are counting 10k characters for being on the safe side
    # a single record is roughly 1k characters.
    batch_size = 10

    # VertexAI free tier allows only 5 requests per minute (concurrently)

    quota_per_minute = 5
    call_count = 0
    start_time = None
    elapsed_time = None

    for i in range(0, len(data), batch_size):

        if i not in retry:
            continue

        if elapsed_time is not None and elapsed_time < 60:
            if call_count >= quota_per_minute:
                time.sleep(60 - elapsed_time)
                call_count = 0
                start_time = time.time()
                elapsed_time = 0
        elif elapsed_time is not None and elapsed_time >= 60:
            call_count = call_count - quota_per_minute if call_count >= quota_per_minute else 0
            start_time = time.time()
            elapsed_time = 0

        batch = data[i : i + batch_size]
        query = "".join(
            [
                f"<query_{i + j}>" + row["Electoral Divisions"] + f"</query_{i + j}>"
                for j, row in enumerate(batch)
            ]
        )
        print(query)
        if start_time is None:
            start_time = time.time()
        responses = generate(query)
        elapsed_time = time.time() - start_time
        call_count += 1
        print(responses)
        with open(f"batch_record_bs{batch_size}_batch_{i}.json", "w") as f:
            f.write(responses)


intro_to_qol_matrix = """I need you to generate synthetic data for our Quality of Life index. We are designing an index to present the Quality of Life (hereafter abbreviated as QoL) in areas within Republic of Ireland. The QoL index consists of 6 top level domains, and various secondary level targets within each -- which are all scalar values; additionally, all these scalar values are discrete integer numbers in range of 1-100. Finally, there\'s a final QoL integer ranging from 0 to 100 target score act as some sort of weighted average of the these values. 

First, let me introduce all QoL variables with their descriptions:

<quality_of_life_index>
<a_sense_of_control>
<cost_of_living>
This maps commonly and closest to average cost of food, commute, housing, financing and leisure on monthly basis. This metric is derived from consumer price for groceries, gas, statistics of household loans and many more data sources.
</cost_of_living>
<safety>
This metric is derived from tourism safety index, UN survey on safety, crime reports from police stations, national spending on security and safety, as well as other sources like consumer insurance price for crime hazards and road safety index.
</safety>
<influence_and_contribution>
This metric is a quantification of availability of local representation of communities / cohort groups; index for freedom of expression and participation degree of democratic processes.
</influence_and_contribution>
<essential_services>
A metric derived from number of essential services like hospitals, schools, libraries, and other public facilities in radius;
</essential_services>
</a_sense_of_control>
<health_equity>
<housing_standard>
A metric derived from housing unit\'s energy rating like BER rating; Space (room count and size); type of housing unit; availability of broadband and mobile access, as well as the speed.
</housing_standard>
<air_noise_light>
A metric derived from proximity to heavy traffic (like highway, dual-carriage lanes, airports and other loud venues); air quality index; proximity to city centers etc.
</air_noise_light>
<food_choice>
A metric derived from availability of grocery; restaurant offerings and types.
</food_choice>
</health_equity>
<connection_to_nature>
<green_and_blue_spaces>
A metric derived from proximity to parks, forests, natural waterways and seashores; size of parks or reserves within radius etc.
</green_and_blue_spaces>
<biodiversity>
A metric derived from number of observed species in radius; number of categorized protected wildlife in radius etc.
</biodiversity>
<climate_resilience_and_adaptation>
A metric derived from temperature, rainfall, wind speed and sunlight statistics.
</climate_resilience_and_adaptation>
</connection_to_nature>
<a_sense_of_wonder>
<distinctive_design_and_culture>
A metric derived from number of indigenous sites in radius; number of historical cultural attractions in radius; number of recognized cultural exports.
</distinctive_design_and_culture>
<play_and_recreation>
A metric derived from recreational sites in number and size (e.g., designed capacity) in radius;
</play_and_recreation>
</a_sense_of_wonder>
<getting_around>
<walking_and_cycling>
A metric derived from dedicated / shared footpath, bike lanes in kilometers in radius.
</walking_and_cycling>
<public_transport>
A metric derived from public transport coverage in kilometers in radius; number of stops in radius; index for reach-ability to populous regions / centers.
</public_transport>
<car>
A metric derived from road traffic capacity index; average drive time per 10 kilometers; top peak traffic time and corresponding average speed.
</car>
</getting_around>
<connected_communities>
<belonging>
A metric derived from quantification of friendliness in neighborhood; tolerance and acceptance of immigrants; quantification of social media sentiment in local community.
</belonging>
<local_business_and_jobs>
A metric derived from number of local businesses in radius; number of distinct local businesses in radius; number of job postings in local region.
</local_business_and_jobs>
</connected_communities>
</quality_of_life_index>

"""
intro_to_housing_crisis = """Next, let me introduce you to some common sense regarding the situations in Ireland, using some example statistics. I\'ll first introduce the housing crisis in Ireland.

<housing_crisis>
The housing crisis in the Republic of Ireland is characterized by a severe shortage of affordable housing, rising homelessness, and skyrocketing rents. Several factors have contributed to this situation:

1.Supply Shortage: There has been a chronic under-supply of housing, particularly in urban areas like Dublin. This shortage is driven by slow construction rates, planning delays, and high building costs.
2.High Demand: Ireland's growing population, fueled by economic growth and immigration, has increased demand for housing. This demand has far outstripped the available supply, pushing prices up.
3.Rising Rents and Property Prices: Rent and property prices have soared, making it difficult for many people to afford a home. Dublin is particularly affected, with some of the highest rents in Europe.
4.Homelessness: The crisis has led to a significant rise in homelessness. Families, in particular, are increasingly finding themselves in emergency accommodation as they are unable to secure affordable housing.
5.Government Policies: Although the government has introduced measures such as rent controls and housing initiatives, these have often been criticized as insufficient. The reliance on the private market to provide affordable housing has also been a point of contention.
6.Social Housing Shortage: There has been a decline in the construction of social housing over the years, leading to long waiting lists and further pressure on the housing market.
7.Impact on Society: The crisis has broader social implications, including increased financial stress, overcrowded living conditions, and a growing divide between those who can afford housing and those who cannot.

Critically, Irish Capital City Dublin and the greater Dublin region possesses distinctive skewed representation of the problem when compared to the rest of the Nation. Published by Department of Housing, Local Government and Heritage, the following two figures presents the Housing statistics of recent years. Specifically, figure_1 presents the statistics for Dublin and figure_2 presents the rest of the nation."""

housing_crisis_statistic_figure_1 = Part.from_data(
    mime_type="image/png",
    data=base64.b64decode(
        """iVBORw0KGgoAAAANSUhEUgAAADwAAAA8CAYAAAA6/NlyAAAEw0lEQVRoQ+1Zf0hbVxT+osbZ6IwLKmVa/UNQwbFN1sLAMjdlc8NZMsGinRinIMNNhk5YWiYbKHNMFx3uj+LY1khXwQy1EelcSdMpkWK7UulKh5Ounf+IdaBVo9H82LsXkr00JnkveaYkeRfEl/vOOe/7zndz37knEkTZkEQZX4iEI11xUWFR4QjLgLikI0xQDzqiwqLCEZaB6FvSDofjSISJ6JOOhCHsiATCN65qcfRVFYZmjDgsfwYpiYlY2XiEt198yY2eG+GpqSmUlZWFJf/rxnM49lo9xW6z2xEbEwOi5U+madQeL3ZxihiFuapECUtOvM7VPii7C+2nceOvBcTGxuJQfDwu37qJ2a++Qaie79BfRnQq3N7eHpRyvb29QfmH0jk6FQ5lhp/0s0K6aT1pstG7aXnL/OLiIrKzs6HX61FYWIi0tDTIZDL6eWhoCGNjY7xE6+rqQn19PTIzM7G6ugqz2Yzu7m4MDAwgLi6OV6y6ujrqm5GRgeXlZdiZYkOhUCAhIQEajQZtbW37xuO0aanVago0Ly8P29vbaGxsxPDwMC+ATuOamhpkZWVhZmYGBQUF6OnpQUpKSkCx1tbWUF1dTZNPxCFvm9nZ2dDV0iNX7uBkSQFn8Npf5qF68wXO9kIYUoV1Oh0qKysDjvdwbQu6q3epf7PyKK2k/I1vx65Tk1T5IeZPhj//+Zd+/vCdY/Q/ue+89heLy31nPE5Lmh1wev4Bco8ocFjxtGvaCZ4N2BeIrZ09/Hjpll+cQhH+bf4+bt97SBPImTCblC+k3kBy9WfH5kKYHXfLbMEn7x6nq2O/4SJMlnRVVZXL5ruJm7BYbX4V8BbUOW9mlPyBg5LeHsQmHEjCHo/LS+GA2B+wE3kVWa1WxDMnLzJ2dnboa8nX4LykDxh7yMJzKi0/OlGJ2/fv4RFTKHTWvoe3Pj/NC2BTWTmULxeh7+LPKH7ueXx6/hzOnKzBFyPDkMsSYYcDp14pwR8P/obp7h2/sW0Xf4WBOUu/8Zkamsb30fb9WZz/WI3ar7+kvqeKS8CExIXpK26xxNLSb2ojwIDzd3hlZQXp6elBU97c3ERSUhKtpVNTU2mjTSIJrj0+NzeH/Px8JCcn+8XHmbDfSGFiIBjhYEtBO6N0DEtpZzzSPgq2BUW0CLi03E9Ib6Wl1WbHWf3vAWvPpdJyBj8zaMCzab6XtNfCg2tV8wFzUNDoruEp6f9nWTbIgyCsGbmGeKn/w4m3KtBtSXMl6kuygyIsFDbX8ZDU0kIFdSZESIWFwuaxaS0sLCA3N5di1mq1UKlUHoIODg6iqamJzk9OTqK8vBwTExNYWlpCc3Ozh/3o6KjHebuzsxMdHR3o7+9HRUUFcnJy0NfXh9bWVupPuhmPd0IMBgNKS0vp/fX1dcjlcrdn7e7uwmg00t/HxsfHoVQq6X3SQmppaaHXgu3SAe9MIXakhElm9vb2YLFYaCOMZI8UBFx6TcSXnFaI78bGBi0m2AqRHhg5wdhsNlejjlyTeVKAsIfJZEJRURGdIvdJr6qhoQFSqVSwtBDC0fWDuGCpC5NAwRWxYUKSDVMkHIai8YIsKswrXWFoLCochqLxgiwqzCtdYWgsKhyGovGCHHUK/we1hSoPks91MQAAAABJRU5ErkJggg=="""
    ),
)
housing_crisis_statistic_figure_2 = Part.from_data(
    mime_type="image/png",
    data=base64.b64decode(
        """iVBORw0KGgoAAAANSUhEUgAAADwAAAA8CAYAAAA6/NlyAAAFPklEQVRoQ+1ae0hbVxz+okaNSXxE0TrJughqh/OBOPCx0TLc/tBu6DLqUJlsdjofuH+UFRy1CQ4pOFDRbjpBRHTULsRKO3XaMdaJ4pxV2UsHa4ey4ZxadT7mK8s5kjRpXjeJBZPcA8GbnN/57u/7feee89175cDFGsfF+IIl7OyKswqzCjtZBdgp7WSCGtBhFWYVdrIKuN6UVqlULziZiGbpcNSEVc5AeGZMgdgkKS7f+Bx/PVzFhaRUfDf7C2RvvKlHT0s4NzcXe3t76OnpoZ/d3V3k5eWhpKQEDQ0N4HK56O7uRk5ODlZXVxEQEIDGxkaUl5efkHoR3Th497NrePvsS+geuYsY8dNIjTqD58SntTk6jcJMq04Jc157mWm8XXFxknBM3//dLgx7Bqv6huCaCutWbWdnB97e3vYU8kSPZRU+0fIcQ3J2LVp+PnysbW0apEEXhye8EPrzBXi4+a/REoiEvljZWDeel7MYD6bim72Gk5KSkJaWBjc3N8jlci1mRkYGNSK9vb1Mz6MXl5qaipGREe1v1dXVmJmZgVKpZIxXUVGBuro6vfi+vj7ExMRAIpGYxGG8aDU3N6O0tBRZWVmIjo5GTU0N4+R0AwcGBtDV1YXOzk7U19ejv78fg4ODNmGRQbW1tSguLqaY4+Pj6OjosOyl29vbkZ+fT5W0p30z9QfOxT+ycfZgPamxVOH5+XmEhYXZTLhRMa4ee3SnGSoSQHr2WVRWVkImkzHKu/XWlEFc4fl4+tvCwgIiIyMZ4ZgLUt79FVkvnnnktA4PDxkRvto9Aj7P0yS2hjCTDGs6v4W/gGcytCzreTDNy9L5rCbcpPzeEqaewuaCf36whK/vPbCIRwiba7ozi8TN/70GcbCf0SFhQUJDha/d/MFiEpYCNAoPDw/TFZ5poYzh6hK2B4dgGyVMfLS5pju9Dg4O4O7uDvJ3eXkZwcHB2N/fh4eHB3x8fLQwS0tLWFlZQVRUFLa2trR929vb4PF4WF9fh6+vL42fnZ2lceQ3oVAIDsfwCdTGxgbtI21xcZHet4vFYu33kJAQ7blJn6en/uXHeFuypKyj9DOylrHPhCM0QARl1RVkflSNr+6Zn/rGrOU/XQrw1Xdh7zXX45OS9xH6Vja1pTGnJej7UI7Xa2UYkl9FUJ7UYu22v7itjr+CxsJShJ96CsILr6K3SoZXLl9CgEAATw8ufmpuQ1CuPhZ7P2yxtE4QwOganpubo5t/VVUVAgMD6YM7sjjZ0sjCFBERQfd8qVQKhUJhCwwdQ2xlQUEB0tPTqQ/XLF7mABkRtjmjEzhQS/i4HE3brUlcPJ9AtyKRSGQT5Y97RuHF9YAl42EN+O3R35CRHGG9tTR1kk9vTmD/UAVvrjsl/Hj7oGUIfnwe1jZ34Mv3Vh97WczXFsKmDIrklL91hA8ODnGp9Q5NkufFhfydc9qEdU+iS5iYhLYvZywSMxVwMT1WazJIzP0/V9F950e14XGDwIyfN4ZnlvDG1n/oGLQt0ccVtscSHqe1NEr4OLy0hjB5bUOeipxYwpppoEmUfL9+/Tqys7NpV2trKwoLC+nx6OgokpOT6fHk5CQSEo6u2enpacTFxRnMKPIoKDMzk/aTRzBkS9J4aPJ+KiUlBYmJiRgbGwN5rGQKa2pqCvHxR/fJunlqtk2CPzExQbeqlpYWFBUV0dimpiaUlZXRY9fdlmxeWRxsIFHYtV6IO5hAdqfrev/jYXfJHAyAVdjBBLM6XVZhq0vmYANYhR1MMKvTZRW2umQONoBV2MEEszrd/wFI40NNNjr9cwAAAABJRU5ErkJggg=="""
    ),
)
geographic_overview = """The housing crisis in Ireland is a complex issue with no easy solutions, requiring sustained government intervention, policy reforms, and increased housing supply to address the underlying causes. 
</housing_crisis>

Next, let me introduce some geographical facts of Ireland.

<geographic_facts>
<geographic_overview>
Ireland is divided into several smaller geographic areas, including counties, electoral districts, and even townlands. Here are some geographical facts about Ireland at the electoral district level and similar granularity:

1.Electoral Divisions: Ireland is divided into approximately 3,440 electoral divisions (EDs), which are the smallest legally defined administrative areas. These divisions are used for various statistical purposes, such as the census.
2.Dublin Electoral Divisions: In Dublin, the electoral divisions can vary widely in population. For example, the Pembroke West division in Dublin 4 is one of the wealthiest areas in the country, while Ballymun D is known for having significant socio-economic challenges.
3.Gaeltacht Areas: Some electoral districts, particularly in counties like Donegal, Galway, and Kerry, are located in Gaeltacht areas where the Irish language is still widely spoken. An example is the An Cheathrú Rua (Carraroe) division in County Galway.
4.Rural vs. Urban Contrast: Electoral districts in rural areas, such as those in County Mayo or County Roscommon, are often much larger in land area but have much smaller populations compared to urban districts. For example, the ED of Ballaghaderreen in Roscommon is a large rural area with a sparse population.
5.Coastal Districts: Electoral divisions along the coast, such as in County Clare's Loop Head or parts of County Cork, often feature stunning landscapes, with a mix of cliffs, beaches, and small fishing villages. For instance, the Kilkee ED in Clare is known for its scenic coastal town.
6.High Population Density: Some EDs, particularly in Dublin and Cork, have very high population densities. Dublin's North Inner City division, for example, has a large number of people living in a relatively small area, with a mix of residential, commercial, and industrial zones.
7.Historical Divisions: Some electoral districts reflect historical boundaries that have been maintained over time. For instance, the ED of Shankill in South Dublin reflects the traditional boundaries of the village of Shankill and its surrounding areas.
8.Island Communities: There are electoral divisions that cover Ireland's offshore islands, such as the Aran Islands (Oileáin Árann) in County Galway. These districts are unique due to their isolation and small, close-knit populations.

These small-scale geographic divisions offer a detailed look at the diversity of Ireland's landscape, population distribution, and cultural heritage.
</geographic_overview>
<electoral_district>
Electoral districts (EDs) in Ireland are the smallest administrative units used for various purposes, including census data collection, electoral processes, and local governance. They play a crucial role in understanding demographic, social, and economic characteristics at a localized level.

Overview of Electoral Districts (EDs)

  - Number and Size: Ireland is divided into approximately 3,440 electoral districts. These vary significantly in size, population, and density. EDs can cover urban neighborhoods, rural areas, or even islands, and their boundaries often align with natural features, historical borders, or community limits.
  - Population: The population of electoral districts can range from just a few dozen people in remote rural areas to several thousand in urban centers. The total population of an ED is influenced by factors such as housing density, geographic area, and local amenities.
  - Area and Density:
  - Urban EDs: In cities like Dublin, Cork, and Limerick, EDs are smaller in area but have higher population densities. For example, Dublin's North Inner City ED covers a compact area but houses a large, diverse population.
  - Rural EDs: In contrast, rural EDs in counties like Mayo, Donegal, and Kerry can cover vast areas with low population densities. These EDs might encompass several townlands and villages, with populations spread out over wide areas.

Relevant Statistics

  - Population Distribution: According to the latest census data, about 63% of the population lives in urban areas, concentrated in urban EDs, while the remaining 37% resides in rural EDs. Urban EDs tend to have younger populations, more diverse communities, and higher employment rates.
  - Socio-Economic Variation: There is significant socio-economic variation between EDs:
  - Affluence: EDs like Blackrock in Dublin or Douglas in Cork have high average incomes, low unemployment rates, and high levels of educational attainment.
  - Deprivation: On the other hand, EDs such as Ballymun in Dublin or Knocknaheeny in Cork are among the most deprived, with higher levels of unemployment, lower incomes, and greater reliance on social services.
  - Language and Culture: Some EDs are located in Gaeltacht areas, where Irish is the predominant language. For example, the EDs in Connemara, County Galway, have a high percentage of Irish speakers, reflecting the area's cultural heritage.
  - Electoral Impact: EDs are also crucial for electoral representation. They are the building blocks for constituencies used in local and national elections. The boundaries of EDs can influence electoral outcomes, particularly in closely contested areas.
  - Dublin Example: Dublin city alone is divided into numerous EDs, each reflecting different aspects of the city's socio-economic fabric. The ED of Rathmines West, for instance, is known for its mix of residential and commercial zones, with a relatively high population density and a diverse population.

Importance in Planning and Policy

  - Census and Data Collection: Electoral districts are essential for collecting census data, which informs national and local policies, resource allocation, and planning decisions. Detailed statistics from EDs help identify areas in need of investment, such as education, healthcare, and infrastructure.
  - Electoral Representation: EDs play a key role in determining electoral constituencies for local, national, and European elections. Changes in population or boundaries can affect the number of representatives in a given area.
  - Urban vs. Rural Dynamics: The contrast between urban and rural EDs is a key factor in national debates on issues like housing, transportation, and public services. Urban EDs often face challenges related to congestion and housing shortages, while rural EDs might struggle with depopulation and access to services.
</electoral_district>
<electoral_district_population_table_snippet>"""
electoral_district_population_chart_1 = Part.from_data(
    mime_type="image/png",
    data=base64.b64decode(
        """iVBORw0KGgoAAAANSUhEUgAAADwAAAA8CAYAAAA6/NlyAAAC20lEQVRoQ+2YP2gaURzHv6dtVVJCEVwcih3E0SHFkE03xUimItJQtIIkQyilhEA7taJgcCgK0rqEghQcC4K1EFxcdCoFQXEROjRQRUmpNaFq8y7VtnjnH84U7+7d6u/3831/n+/v3XvHQGYPIzO9oIKlTpwSpoQl1gFqaYkBHZNDCVPCEusAtbTEgNJNi1qaWlpiHZCfpQeDwSOJQZwoh2m1WgM5CM5kMtjc3IRsBA+hMvV6fSrheDyOvb09wUbw+XxQKBQIBAJYX18XXG9YwGaz4eTkBKurqygWi//UzefzCIfDsFgsCIVCYC5meKrgha3sPxX6dsYt6WOpIC/BasXPS8EXtobBYODtPzEBGXqXy8XGHBwcIBKJzM2rWq2iUCjA7/fPncuXYLfbkUqlcH5+Dr1ez4Z9bvfHwl88e4LEy0OZEl5Yu5ekEN8MjyxdKpXYXWzSQ2y9u7uLcrmMYDAIq9U6tzyPx4N+v490Oj137qSE7e1txGIxaLVaNoxL8NvUGzx8cF+aln7+4YyzP09tCpkKrtVqMBqNvK45OjpiDwqVSgVbW1s4Pj7G/v4+stnsaGecxaPRaBROpxPtdhsbGxuzpMwUQ3ZoMnIqlYqN//SlN5b3/l0aj/33pEn463fug8etG7/fw9Pa2O12oVarp4XN9DshwTCLvZX2ej0olcrR/wsWPJOSJQpq/eAmfPPaBeFOpyO5s/Qpz1lau3L9coan2Yy8O3O5HBwOBxKJBMitR6PRzM2U1Ekmk9jZ2Zk7ly/B7XbD6/XCbDaPNtDTLjdDjXLGGV7Y6q6o0N8XPrI/tHksvUIsLfbrYbPZxOvkK6zdXYPJZILh9h1pCyamGRJuNBrQ6XSsj/hugISwvD7iXdFYLW3ZxZ4Allbmn4VRwSKAJGiJlLCg9okgmRIWASRBS6SEBbVPBMmUsAggCVoiJSyofSJIpoRFAEnQEilhQe0TQbLsCP8CYm8mf02Q6CcAAAAASUVORK5CYII="""
    ),
)
electoral_district_population_chart_2 = Part.from_data(
    mime_type="image/png",
    data=base64.b64decode(
        """iVBORw0KGgoAAAANSUhEUgAAADwAAAA8CAYAAAA6/NlyAAAEq0lEQVRoQ+1aW0hrRxRdMVeNRgyYilbBYq3BCz7gWl+oFLUKFyu0SCuKcFF8oGhprSIiQrQ/ih+C7wdIlYK0PxItftharVgQEato5HJVWj8s1hpJRVPfqTOaQxJzPedqKCcnZ36OntmzZ6+99kzm7D0SOFmTOBleiICFzrjIsMiwwDzgfCFtNBq7BUbivXAk14CNImABe4CVYclX/1D4Chnw48evEBMTg8nJSWRkZGB+fh4XFxfIzc3FyMgIkpKSsLGxgZCQECQnJ6O5uRl+fn5QqVS4vLxEW1sbtFotlEol1ZOTk4M/DKcI/mWVzrHkL8Xg4CBWVlYwPT2NzMxMjI+P07Hx8fFYXl6mcoeqHvr0flVGn+Hh4ejr66Nzp6en02dJSQn0ej329vYs6GMFfPL57b7moYCsRY+zszOcnJyArITZ2VlkZWVRg1xcXCCR3Mp+53IzSc4Vjo6O4OXlReXn5uawtLSE/Px8+Pj4MPINP6QxRr37dz4KCgro/7u7u3Ssh4cHpFIpffcidow+w54poXympcCOj48xPDyM0NBQuLm5YW1tDeXl5Tbj9I0BW2shYE3GMH1mgG3OavXSHLD6+aSl86xkzQFXd8TC1dWVSlxdXdFxbI0V8JPvj6kOxbVe3SdyZGdno6urC42NjejpuQmtw8NDKBQK7OzsICAggL4zfDOFf4d+pn/PfRGLqakpnJ+f07Ek/MrKyug7nU6HoaEhGn6VlZXY3NykckTfwsIC1tfXqU4yX1xc3A2eLz9kcPU//YxGWlVVFXp7e9Hf338vZpuADw4O0N3djbCwMKSmprI5jdf9ZOmYN1aGeY3mAcaJgB/gNIcaIjJM6CKbVnV1Nf1dq6urcygG2YzlxLAupZ7RoxiowJP33mbTy9t+EbAtakSGhRbSZNMiR0B/f38UFxczB3bCftO3H+AdlYK3a5TNME5r2HRgFwGzuZOH/XcYNhgM8PT0tDBV0AyTj2m5XO48gE9PT+Hu7o7CwkIKvKOjg0mpEC/INZ9C+vQtHgYrN5M4bVqmHJIgAW9tbdEknHkTNGCSpgkMDHQewLZWgqAZNgEmSTaScx4YGBA3rcfs0uYpWeLcrz+a4ra92kmK0y5tqj6QOX+r8oL2z0a8/OtXxoQ3MdohAat3f4dmT88ANj5/n7P/nQ4wU7q5dZGs/f8tXr42pEnNJjo6GqWlpbAO6ccwzFvA5jH6YMCmGpNJ2XVxTTiAzeo9FF/bT4AIWGQYvNm0SFTW1taipaWF26YllJAmHxPb29u0cl9RUYHW1lbU1NTc+d0lib/9/X2Mjo7C19cXwcHBSElJuSO3uLhIq/+dnZ1Qq9Xw9va2kKmvr6e14qCgICQkJCAxMZF+k6elpSEiIsJClthTVFSEqKgoWiEh1yzINYn7GqeTFudThQMIPgrwxMQEvYDyuvpTQ0MDVldX6bIgmZTIyEibLmlqaqIV/Ly8PIyN3dzhMG/kOgPRQyr9pkwM0UmWnHXTaDT0zsnMzAza29vv9D8KsAMQyh/AJDsqk8k4XUSxp2MJw8519dCe3nMEXc53m9YRWLGnjSLD9vQmH3WJDPORFXva5HQM/weTdrHZXvsTYgAAAABJRU5ErkJggg=="""
    ),
)
public_transport_csv_as_text = Part.from_data(
    mime_type="text/plain",
    data=base64.b64decode(
        """U2V0dGxlbWVudHMsUGVyY2VudGFnZUNlbnN1czIwMTZfUE9QVUxBVElPTl9QRVJfNTAwbV9QVUJMSUNUUkFOU1BPUlQsUGVyY2VudGFnZUNlbnN1czIwMTZfTUFMRV9QT1BVTEFUSU9OXzUwMG1fUFVCTElDVFJBTlNQT1JULFBlcmNlbnRhZ2VDZW5zdXMyMDE2X0ZFTUFMRV9QT1BVTEFUSU9OXzUwMG1fUFVCTElDVFJBTlNQT1JULFBlcmNlbnRhZ2VDZW5zdXMyMDE2X0RJU0FCTEVEX1BPUFVMQVRJT05fNTAwbV9QVUJMSUNUUkFOU1BPUlQsUGVyY2VudGFnZUNlbnN1czIwMTZfQV8wXzE0XzUwMG1fUFVCTElDVFJBTlNQT1JULFBlcmNlbnRhZ2VDZW5zdXMyMDE2X0FHRV8xNS02NF9QT1BVTEFUSU9OXzUwMG1fUFVCTElDVFJBTlNQT1JULFBlcmNlbnRhZ2VDZW5zdXMyMDE2X0FHRV9BQk9WRV82NV9QT1BVTEFUSU9OXzUwMG1fUFVCTElDVFJBTlNQT1JUDQpOYWFzLDE2LjMsMTYuNCwxNi4yLDIxLjUsMTIuNSwxNi4yLDI0LjINCkF0aGxvbmUsNjkuOCw2OS4zLDcwLjMsNzMuNSw2Ny40LDY5LjEsNzcNCkJhbGJyaWdnYW4sNzguNiw3OC43LDc4LjYsNzguMiw3OSw3OC4xLDgwLjQNCkJyYXksNjQuNyw2NC45LDY0LjUsNjMuOCw2NC40LDY0LjksNjQuOQ0KQ2FybG93LDUsNS4yLDQuOCw3LjksMi45LDUuMSwxMC4zDQpEcm9naGVkYSw1MSw1MS4yLDUwLjcsNjEuNCw0MS44LDUxLDcxLjINCk5ld2JyaWRnZSwxNi4yLDE2LjQsMTYuMSwyMC40LDExLjIsMTYuMiwyOC40DQpEdW5kYWxrLDQzLjQsNDMuNCw0My4zLDQ3LjUsNDAuOSw0My43LDQ0LjENCkVubmlzLDI4LjIsMjguMiwyOC4xLDM0LjgsMjEuNSwyNy4xLDQzLjgNCktpbGtlbm55LDcuNCw3LjcsNy4xLDguNCwzLjYsOCwxMC40DQpNdWxsaW5nYXIsMTQuNywxNS4zLDE0LjEsMTkuMiwxMC4yLDE0LjksMjMuNw0KTmF2YW4sMzkuNSwzOS40LDM5LjYsNDAuNCwzOC40LDM5LjMsNDIuOQ0KUG9ydGxhb2lzZSw1LjQsNS4zLDUuNSw3LjgsMy4zLDUuNCwxMi4yDQpUcmFsZWUsMTQsMTUuMSwxMywxNS43LDguNCwxNSwxNS41DQpXZXhmb3JkLDEyLjUsMTMsMTIsMTQuMiw4LjYsMTIsMTguMw0KV2F0ZXJmb3JkIGNpdHkgYW5kIHN1YnVyYnMsNjAuOSw2MS4zLDYwLjYsNzEuNSw1My4zLDYwLjQsNzMuOQ0KQ2VsYnJpZGdlLDQ2LjksNDcuMiw0Ni42LDU1LjIsNDEuOCw0Ny44LDU2LjYNCkdhbHdheSBjaXR5IGFuZCBzdWJ1cmJzLDY3LjIsNjcuNCw2Nyw3My40LDU3LjMsNjcuNSw4MS45DQpMaW1lcmljayBjaXR5IGFuZCBzdWJ1cmJzLDY4LjksNjksNjguNyw3Ny41LDYyLjcsNjguMiw3OS45DQpDb3JrIGNpdHkgYW5kIHN1YnVyYnMsNzYuMiw3Ni4zLDc2LjEsODEuMiw2OS44LDc2LjksODIuOQ0KU3dvcmRzLDY4LjcsNjksNjguNCw3MS42LDYzLjgsNjkuOCw3NC4yDQpEdWJsaW4gY2l0eSBhbmQgc3VidXJicyw3OC4xLDc4LjEsNzguMSw3OS44LDc0LjMsNzguOCw4MA=="""
    ),
)
task_instruction_prompt = """</public_transportation_statistics>


Finally, let me explain your task:
You are asked to generate synthetic QoL metrics based on given electoral district / settlement area or county, like \"Agha, Carlow\", \"Agha\" or \"Carlow\". 
I'll provide you with a list of (at most 10) electoral districts, and you'll generate a QoL metrics for each one. 
Your output should be in JSON format with the keys being the QoL metrics. 

Now here are my queries: <queries>{}</queries>"""
system_prompt = """You are an experienced data synthesizer, your job is to analyze descriptive and quantitative instructions and synthesize data based on user provided data format."""

output_json_schema = {
    "type": "ARRAY",
    "items": {
        "type": "OBJECT",
        "properties": {
            "query": {"type": "STRING"},
            "answer": {
                "type": "OBJECT",
                "properties": {
                    "a_sense_of_control": {
                        "type": "OBJECT",
                        "properties": {
                            "cost_of_living": {"type": "INTEGER"},
                            "safety": {"type": "INTEGER"},
                            "influence_and_contribution": {"type": "INTEGER"},
                            "essential_services": {"type": "INTEGER"},
                        },
                        "required": [
                            "cost_of_living",
                            "safety",
                            "influence_and_contribution",
                            "essential_services",
                        ],
                    },
                    "health_equity": {
                        "type": "OBJECT",
                        "properties": {
                            "housing_standard": {"type": "INTEGER"},
                            "air_noise_light": {"type": "INTEGER"},
                            "food_choice": {"type": "INTEGER"},
                        },
                        "required": [
                            "housing_standard",
                            "air_noise_light",
                            "food_choice",
                        ],
                    },
                    "connection_to_nature": {
                        "type": "OBJECT",
                        "properties": {
                            "green_and_blue_spaces": {"type": "INTEGER"},
                            "biodiversity": {"type": "INTEGER"},
                            "climate_resilience_and_adaptation": {"type": "INTEGER"},
                        },
                        "required": [
                            "green_and_blue_spaces",
                            "biodiversity",
                            "climate_resilience_and_adaptation",
                        ],
                    },
                    "a_sense_of_wonder": {
                        "type": "OBJECT",
                        "properties": {
                            "distinctive_design_and_culture": {"type": "INTEGER"},
                            "play_and_recreation": {"type": "INTEGER"},
                        },
                        "required": [
                            "distinctive_design_and_culture",
                            "play_and_recreation",
                        ],
                    },
                    "getting_around": {
                        "type": "OBJECT",
                        "properties": {
                            "walking_and_cycling": {"type": "INTEGER"},
                            "public_transport": {"type": "INTEGER"},
                            "car": {"type": "INTEGER"},
                        },
                        "required": ["walking_and_cycling", "public_transport", "car"],
                    },
                    "connected_communities": {
                        "type": "OBJECT",
                        "properties": {
                            "belonging": {"type": "INTEGER"},
                            "local_business_and_jobs": {"type": "INTEGER"},
                        },
                        "required": ["belonging", "local_business_and_jobs"],
                    },
                    "QoL": {"type": "INTEGER"},
                },
                "required": [
                    "a_sense_of_control",
                    "health_equity",
                    "connection_to_nature",
                    "a_sense_of_wonder",
                    "getting_around",
                    "connected_communities",
                    "QoL",
                ],
            },
        },
        "required": ["query", "answer"],
    },
}

generation_config = GenerationConfig(
    max_output_tokens=8192,
    temperature=0.1,
    top_p=0.95,
    response_mime_type="application/json",
    response_schema=output_json_schema,
)


safety_settings = [
    # I think these are stupid, it rewrites Swineford to Swinford
    
    # SafetySetting(
    #     category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
    #     threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    # ),
    # SafetySetting(
    #     category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    #     threshold=SafetySetting.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    # ),
    # SafetySetting(
    #     category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
    #     threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    # ),
    # SafetySetting(
    #     category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
    #     threshold=SafetySetting.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    # ),
]


fire.Fire(main)
