import os
import firebase_admin
import json
from flask import Flask ,request, jsonify
from firebase_admin import credentials, firestore, initialize_app


app = Flask(__name__)

cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref_flight = db.collection('flight')
todo_ref_price = db.collection('price')
todo_ref_seat = db.collection('seat_availability')
todo_ref_book = db.collection('booking')


@app.route('/addFlight', methods=['POST'])
def create_flight():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        todo_ref_flight.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/listFlight', methods=['GET'])
def read_flight():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        cityFrom = request.args.get('from')
        cityTo = request.args.get('to')
        if cityFrom and cityTo:
            print(123)
            todo = [doc.to_dict() for doc in todo_ref_flight.where(u'start',u'==',cityFrom).where(u'end',u'==',cityTo).stream()]
            return jsonify(todo), 200
        else:
            all_todos = [(doc.get('id'),doc.get('start'),doc.get('end')) for doc in todo_ref_flight.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/updateFlight', methods=['POST', 'PUT'])
def update_flight():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref_flight.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/deleteFlight', methods=['GET', 'DELETE'])
def delete_flight():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref_flight.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"


####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################



@app.route('/addPrice', methods=['POST'])
def create_price():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        id = request.json['id']
        todo_ref_price.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/listPrice', methods=['GET'])
def read_price():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        route = request.args.get('route')
        Class = request.args.get('class')
        Day = request.args.get('day')
        print(Class)
        #cityTo = request.args.get('to')
        if route and Class and Day:
            if (Day=='0' or Day=='5' or Day=='6'):
                todo = [(doc.get('id'),doc.get('price_weekend_'+Class.split('_')[0].lower())) for doc in todo_ref_price.where(u'id',u'==',route).stream()]
            else:
                todo = [(doc.get('id'),doc.get('price_normal_'+lower(Class.split('_')[0].lower()))) for doc in todo_ref_price.where(u'id',u'==',route).stream()]
            return jsonify(todo), 200
    
        else:
            all_todos = [doc.to_dict() for doc in todo_ref_price.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/updatePrice', methods=['POST', 'PUT'])
def update_price():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref_price.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/deletePrice', methods=['GET', 'DELETE'])
def delete_price():
    """
        delete() : Delete a document from Firestore collection.
    """
    try:
        # Check for ID in URL query
        todo_id = request.args.get('id')
        todo_ref_price.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
####################################################################################################################################
@app.route('/checkSeat',methods=['GET'])
def check_seat():
    try:
        todo_seat=[]
        date = request.args.get('date')
        cityFrom = request.args.get('from')
        cityTo = request.args.get('to')
        Class = request.args.get('class')
        if cityFrom and cityTo:
            todo = [doc.get('id') for doc in todo_ref_flight.where(u'start',u'==',cityFrom).where(u'end',u'==',cityTo).stream()]
        for flight in todo:
            todo_seat.append([ (doc.get('id'),doc.get(Class)) for doc in todo_ref_seat.document(date).collection(flight).stream()] )
        if len(todo_seat[0])==0 :
            tmp = [doc.get('id') for doc in todo_ref_seat.stream()]
            if date not in tmp:
                todo_ref_seat.document(date).set({"id":date})
            for flight in todo:
                todo_ref_seat.document(date).collection(flight).document(flight).set({"id":flight,"Bs_left":30 ,"Eco_left":250,"F_left":10, "Bs_booked":[], "Eco_booked":[], "F_booked":[]})
            todo_seat=[]
            todo_seat.append([ (doc.get('id'),doc.get(Class)) for doc in todo_ref_seat.document(date).collection(flight).stream()] )

        
        return jsonify(todo_seat), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/addSeat', methods=['POST'])
def create_seat():
    """
        create() : Add document to Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post'}
    """
    try:
        date = request.json['date']
        todo_ref_flight.document(id).set(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/listSeat', methods=['GET'])
def read_seat():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        cityFrom = request.args.get('from')
        cityTo = request.args.get('to')
        if cityFrom and cityTo:
            print(123)
            todo = [doc.to_dict() for doc in todo_ref_flight.where(u'start',u'==',cityFrom).where(u'end',u'==',cityTo).stream()]
            return jsonify(todo), 200
        else:
            all_todos = [(doc.get('id'),doc.get('start'),doc.get('end')) for doc in todo_ref_flight.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/getBookedSeat', methods=['GET'])
def booked_seat():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        date_depart = request.args.get('date_depart')
        flight_depart = request.args.get('flight_depart')
        Class = request.args.get('Class')

        seatArrayX = todo_ref_seat.document(date_depart).collection(flight_depart).document(flight_depart).get().get(Class.split('_')[0]+'_booked')
        if request.args.get('date_return'):
            date_return = request.args.get('date_return')
            flight_return = request.args.get('flight_return')
            seatArrayY = todo_ref_seat.document(date_return).collection(flight_return).document(flight_return).get().get(Class.split('_')[0]+'_booked')
            return jsonify({"depart":seatArrayX, "return":seatArrayY}), 200
        else:
            return jsonify({"depart":seatArrayX}), 200
        
    except Exception as e:
        return f"An Error Occured: {e}"


@app.route('/updateSeat', methods=['POST', 'PUT'])
def update_seat():
    """
        update() : Update document in Firestore collection with request body.
        Ensure you pass a custom ID as part of json body in post request,
        e.g. json={'id': '1', 'title': 'Write a blog post today'}
    """
    try:
        id = request.json['id']
        todo_ref_flight.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/checkFlight', methods=['GET'])
def check_flight():
    try:
        todo_seat=[]
        date = request.args.get('date')
        cityFrom = request.args.get('from')
        cityTo = request.args.get('to')
        Class = request.args.get('class')
        Day = request.args.get('day')
        guest = request.args.get('guest')
        strDay =''
        if(Day==0 or Day==5 or Day==6):
            strDay='price_weekend'
        else:
            strDay='price_normal'
        if not todo_ref_seat.document(date).get().exists:
            todo_ref_seat.document(date).set({"id":date})
        if cityFrom and cityTo:
            todo = [doc.to_dict() for doc in todo_ref_flight.where(u'start',u'==',cityFrom).where(u'end',u'==',cityTo).stream()]
        for flight in todo:
            tmp = [doc.to_dict() for doc in todo_ref_seat.document(date).collection(flight['id']).get()]
            if(len(tmp)==0):
                 todo_ref_seat.document(date).collection(flight['id']).document(flight['id']).set({"id":flight['id'],"Bs_left":30 ,"Eco_left":250,"F_left":10, "Bs_booked":[], "Eco_booked":[], "F_booked":[]})
            x = todo_ref_seat.document(date).collection(flight['id']).document(flight['id']).get().get(Class)
            if x>=int(guest) :
                y = todo_ref_price.document(flight['id']).get().get(strDay+'_'+Class.split('_')[0].lower())
                flight.update({"Seat_left":x , "price":y })
                todo_seat.append(flight)
            
        return jsonify(todo_seat),200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/booking',methods=['POST'])
def booking():
    print(request.json)
    ref = todo_ref_book.document()
    bookig_id = ref.set(request.json)
    x = todo_ref_seat.document(request.json['date_depart']).collection(request.json['flight_depart']).document(request.json['flight_depart']).get().get(request.json['Class'])
    x = x-len(request.json['personal_data'])
    todo_ref_seat.document(request.json['date_depart']).collection(request.json['flight_depart']).document(request.json['flight_depart']).update({request.json['Class']:x})

    seatArrayX = todo_ref_seat.document(request.json['date_depart']).collection(request.json['flight_depart']).document(request.json['flight_depart']).get().get(request.json['Class'].split('_')[0]+'_booked')
    seatArrayX.extend(request.json['seat_depart'])
    todo_ref_seat.document(request.json['date_depart']).collection(request.json['flight_depart']).document(request.json['flight_depart']).update({request.json['Class'].split('_')[0]+'_booked':seatArrayX})

    data = json.loads(request.data)
    if('date_return' in data and 'flight_return' in data):
        y = todo_ref_seat.document(request.json['date_return']).collection(request.json['flight_return']).document(request.json['flight_return']).get().get(request.json['Class'])
        y = y-len(request.json['personal_data'])
        todo_ref_seat.document(request.json['date_return']).collection(request.json['flight_return']).document(request.json['flight_return']).update({request.json['Class']:y})

        seatArrayY = todo_ref_seat.document(request.json['date_return']).collection(request.json['flight_return']).document(request.json['flight_return']).get().get(request.json['Class'].split('_')[0]+'_booked')
        seatArrayY.extend(request.json['seat_return'])
        todo_ref_seat.document(request.json['date_return']).collection(request.json['flight_return']).document(request.json['flight_return']).update({request.json['Class'].split('_')[0]+'_booked':seatArrayY})
    return jsonify({"id": ref.id}), 200

@app.route('/result',methods=['GET'])
def result():
    print(request.json)
    booking_id = request.args.get('id')
    todo_ref_book.document(booking_id)
    if todo_ref_book.document(booking_id).get().exists:
        book = todo_ref_book.document(booking_id).get().to_dict()
        del book['Address']
        del book['Email']
        del book['Zip']
        del book['payment']

        flight_depart = todo_ref_flight.document(book['flight_depart']).get().to_dict()

        book.update({'flight_depart':flight_depart})
        if not book['isOneway']:
            flight_return = todo_ref_flight.document(book['flight_return']).get().to_dict()
            book.update({'flight_return':flight_return})

        return jsonify(book), 200
    else:
        return f"Not Found"
