from flask import Flask, request, render_template_string, session, redirect, url_for
import requests
import html
import re

app = Flask(__name__)



HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>TV Show Explorer</title>
    <style>
    .show-block {
    flex-direction: row-reverse;
    }
        body {
            background-color: grey;
            }


    img.featured-image {
            display: block;
            width: 25%;
            margin: 20px auto;
            border-radius: 1000px;
        }

    h1 {text-align: center;}
    form {text-align: center;}
    <script>
        window.onload = function() {};
    </script>
    </style>

{% if results %}
    <form action = "http://localhost:5000/iloveDNE" method = "get">
        <p><input type = "submit" value = "Return Home" /></p>
        </form>

{% elif found == True %}
    <form action = "http://localhost:5000/iloveDNE" method = "get">
        <p><input type = "submit" value = "Return Home" /></p>
        </form>
{% endif %}

<img class="featured-image" src='https://media.gq.com/photos/5df5a3794e7a380009b83bbd/16:9/w_2560%2Cc_limit/BestShows.jpg'>
<title>TV Show Explorer</title>

</head>

<body>
    <h1>Search for a TV Show</h1>
    <form method="get">
    <input name="query" placeholder="Search..." value="{{ query }}" autocomplete="off">
        <button type="submit">Search</button>
    </form>

    {% if results %}
        <h2>Results:</h2>
        {% for show in results %}
            <div class="show-block">
                <div class="show-info">
                    <strong>{{ show['name'] }}</strong><br>
                    Genres: {{ show['genres'] }}<br>
                    Rating: {{ show['rating'] or 'N/A' }}<br>
                    Summary: {{ show['summary'] }}<br>

                    {% if show['officialSite'] %}
                        officialSite: <a href="{{ show['officialSite'] }}">{{ show['officialSite'] }}</a><br><br>
                    {% else %}
                        officialSite: Not available<br><br><br>
                    {% endif %}
                </div>
            
            {% if show['image'] %}
                <img class="show-image" src="{{ show['image'] }}" alt="Show Image">
            {% endif %}
        </div>
            
        {% endfor %}
    {% elif found == True %}
    <p>No results found. Try a different search!</p> 
    {% endif %}
    
</body>
</html>
"""

def reset():
    return redirect(url_for("index"))
    
def strip_tags(text):
    if text:
        return html.unescape(re.sub('<[^<]+?>', '', text))
    else:
        return "No summary available."

@app.route("/iloveDNE", methods=["GET"])
def index():
    query = request.args.get("query","")
    results = []
    found = False
    if query:
        url = f"http://api.tvmaze.com/search/shows?q={query}"
        response = requests.get(url)
        data = response.json()
        found = True

        for item in data[:5]:  # Limiting the number of results
            show = item['show']
            rating = show.get('rating', {}).get('average')
            image = show.get('image')
            if rating and rating > 3:
                results.append({
                    'name': show['name'],
                    'genres': ', '.join(show['genres']),
                    'rating': rating,
                    'summary': strip_tags(show.get('summary', '')),
                    'officialSite': show['officialSite'],
                    'image': image['medium'] if image else None
                })



    
    print(results)
    return render_template_string(HTML_TEMPLATE, results=results, found=found)

if __name__ == '__main__':
    app.run(debug=True)
