from tools.stats_extractor import StatsExtractor
from constants import points_decimal, goal_decimal, PGD_decimal, NGD_decimal

import numpy as np
import boto3


# Create an S3 client
s3 = boto3.client('s3')


def accumulate_stats(points:list, goal_difference:list, goals:list) -> list:
    # accumulate points, goal difference, and goals scored over matches
    points_array =  (lambda x: x+points_decimal)(np.cumsum(points))
    gd_array = np.cumsum(goal_difference)
    goals_array = (lambda x: x*goal_decimal)(np.cumsum(goals))

    # create list of points earned over matches with gd and goals scored in the decimal
    points_gd_goals = []
    for points, gd, goals in zip(points_array, gd_array, goals_array):
        if gd >= 0:
            points_gd_goals.append(round(points + gd * PGD_decimal + goals, 10))
        else:
            points_gd_goals.append(round(points + gd * NGD_decimal + goals, 10))

    return points_gd_goals


def calculate_stats(club : list[str]) -> list[float]:
    stats_getter = StatsExtractor(club)
    stats_getter.prepare_df()
    gd, pts = stats_getter.calculate_gd_and_points()
    goals = stats_getter.get_all_goals()
    pts_gd_goals = accumulate_stats(pts, gd, goals)
    return club, pts_gd_goals 



if __name__=="__main__":
    pass
    
    # scraper = Scraper("9", "Premier-League", "2022-2023")
    # club_names, dates = scraper.get_fixtures()
    # clubs = []
    # pts = []
    # data = {}

    # with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    #     results = executor.map(calculate_points, club_names)

    #     for club, point in results:
    #         clubs.append(club)
    #         pts.append(point)

    
    # print(clubs)
    # print(len(pts))
    # print(len(pts[0]))
    # json_string = json.dumps(data, indent=2)  
    # with open('output.json', 'w') as json_file:
    #     json_file.write(json_string)

    # df = pd.DataFrame({'Club': clubs, 'Points': pts})
    # reshaped = df.T.reshape((20, 2))

    # new_column_names = {}
    # df.rename(columns=new_column_names, inplace=True)
    # print(reshaped)
    # raceplot = barplot(df,  item_column='Country Name', value_column='GDP', time_column='Year')

    # raceplot.plot(item_label = 'Racing bar chart', value_label = 'GDP ($)', frame_duration = 800)
   

  
   


