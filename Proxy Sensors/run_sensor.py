from multiprocessing import Process, Queue, Pipe
import timefrom Sensor import getDistance

#https://stackoverflow.com/questions/43861164/passing-data-between-separately-running-python-scripts

print("Main File")
print("Calling Sensor.py")
if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target = getDistance, args = (child_conn,))
    p.start()
    while True:
        distance = parent_conn.recv()
        if distance < 50.0:
            print("Stop the cart")
        else
            print("Continue")
        time.sleep(1)