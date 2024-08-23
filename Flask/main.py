from flask import Flask, jsonify, request
from marshmallow import Schema, fields, ValidationError
from datetime import datetime
# Crea una instancia de la aplicación Flask
app = Flask(__name__)

# Define el esquema de validación con marshmallow
class UserSchema(Schema):
    name = fields.Str(required=True)
    lastName = fields.Str(required=True)
    age = fields.Int(required=True)
    maritalStatus = fields.Str(required=True)
    birthdate = fields.Str(required=True)

# Crea una instancia del esquema
user_schema = UserSchema()

# Define una ruta para el método GET
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({"message": "Hello, World!"})

# Define una ruta para el método POST
@app.route('/api/data', methods=['POST'])
def post_data():
     # Obtiene los datos JSON de la solicitud
    data = request.get_json()

    # Validar los datos recibidos usando el esquema
    try:
        # Deserializa y valida los datos
        validated_data = user_schema.load(data)
    except ValidationError as err:
        # En caso de error de validación, devuelve el error
        return jsonify({"errors": err.messages}), 400

    # Accede a propiedades individuales del diccionario validado
    name = validated_data['name']
    lastName = validated_data['lastName']
    age = validated_data['age']
    maritalStatus = validated_data['maritalStatus']
    birthdate = validated_data['birthdate']


     # Verifica que la fecha de nacimiento esté en el formato correcto
    try:
        date_of_birth = datetime.strptime(birthdate, '%Y/%m/%d')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY/MM/DD."}), 400


    # Extrae el año de la fecha de nacimiento
    year = date_of_birth.year

    # Verifica si el año es bisiesto
    is_leap = is_leap_year(year)
    # Puedes realizar operaciones con los datos recibidos
    response_message = {
        "status": is_leap,
    }

    # Responde con los datos recibidos y procesados
    return jsonify(response_message), 201

def is_leap_year(year):
    
    #Devuelve True si el año es bisiesto, de lo contrario False.
    if (year % 4 == 0):
        if (year % 100 == 0):
            if (year % 400 == 0):
                return True
            return False
        return True
    return False
# Ejecuta la aplicación
if __name__ == '__main__':
    app.run(debug=True)
