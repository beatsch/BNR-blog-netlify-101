from bottle import route, run, get, post, put, delete, request, response, error
import json, sqlite3
from json import dumps

# Define the database.
conn = sqlite3.connect('data.db')
# Define the cursor for the database.
c = conn.cursor()

# Create a table for the data.
def createTable():
    c.execute('CREATE TABLE IF NOT EXISTS Telephones(brand TEXT, screensize INTEGER, image TEXT , model TEXT, os TEXT)')
createTable()

# Create a product item.
@post('/phones')
def createItem():
    def insertData():
        # Insert into the table called 'Telephones' the data (brand, screensize, image, model and os) of the product item.
        c.execute('INSERT INTO Telephones(brand, screensize, image , model, os) VALUES(?, ?, ?, ?, ?)', (request.json.get('brand'), request.json.get('screensize'), request.json.get('image'), request.json.get('model'), request.json.get('os')))
        conn.commit()
    insertData()
    # The status code indicates that the prodct item has been created.
    response.status = 201
    response.headers['Access-Control-Allow-Methods']='POST, GET, PUT, DELETE'
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Content-Type']='application/json'
    response.headers['Host']='localhost:8080'
    response.headers['Status-Code']='201 (Created)'

# Retrieve the full dataset.
@get('/phones')
def getData():
    # Select all rows and ROWIDs from the table called 'Telephones'.
    c.execute('SELECT * FROM Telephones')
    # Fetch all the selected data.
    data = c.fetchall()
    # If the there is no content, then there should be a status code indicating this.
    if len(data) == 0:
        # Thus, the status code is 404. This indicates that the item is not found.
        response.status = 404
        response.headers['Access-Control-Allow-Methods']='POST, GET, PUT, DELETE'
        response.headers['Access-Control-Allow-Origin']='*'
        response.headers['Content-Type']='application/json'
        response.headers['Host']='localhost:8080'
        message = {'Error': '404 (Not found)'}
        return json.dumps(message)
    # Else, if there is content, then the data of the item should be returned.
    else:
        # The status code is by default 200 (and content is returned).
        response.headers['Access-Control-Allow-Methods']='POST, GET, PUT, DELETE'
        response.headers['Access-Control-Allow-Origin']='*'
        response.headers['Content-Type']='application/json'
        response.headers['Host']='localhost:8080'
        response.headers['Status-Code']='200 (OK)'
        # Reference: https://stackoverflow.com/questions/35615083/python-query-sqlite-map-values-to-column-names
        conn.row_factory = sqlite3.Row
        c2 = conn.cursor()
        # Select all rows and ROWIDs from the table called 'Telephones'.
        c2.execute('SELECT *, ROWID AS id FROM Telephones')
        # Fetch all the selected data.
        data = c2.fetchall()
        # JSON array called 'rowarray_list'.
        rowarray_list = []
        for row in data:
            # Dictonary with the columns as the 'key'.
            item = dict(zip(row.keys(), row))
            # Appeend the item to 'rowarray_list'.
            rowarray_list.append(item)
        # Return the data in JSON format.
        return json.dumps(rowarray_list)

# Retrieve an item .
@get('/phones/<id>')
def getPhone(id):
    # Select all and the rowids from the the table called 'Telephones' with the specific id.
    c.execute('SELECT *, ROWID FROM Telephones WHERE ROWID=?', [id])
    # The cursor fetches all selected data.
    data = c.fetchall()
    # If there is no actual data, it means that there is no item with the specific id.
    if len(data) == 0:
        # Therefore, the status code is 404. This indicates that the item is not found.
        response.status = 404
        response.headers['Access-Control-Allow-Methods']='GET, DELETE'
        response.headers['Access-Control-Allow-Origin']='*'
        response.headers['Content-Type']='application/json'
        response.headers['Host']='localhost:8080'
        message = {'Error': '404 (Not found)'}
        return json.dumps(message)
    # If len(data) is not equal to zero, then  return the desired item with its id.
    else:
        # The status code is by default 200 (and content is returned).
        response.headers['Access-Control-Allow-Methods']='GET, DELETE'
        response.headers['Access-Control-Allow-Origin']='*'
        response.headers['Content-Type']='application/json'
        response.headers['Host']='localhost:8080'
        response.headers['Status-Code']='200 (OK)'
        # Reference: https://stackoverflow.com/questions/35615083/python-query-sqlite-map-values-to-column-names
        conn.row_factory = sqlite3.Row
        c2 = conn.cursor()
        # Select all rows and ROWIDs (as 'id') from the table called 'Telephones' where ROWID equals the specific id.
        c2.execute('SELECT *, ROWID AS id FROM Telephones WHERE ROWID=?', [id])
        # Fetch all the selected data.
        data = c2.fetchall()
        # JSON array called 'rowarray_list'.
        rowarray_list = []
        for row in data:
            # Dictonary with the columns as the 'key'.
            item = dict(zip(row.keys(), row))
            # Appeend the item to 'rowarray_list'.
            rowarray_list.append(item)
            # Return the data in JSON format.
        return json.dumps(rowarray_list)

# Update data of an item.
@put('/phones')
def changeId():
    # Select the row from the table called 'Telephones' with the rowid equal to the specific id.
    c.execute('SELECT * FROM Telephones WHERE ROWID=?', [request.json.get('id')])
    # The cursor fetches all selected data.
    data = c.fetchall()
    # If there is no actual data, it means that there is no item with the specific id.
    if len(data) == 0:
        # Therefore, the status code is 404. This indicates that the item is not found.
        response.status = 404
        response.headers['Access-Control-Allow-Methods']='POST, GET, PUT, DELETE'
        response.headers['Access-Control-Allow-Origin']='*'
        response.headers['Content-Type']='application/json'
        response.headers['Host']='localhost:8080'
        message = {'Error': '404 (Not found)'}
        return json.dumps(message)
    else:
        # Selected from the table called 'Telephones' the row where brand, screensize, image, model and os equal the JSON data from the request body.
        c.execute('SELECT * FROM Telephones WHERE brand=? AND screensize=? AND image=? AND model=? AND os=? AND ROWID=?', [request.json.get('brand'), request.json.get('screensize'), request.json.get('image'), request.json.get('model'), request.json.get('os'), request.json.get('id')])
        # The cursor fetches all selected data.
        data = c.fetchall()
        # If there is no actual data, it means that there is an item with the specific id, but not the exact same data.
        if len(data) == 0:
            c.execute('UPDATE Telephones SET brand=?, screensize=?, image=?, model=?, os=? WHERE ROWID=?', [request.json.get('brand'), request.json.get('screensize'), request.json.get('image'), request.json.get('model'), request.json.get('os'), request.json.get('id')])
            # The response status indicates that the request has succesfully been processed, although the response body contains no content.
            response.status = 204
            response.headers['Access-Control-Allow-Methods']='POST, GET, PUT, DELETE'
            response.headers['Access-Control-Allow-Origin']='*'
            response.headers['Content-Type']='application/json'
            response.headers['Host']='localhost:8080'
            response.headers['Status-Code']='204 (No content)'
        # Else, if the already has been updated or if the to be updated data is the same as the incoming data, then the data of the item should not be updated.
        else:
            # Therefore, the status code is 409. This indicates that the item already exists.
            response.status = 409
            response.headers['Access-Control-Allow-Methods']='POST, GET, PUT, DELETE'
            response.headers['Access-Control-Allow-Origin']='*'
            response.headers['Content-Type']='application/json'
            response.headers['Host']='localhost:8080'
            message = {'Error': '409 (Conflict)'}
            return json.dumps(message)

 # Delete an item.
@delete('/phones/<id>')
def deletePhone(id):
    # Select the row from the table called 'Telephones' which has the specific rowid.
    c.execute('SELECT * FROM Telephones WHERE rowid=?', [id])
    # The cursor fetches all selected data.
    data = c.fetchall()
    # If there is no actual data, it means that there is no item with the specific id.
    if len(data) == 0:
        # Thus, the status code is 404. This indicates that the item is not found.
        response.status = 404
        response.headers['Access-Control-Allow-Methods']='GET, DELETE'
        response.headers['Access-Control-Allow-Origin']='*'
        response.headers['Host']='localhost:8080'
        message = {'Error': '404 (Not found)'}
        return json.dumps(message)
    # Else, if there exists a data item with the specific id, then it will be deleted.
    else:
        # Delete all rows from the table called 'Telephones' with the specifix rowid.
        c.execute('DELETE FROM Telephones WHERE rowid=?', [id])
        conn.commit()
        # The response status indicates that the request has succesfully been processed, although the response body contains no content.
        response.status = 204
        response.headers['Access-Control-Allow-Methods']='GET, DELETE'
        response.headers['Access-Control-Allow-Origin']='*'
        response.headers['Host']='localhost:8080'
        response.headers['Status-Code']='204 (No content)'

# Reset the full dataset.
@delete('/phones')
def resetDatabase():
    # Select all rows from the table called 'Telephones'.
    c.execute('SELECT * FROM Telephones')
    # The cursor fetches all selected data.
    data = c.fetchall()
    # If there is no actual data, it means that there is no data to delete.
    if len(data) == 0:
        # Thus, the status code is 404. This indicates that no data is not found.
        response.status = 404
        response.headers['Access-Control-Allow-Methods']='POST, GET, PUT, DELETE'
        response.headers['Access-Control-Allow-Origin']='*'
        response.headers['Host']='localhost:8080'
        message = {'Error': '404 (Not found)'}
        return json.dumps(message)
    else:
        # Delete all from the table called 'Telephones'.
        c.execute('DELETE FROM Telephones')
        conn.commit()
        # The response status indicates that the request has succesfully been processed, although the response body contains no content.
        response.status = 204
        response.headers['Access-Control-Allow-Methods']='POST, GET, PUT, DELETE'
        response.headers['Access-Control-Allow-Origin']='*'
        response.headers['Host']='localhost:8080'
        response.headers['Status-Code']='204 (No content)'

run(host='localhost', port=8080, reloader=True, debug=True)

@error(400)
def error400(error):
    return 'Error: 400 (Bad request)'

@error(404)
def error404(error):
    return 'Error: 404 (Not found)'

@error(405)
def error405(error):
    return 'Error: 405 (Method not allowed)'

@error(409)
def error409(error):
    return 'Error: 409 (Conflict)'

@error(500)
def error500(error):
    return 'Error: 500 (Internal server error)'
