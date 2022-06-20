#Main.py for SmrtCube Project Submission
#Matthew Moulton and Toby Soukup

#import libraries
try:
  from pathlib import Path
  from orbit import ISS
  from skyfield.api import load
  import csv
  import time
  import datetime
  base_folder = Path(__file__).parent.resolve()
except:
  print("attempting to run in SenseHat Emulator mode")
  mode = 'sensehat'
else:
  print("attempting to run in AstroPi mode")
  mode = 'astropi'
  
def create_csv_file(data_file):
    #Create a new CSV file and add the header row
    try:
      with open(data_file, 'w') as f:
        writer = csv.writer(f)
        if mode == 'emulator':
          header = ("Before Date", "Lattitude", "Longtitude", "Elevation (km)", "Velocity (x km/s)", "Velocity (y km/s)", "Velocity (z km/s)", "After Date")
        else:
          header = ("Before Date", "Lattitude", "Longtitude", "Elevation (km)", "Velocity (x km/s)", "Velocity (y km/s)", "Velocity (z km/s)", "Magnetometer X", "Magnetometer Y", "Magnetometer Z", "Gyroscope X", "Gyroscope Y", "Gyroscope Z", "Accelerometer X", "Accelerometer Y", "Accelerometer Z", "After Date")

        writer.writerow(header)
    except:
      print("failed to open csv file")
    else:
      print("successfully openned csv file")

def add_csv_data(data_file, data):
    #Add a row of data to the data_file CSV
    try: 
      with open(data_file, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(data)  
    except:
      pass
  
if mode == 'astropi':
  # create a csv file and prepare it for writing
  data_file = base_folder/"dataCSV.csv"
  create_csv_file(data_file)  
  
try:
  from sense_hat import SenseHat
  import datetime
  import time
  sense = SenseHat()
except:
  print("attempting to run in astropi emulation mode")
  mode = 'emulator'
else:
  print('running with sensehat')

def sense_hat_datetime_to_float(d):
    epoch = datetime.datetime.utcfromtimestamp(0)
    total_seconds =  (d - epoch).total_seconds()
    # total_seconds will be in decimals (millisecond precision)
    return total_seconds
    
def datetime_to_float(d):
    return d.timestamp()
    
if mode == 'sensehat':
  ts = datetime.datetime
  start_time = sense_hat_datetime_to_float(ts.now())
  now = sense_hat_datetime_to_float(ts.now())
else:
  ts = load.timescale() # Loads current timescale from the Skyfield API library
  start_time = datetime_to_float(ts.now().utc_datetime())
  now = datetime_to_float(ts.now().utc_datetime())

# run for 10680 seconds (178 minutes)
# for testing using 60 seconds --- MUST CHANGE!!!
while (now < start_time + 60): 

    # capture time before collecting data 
    t = ts.now()
    if mode == 'sensehat':
      before_date = t.strftime('%Y-%m-%d_%H.%M.%S.%f')[:30]
    else:
      before_date = t.utc_strftime('%Y-%m-%d_%H.%M.%S.%f')[:30]
      
    if mode != 'emulator':
      # collect magnetometer, gyroscope, and accelerometer raw measurements
      mag = sense.get_compass_raw()
      gyro = sense.get_gyroscope_raw()
      nyoom = sense.get_accelerometer_raw()

    if mode != 'sensehat':
      # Compute where the ISS is at time `t` (beforetime)
      position = ISS.at(t)
      # Compute the coordinates of the Earth location directly beneath the ISS
      location = position.subpoint()
      velocity = position.velocity.km_per_s

    # capture time after collecting data
    if mode == 'sensehat':
      after_date = ts.now().strftime('%Y-%m-%d_%H.%M.%S.%f')[:30]
    else:
      after_date = ts.now().utc_strftime('%Y-%m-%d_%H.%M.%S.%f')[:30]

    if mode == 'sensehat':
      # print magnetometer magnetic intensity of the axis in microteslas (µT), 
      #   gyroscope rotational intensity of the axis in radians per second, 
      #   accelerometer acceleration intensity of the axis in Gs.
      print('MAG', before_date, after_date, mag['x'], mag['y'], mag['z'])
      print('GYR', before_date, after_date, gyro['x'], gyro['y'], gyro['z'])
      print('ACC', before_date, after_date, nyoom['x'], nyoom['y'], nyoom['z'])

    if mode == 'emulator':
      # format data for writing to CSV
      data = (
        before_date,
        location.latitude,
        location.longitude,
        location.elevation.km,
        velocity[0],
        velocity[1],
        velocity[2],
        after_date
      )

    if mode == 'astropi':
      # format data for writing to CSV
      data = (
        before_date,
        location.latitude,
        location.longitude,
        location.elevation.km,
        velocity[0],
        velocity[1],
        velocity[2],
        mag['x'],
        mag['y'],
        mag['z'],
        gyro['x'],
        gyro['y'],
        gyro['z'],
        nyoom['x'],
        nyoom['y'],
        nyoom['z'],
        after_date
      )
      # write the data to the csv file
      add_csv_data(data_file, data)

    # wait
    time.sleep(0.5)
    
    # update current time for loop exit criteria
    if mode =='sensehat':
      now = sense_hat_datetime_to_float(ts.now())
    else:
      now = datetime_to_float(ts.now().utc_datetime())

