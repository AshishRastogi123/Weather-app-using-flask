from flask import Flask, send_file, jsonify
from fetch_data import fetch_weather_data
from config import CSV_FILE,EXCEL_FILE,XML_FILE
from process_data import process_weather_data
from convert_data import convert_to_csv, convert_to_excel, convert_to_xml

app=Flask(__name__)

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