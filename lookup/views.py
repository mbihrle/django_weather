from django.shortcuts import render
import configparser

# Create your views here.
config = configparser.ConfigParser()
config.read('../../../_configs/config.ini')
API_KEY = config['airnowapi.org']['API_KEY']


def home(request):
    import json
    import requests

    if request.method == "POST":
        zipcode = request.POST['zipcode']
        # 89129

        request_string = "https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" + \
            zipcode+"&distance=5&API_KEY=" + API_KEY

        api_request = requests.get(request_string)

        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = "Error"

        if api[0]['Category']['Name'] == "Good":
            category_description = "(0 to 50): Air quality is satisfactory, and air pollution poses little or no risk."
            category_color = "good"
        elif api[0]['Category']['Name'] == "Moderate":
            category_description = "(51 to 100): Air quality is acceptable. However, there may be a risk for some people, particularly those who are unusually sensitive to air pollution."
            category_color = "moderate"
        elif api[0]['Category']['Name'] == "Unhealty for Sensitive Groups":
            category_description = "(101 to 150): Members of sensitive groups may experience health effects. The general public is less likely to be affected."
            category_color = "usg"
        elif api[0]['Category']['Name'] == "Unhealthy":
            category_description = "(151 to 200): Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects."
            category_color = "unhealthy"
        elif api[0]['Category']['Name'] == "Very Unhealthy":
            category_description = "(201 to 300): Health alert: The risk of health effects is increased for everyone."
            category_color = "veryunhealthy"
        elif api[0]['Category']['Name'] == "Hazardous":
            category_description = "(301 and higher): Health warning of emergency conditions: everyone is more likely to be affected."
            category_color = "hazardous"
        else:
            category_description = "Category Could Not Be Found"
            category_color = "unknown"

        return render(request, 'home.html', {'api': api, 'category_description': category_description, 'category_color': category_color})
    else:
        return render(request, 'home.html', {})


def about(request):
    return render(request, 'about.html', {})
