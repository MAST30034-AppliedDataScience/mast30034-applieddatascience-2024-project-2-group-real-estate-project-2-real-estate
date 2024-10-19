## Generic Real Estate Consulting Project
Data can be downloaded via URL or uploaded directly to the `raw` directory.

-**Group member:** Xiaowei Guo(1346452), Zixuan Zhang(1132592), Hanyang Shi(1346903), Hao Tian(1342982), Luochan Bao(1131378)

-**Research objective:** Predict property rents for the next three years and to identify the fatures of property rents. Recommendations are made based on the predict and analysis.

-**Timeline:** The timeline for the research area is 2023.

-**API Access:** (1).Declaration : The API keys are securely stored in environment variables and have been excluded from version control by including them in the .gitignore file. (2). Guidance about how to get API access is provided in "distance_train_station.ipynb" in "notebook" folder.


Step 1 : To find the relevant analysis (EDA) and get the dataset for prediction model, please visit the "notebook" folder and run the files in order:
1. **population_EDA.ipynb**：Perform exploratory data analysis of demographic data.
2. **EDA_aff.ipynb**: Exploratory data analysis of economic prosperity data.
3. **avg_rent.ipynb**：Analyzing and calculating the average rent price in each area.
4. **code_sa2postcode.ipynb**：Conversion of SA2 area codes to zip codes for finer geographic analysis.
5. **code_top10_new.ipynb**：Generate a visualization of the top ten SUBURBS with the largest GROWTH RATE and make projections for the next three years.
6. **distance_facilities.ipynb**：Calculate the distance of each property from surrounding amenities (e.g. schools, stores, etc.) to assess location convenience.
7. **distance_train_station.ipynb**：The distance from the property to the nearest train station is calculated for analyzing accessibility.
8. **Feature_interested.ipynb**：Select features useful for analysis and perform feature engineering to optimize model performance.
9. **map_growrate.ipynb**：Generate map visualizations based on growth rates in different regions.
10. **map_top10.ipynb**：Generate a geographic visualization of the top10 suburbs with the highest predicted growth rates.
11. **radar_code.ipynb**：Several influences on most livable affordable are visualized as radar charts.

Step 2 : To run the model, please visit the "Model" folder and run the juypter notebooks:
1. **code_predict.ipynb**：Analyze the importance of features using regression models, do model evaluation.
2. **growth rate and price.ipynb**：Analyze and visualize the relationship between growth rates and rent prices in different regions. Use random forest model and gradient boost model to predict the top ten highest rent suburb.

Please See the `scrape.py` file in the `scripts` directory to get started scraping data. 
