from flask import Flask, jsonify, request, Response
from datetime import datetime
import dicttoxml

app = Flask(__name__)

@app.route('/api/age', methods=['POST'])
def hello():
    data = request.get_json() or {}
    flag = False
    age = ""
    print(data)
    try:
        if 'name' not in data:
            data['name'] = ''
        if 'lastName' not in data:
            data['lastName'] = ''
        #if 'age' not in data:
        #    data['age'] = ''
        if 'maritalStatus' not in data:
            data['maritalStatus'] = '' 
        if 'birthdate' not in data:
            data['birthdate'] = ''
        if 'secondName' in data:
            valor = data['secondName']
        if valor is None:
            data['secondName'] = ''
        print(data)
        if data['birthdate']  is not None:
            flag = validDate(data['birthdate'])
        if flag:
            #print("sigue")
            date_of_birth = datetime.strptime(data['birthdate'], '%Y/%m/%d')
            year = date_of_birth.year
            age = ageByYear(year)
            print(age)
        else: 
            age = "Invalid Date" 
            print(age)
        response_message = {
        "age": age,
        "birthdate":data['birthdate']
            }
        #return jsonify(data)
        print(data)
        return jsonify(response_message),201
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY/MM/DD."}), 400


def validDate(dateStr):
    try:
        dateStr = datetime.strptime(dateStr, "%Y/%m/%d")
        if dateStr > datetime.now():
            return False
        return True
    except ValueError:
        return False
    
def ageByYear(year):
    today = datetime.now()
    age = today.year - year
    return age

@app.route('/api/bisiesto', methods=['POST'])
def post_data():
    flag = False
    data = request.get_json()

    if 'age' not in data:
            data['age'] = ''
    if 'birthdate' not in data:
            data['birthdate'] = ''

    age = data['age']
    birthdate = data['birthdate']
    response_message = ""

    if data['birthdate']!="":
        flag = validDate(data['birthdate'])

    if flag:
        try:
            date_of_birth = datetime.strptime(birthdate, '%Y/%m/%d')
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY/MM/DD."}), 400

        year = date_of_birth.year

        is_leap = is_leap_year(year)
        response_message = {
        "status": is_leap,
        "age":age
        }
        print(response_message)
    else:
         return jsonify({"error": "Incorrect Date"}), 400
    return jsonify(response_message), 201

def is_leap_year(year):
    
    if (year % 4 == 0):
        if (year % 100 == 0):
            if (year % 400 == 0):
                return True
            return False
        return True
    return False

@app.route('/api/message', methods=['POST'])
def message():
    data = request.get_json()
    print(data)

    if 'age' not in data:
            data['age'] = 0
    if 'status' not in data:
            data['status'] = False

    age = data['age']
    status = data['status']
    message = ""
    #status = data['status']

    if(age <26):
        message = "Eres menor a la edad de Andres"
    elif(age == 26):
        message = "tienes la misma edad de Andres"
    else:
        message = "Eres mayor a la edad de Andres"


    response_message = {
        "message": message,
        "age":age,
        "bisiesto":status
    }

    xml_data = dicttoxml.dicttoxml(response_message)
    
    response = Response(xml_data, mimetype='application/xml')
    return response, 201

if __name__ == '__main__':
    app.run(debug=True)
