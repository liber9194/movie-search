import random
import requests
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def home():
    name = '김땡땡'
    lotto =  [16, 18, 22, 43, 32, 11]

    def generate_lotto_numbers():
        numbers = random.sample(range(1,46),6)
        return sorted(numbers)
    random_lotto = generate_lotto_numbers()

    # 두 개의 리스트 생성
    list1 = [1, 2, 2, 3, 4, 5]
    list2 = [2, 2, 3, 4, 4, 5]

    # 두 리스트에서 공통으로 나타나는 요소를 저장할 리스트 생성
    common_elements = []

    # list1의 요소를 순회하면서 list2에도 있는지 확인
    for item in lotto:
        if item in random_lotto:
            common_elements.append(item)

    # 공통 요소 출력
    print("공통 요소:", common_elements)
    print("공통 요소 개수:", len(common_elements))

    context = {
        "name" : name,
        "lotto" : lotto,
        "random_lotto": random_lotto,
        "common_count" : len(common_elements),
    }

    return render_template('index.html', data = context)

@app.route('/mypage')
def mypage():
    return 'This is Mypage!'

@app.route('/movie')
def movie():
    query = request.args.get('query')
    res = requests.get(
	f"http://kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json?key=f5eef3421c602c6cb7ea224104795888&movieNm={query}"
    )
    rjson = res.json()

    movie_list = rjson["movieListResult"]["movieList"]
    print(movie_list)
    return render_template('movie.html', data = movie_list)

@app.route("/answer")
def answer():

    if request.args.get('query'):
        query = request.args.get('query')
    else:
        query = '20230601'    

    URL = f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?key=f5eef3421c602c6cb7ea224104795888&targetDt={query}"

    res = requests.get(URL)

    rjson = res.json()
    movie_list = rjson.get("boxOfficeResult").get("weeklyBoxOfficeList")

    return render_template("answer.html", data=movie_list)

if __name__ == '__main__':  
    app.run(debug=True)