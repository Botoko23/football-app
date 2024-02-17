from flask import Flask, request, jsonify
from flask_cors import CORS

import concurrent.futures

from tools.scraper import Scraper
from constants import comp_code_dict
from assemble import calculate_points

app = Flask(__name__)
CORS(app)


@app.route('/chart', methods=['GET'])
def get_chart_data():

    season = request.args.get('season')
    league = request.args.get('league')
    comp_code = comp_code_dict[league]
    data = {}
    
    scraper = Scraper(comp_code, league, season)
    club_names = scraper.get_fixtures()

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        results = executor.map(calculate_points, club_names)

        for club, pts in results:
            data.update({club:pts})
  
    return jsonify(data)

if __name__=="__main__":
    app.run(debug=True, port=5000, threaded=True)
   

  
   


