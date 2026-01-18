from flask import Flask, send_file, jsonify, render_template, request
from fetch_data import fetch_weather_data
from config import CSV_FILE,EXCEL_FILE,XML_FILE
from process_data import process_weather_data
from convert_data import convert_to_csv, convert_to_excel, convert_to_xml
from datetime import datetime

app=Flask(__name__)

# Popular cities list
POPULAR_CITIES = {
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Miami', 'Seattle', 'Boston'],
    'UK': ['London', 'Manchester', 'Birmingham', 'Liverpool', 'Leeds', 'Bristol', 'Edinburgh', 'Glasgow'],
    'India': ['Delhi', 'Mumbai', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad'],
    'Japan': ['Tokyo', 'Osaka', 'Kyoto', 'Yokohama', 'Nagoya', 'Sapporo', 'Fukuoka', 'Kobe'],
    'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Canberra', 'Hobart'],
    'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa', 'Winnipeg', 'Edmonton', 'Quebec City'],
    'Germany': ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt', 'Dusseldorf', 'Stuttgart', 'Dortmund'],
    'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Bordeaux']
}

@app.route('/')
def home():
    return render_template('index.html', countries=POPULAR_CITIES)

@app.route('/api/cities/<country>')
def get_cities(country):
    """Get cities for a specific country"""
    cities = POPULAR_CITIES.get(country, [])
    return jsonify({'cities': cities})

@app.route('/search', methods=['POST', 'GET'])
def search():
    city = request.form.get('city', request.args.get('city', '')).strip()
    country = request.form.get('country', request.args.get('country', ''))
    selected_city = request.form.get('selected_city', request.args.get('selected_city', ''))
    
    # Use selected city if available, otherwise use custom city input
    search_city = selected_city if selected_city else city
    
    if not search_city:
        return render_template('index.html', countries=POPULAR_CITIES, error='Please enter or select a city name', 
                             selected_country=country, searched_city=city)
    
    # Fetch and process weather data for the city
    weather_data = fetch_weather_data(search_city)
    processed_data = process_weather_data(weather_data)
    
    if isinstance(processed_data, dict) and 'error' in processed_data:
        return render_template('index.html', countries=POPULAR_CITIES, 
                             error=f"City not found: {search_city}", 
                             selected_country=country, 
                             searched_city=city)
    
    # Add search info to the result
    processed_data['searched_city'] = search_city
    processed_data['selected_country'] = country
    
    return render_template('index.html', countries=POPULAR_CITIES, data=processed_data, 
                         selected_country=country, searched_city=search_city)

@app.route('/get_weather_data',methods=['GET'])
def get_weather_data():
    #fetch the raw weather data from open weather api
    raw_data=fetch_weather_data()
    #proceess data to clean version
    processed_data=process_weather_data(raw_data)
    if 'error' in processed_data:
        return jsonify(processed_data),400
    #save the data in csv , excel and xml
    csv_file=convert_to_csv(processed_data)
    excel_data=convert_to_excel(processed_data)
    xml_data=convert_to_xml(processed_data)

    return jsonify({
        'message':'weather data fetched and processed successfully',
        'csv_file':csv_file,
        'Excel_file':excel_data,
        'xml_file':xml_data
    })

@app.route('/download_csv',methods=['GET'])
def download_csv():
    return send_file(CSV_FILE, as_attachment=True)

@app.route('/download_excel',methods=['GET'])
def download_excel():
    return send_file(EXCEL_FILE, as_attachment=True)

@app.route('/download_xml',methods=['GET'])
def download_xml():
    return send_file(XML_FILE, as_attachment=True)

if __name__=="__main__":
    app.run(debug=True)