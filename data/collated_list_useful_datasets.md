# A list of accessible datasets for future use

(
At the bare minimum, groups should aim to find the proximity to the closest train station or Melbourne CBD.
Proximity/Distance should be calculated via routes (as travelled by car).
This can be done by leveraging an API such as Open Route Service.
One example is Open Route Service, examples have been provided at the end of this document.
)

Time dependent:

    - Interest rates
        - Housing Lending Rates
            - Timeline: 31/07/2019 to 30/06/2024 (Monthly)
            - URL: https://www.rba.gov.au/statistics/tables/xls/f06hist.xlsx (XLSX)
                   https://www.rba.gov.au/statistics/tables/csv/f6-data.csv (CSV)
        - Advertised Deposit Rates
            - Timeline: Jun-2022 to Jul-2024 (Monthly)
            - URL: https://www.rba.gov.au/statistics/tables/xls/f04hist.xlsx (XLSX)
        - Paid Deposit Rates
            - Timeline: Jul-2019 to Jun-2024 (Monthly)
            - URL: https://www.rba.gov.au/statistics/tables/xls/f04-1-hist.xlsx (XLSX)
                   https://www.rba.gov.au/statistics/tables/csv/f4.1-data.csv (CSV)

    - GDP growth
        - Gross domestic product, chain volume measures, seasonally adjusted
            - Timeline: Jun-16 to Jun-24 (Quarterly)
            - URL: https://www.abs.gov.au/statistics/economy/national-accounts/australian-national-accounts-national-income-expenditure-and-product/latest-release#expenditure
        - Annual growth in gross domestic product, chain volume measures, original
            - Timeline: 1989-90 to 2023-24
            - URL: https://www.abs.gov.au/statistics/economy/national-accounts/australian-national-accounts-national-income-expenditure-and-product/latest-release#expenditure

    - Immigration numbers
        - Net overseas migration by country of birth, state/territory
            - Timeline: 2004-05 to 2022-23
            - URL: https://www.abs.gov.au/statistics/people/population/overseas-migration/2022-23-financial-year/34070DO001_202223.xlsx (XLSX)

    - Age demographics
        - Population estimates by age and sex, by SA2
            - Timeline: 2001 to 2023
            - URL: https://www.abs.gov.au/statistics/people/population/regional-population-age-and-sex/2023/32350DS0005_2001-23.xlsx (XLSX)
        - Population estimates by age and sex, by SA2, GDA2020
            - Timeline: 2023
            - URL: https://www.abs.gov.au/statistics/people/population/regional-population-age-and-sex/2023/32350_ERP_Age_Sex_SA2_GDA2020_2023_gpkg.zip (GeoPackages.zip)
        - Population estimates by age and sex, by SA2, GDA94
            - Timeline: 2023
            - URL: https://www.abs.gov.au/statistics/people/population/regional-population-age-and-sex/2023/32350_ERP_Age_Sex_SA2_GDA94_2023_gpkg.zip (GeoPackages.zip)
        - Population projections (based on assumptions of fertility, mortality and migration) for Victoria
            - Timeline: 2022 (base) to 2071
            - URL: https://www.abs.gov.au/statistics/people/population/population-projections-australia/latest-release#victoria

Location dependent:

    - Socio economic (income)
        - Total income, earners and summary statistics by geography
            - Timeline: 2016-17 to 2020-21
            - URL: https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2020-21-financial-year/Table%201%20-%20Total%20income%2C%20earners%20and%20summary%20statistics%20by%20geography%2C%202016-17%20to%202020-21.xlsx (XLSX)
        - Total income distribution by geography
            - Timeline: 2020-21
            - URL: https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2020-21-financial-year/Table%202%20-%20Total%20income%20distribution%20by%20geography%2C%202020-21.xlsx (XLSX)
        - Employee income, earners and summary statistics by geography
            - Timeline: 2016-17 to 2020-21
            - URL: https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2020-21-financial-year/Table%203%20-%20Employee%20income%2C%20earners%20and%20summary%20statistics%20by%20geography%2C%202016-17%20to%202020-21.xlsx (XLSX)
        - Investment income, earners and summary statistics by geography
            - Timeline: 2016-17 to 2020-21
            - URL: https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2020-21-financial-year/Table%205%20-%20Investment%20income%2C%20earners%20and%20summary%20statistics%20by%20geography%2C%202016-17%20to%202020-21.xlsx (XLSX)
        - Own unincorporated business income, earners and summary statistics by geography
            - Timeline: 2016-17 to 2020-21
            - URL: https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/personal-income-australia/2020-21-financial-year/Table%206%20-%20Own%20unincorporated%20business%20income%2C%20earners%20and%20summary%20statistics%20by%20geography%2C%202016-17%20to%202020-21.xlsx (XLSX)

    - Schools (quality of schools, e.g. look into school zones)
        - Number of Schools by Region, Sector, School Size and School Type
            - Timeline: 2015 to 2024
            - URL: https://www.education.vic.gov.au/Documents/about/department/schoolsandenrolments.xlsx (XLSX)



    - Nearby shopping centres, nightclubs, universities, health facilities, industrial factories and parks
        - Up to date
        - URL: https://www.openstreetmap.org/export (or via API)

    - PTV Metro Train Stations
        - Up to date
        - URL: https://discover.data.vic.gov.au/dataset/ptv-metro-train-stations/resource/e9aa79ac-a619-4943-bca1-34ff25cf4812 (SHP)

    - PTV Regional Train Stations
        - Up to date
        - URL: https://discover.data.vic.gov.au/dataset/ptv-regional-train-stations/resource/25787f0f-c598-4d65-9f97-4f578562d7f5 (SHP)

    - ABS maps (ASGS Edition 3)
        - URL: https://maps.abs.gov.au/

    - Allocation file by Main Structure and Greater Capital City Statistical Areas, SA2 (ASGS Edition 3)
        - Reference Date: 2021
        - URL: https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/allocation-files/SA2_2021_AUST.xlsx (XLSX)

    - Digital boundary file by Main Structure and Greater Capital City Statistical Areas, SA2, GDA2020 (ASGS Edition 3)
        - Reference Date: 2021
        - URL: https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA2_2021_AUST_SHP_GDA2020.zip (SHP)

    - Digital boundary file by Main Structure and Greater Capital City Statistical Areas, SA2, GDA96 (ASGS Edition 3)
        - Reference Date: 2021
        - URL: https://www.abs.gov.au/statistics/standards/australian-statistical-geography-standard-asgs-edition-3/jul2021-jun2026/access-and-downloads/digital-boundary-files/SA2_2021_AUST_SHP_GDA94.zip (SHP)

    - Data services and APIs by Main Structure and Greater Capital City Statistical Areas, SA2 (ASGS Edition 3)
        - Reference Date: 2021
        - URL: https://geo.abs.gov.au/arcgis/rest/services/ASGS2021/SA2/MapServer