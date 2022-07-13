import mysql.connector

connection = mysql.connector.connect(host='localhost', port = '3306', database='secadora', user='cursoIoT', password='cursoIoT')

def insetarDatos(tem, pes, vel, tip):
    try:
        query = "insert into muestras (temperatura, peso, velocidad, hora, fecha, tipoProducto) values (" + str(tem) + ", " + str(pes) + ", " + str(vel) + ", NOW(), NOW(), '" + tip + "');"
        print(query)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        cursor.close()
        
    except mysql.connector.Error as error:
        print("Failed to insert record into Laptop table {}".format(error))

insetarDatos(32.21, 12.62, 421, 'naranjas')