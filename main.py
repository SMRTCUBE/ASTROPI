# main.py for SmrtCube AstroPi Mission Space Project Submission
# Matthew Moulton and Toby Soukup, Ottawa, Canada

# import required libraries for program initialization
from pathlib import Path
from logzero import logger, logfile
from colorzero import Color
from orbit import ISS
from skyfield.api import load
import csv
import time
from datetime import datetime
import pytz
from sense_hat import SenseHat

sense = SenseHat()

def create_csv_file(data_file):
    """ Create a new CSV file and add the header row """
    try:
      with open(data_file, 'w', buffering=1) as f:
        writer = csv.writer(f)
        header = ("BeforeTimestamp", "LoopCounter", "Lattitude", "Longtitude", "Elevation(km)", "Velocity(xkm/s)", "Velocity(ykm/s)", "Velocity(zkm/s)", "MagnetometerX", "MagnetometerY", "MagnetometerZ", "GyroscopeX", "GyroscopeY", "GyroscopeZ", "AccelerometerX", "AccelerometerY", "AccelerometerZ", "AfterTimestamp")
        writer.writerow(header)
    except:
      logger.error(f'{e.__class__.__name__}: {e}')

def add_csv_data(data_file, data):
    """ Add a row of data to a CSV file """
    try:
      with open(data_file, 'a', buffering=1) as f:
        writer = csv.writer(f)
        writer.writerow(data)
    except:
      logger.error(f'{e.__class__.__name__}: {e}')

# set the base location for any files to be the current directory
base_folder = Path(__file__).parent.resolve()

# open a CSV data file
data_file = base_folder/"data.csv"
create_csv_file(data_file)

# set a logfile name
logfile(base_folder/"events.log")

# set LED matrix brightness according to latest email from AstroPi
sense.color.gain = 60

# load timescale from skyfield api for later use
ts = load.timescale()

# capture start time and current time as floating point timestamps
start_time = datetime.timestamp(datetime.now(pytz.utc))
now = datetime.timestamp(datetime.now(pytz.utc))

# initialize loop variables, including end time 178 minutes after start
endoftime = start_time + 10680
counter = 0

logger.info("setting up LED matrix")

# setup LED matrix to show progress by displaying the ISS orbiting the earth

sense.low_light = False

green = (0, 255, 0)
blue = (0, 0, 255)
white = (255,255,255)
nothing = (0,0,0)

G = green
B = blue
O = nothing

# setup initial image of the earth at the centre of the LED matrix
earth = [
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, B, B, O, O, O,
    O, O, B, G, B, G, O, O,
    O, O, G, B, G, B, O, O,
    O, O, O, G, B, O, O, O,
    O, O, O, O, O, O, O, O,
    O, O, O, O, O, O, O, O,
    ]

# define a function for each of the 24 orbital locations of the ISS on the LED matrix
def iss_pixel_0():
    sense.set_pixel(7,2,nothing)
    sense.set_pixel(7,1,white)
    
def iss_pixel_1():
    sense.set_pixel(7,1,nothing)
    sense.set_pixel(6,0,white)

def iss_pixel_2():
    sense.set_pixel(6,0,nothing)
    sense.set_pixel(5,0,white)
    
def iss_pixel_3():
    sense.set_pixel(5,0,nothing)
    sense.set_pixel(4,0,white)
    
def iss_pixel_4():
    sense.set_pixel(4,0,nothing)
    sense.set_pixel(3,0,white)
    
def iss_pixel_5():
    sense.set_pixel(3,0,nothing)
    sense.set_pixel(2,0,white)

def iss_pixel_6():
    sense.set_pixel(2,0,nothing)
    sense.set_pixel(1,0,white)

def iss_pixel_7():
    sense.set_pixel(1,0,nothing)
    sense.set_pixel(0,1,white)

def iss_pixel_8():
    sense.set_pixel(0,1,nothing)
    sense.set_pixel(0,2,white)

def iss_pixel_9():
    sense.set_pixel(0,2,nothing)
    sense.set_pixel(0,3,white)

def iss_pixel_10():
    sense.set_pixel(0,3,nothing)
    sense.set_pixel(0,4,white)

def iss_pixel_11():
    sense.set_pixel(0,4,nothing)
    sense.set_pixel(0,5,white)

def iss_pixel_12():
    sense.set_pixel(0,5,nothing)
    sense.set_pixel(0,6,white)
    
def iss_pixel_13():
    sense.set_pixel(0,6,nothing)
    sense.set_pixel(1,7,white)

def iss_pixel_14():
    sense.set_pixel(1,7,nothing)
    sense.set_pixel(2,7,white)

def iss_pixel_15():
    sense.set_pixel(2,7,nothing)
    sense.set_pixel(3,7,white)

def iss_pixel_16():
    sense.set_pixel(3,7,nothing)
    sense.set_pixel(4,7,white)

def iss_pixel_17():
    sense.set_pixel(4,7,nothing)
    sense.set_pixel(5,7,white)

def iss_pixel_18():
    sense.set_pixel(5,7,nothing)
    sense.set_pixel(6,7,white)

def iss_pixel_19():
    sense.set_pixel(6,7,nothing)
    sense.set_pixel(7,6,white)

def iss_pixel_20():
    sense.set_pixel(7,6,nothing)
    sense.set_pixel(7,5,white)

def iss_pixel_21():
    sense.set_pixel(7,5,nothing)
    sense.set_pixel(7,4,white)

def iss_pixel_22():
    sense.set_pixel(7,4,nothing)
    sense.set_pixel(7,3,white)

def iss_pixel_23():
    sense.set_pixel(7,3,nothing)
    sense.set_pixel(7,2,white)

# put the orbital position functions in an array to easily index them for display
iss_pixel = {
       0 : iss_pixel_0,
       1 : iss_pixel_1,
       2 : iss_pixel_2,
       3 : iss_pixel_3,
       4 : iss_pixel_4,
       5 : iss_pixel_5,
       6 : iss_pixel_6,
       7 : iss_pixel_7,
       8 : iss_pixel_8,
       9 : iss_pixel_9,
       10: iss_pixel_10,
       11: iss_pixel_11,
       12: iss_pixel_12,
       13: iss_pixel_13,
       14: iss_pixel_14,
       15: iss_pixel_15,
       16: iss_pixel_16,
       17: iss_pixel_17,
       18: iss_pixel_18,
       19: iss_pixel_19,
       20: iss_pixel_20,
       21: iss_pixel_21,
       22: iss_pixel_22,
       23: iss_pixel_23
      }

# display the earth image and initialize the ISS display location on the LED matrix
sense.set_pixels(earth)
iss_pixel_23()
pixel_index = 0

# main loop which collects sensor data, timestamps and stores them in a row in the csv file
logger.info("starting main loop")
while (now < endoftime):
  counter += 1
  try:
   
    # every 25 loop iterations (roughly 1.5s) move the ISS image (dot) on the LED matrix to the next orbital position
    if counter % 25 == 0:
      iss_pixel[pixel_index]()
      pixel_index +=1
      if pixel_index == 24:
       pixel_index = 0
    
    # capture the timestamp before SenseHat information is collected
    utc = pytz.timezone('UTC')
    now_datetime = datetime.fromtimestamp(now)
    now_utc = utc.localize(now_datetime)
    t = ts.from_datetime(now_utc)
    before_date = now
    
    # collect the magnotometer, gyroscope, and accelerometer measurements from the SenseHat
    mag = sense.get_compass_raw()
    gyro = sense.get_gyroscope_raw()
    nyoom = sense.get_accelerometer_raw()
    
    # using skyfield TLE information estimates the ISS position and velocity
    position = ISS.at(t)
    location = position.subpoint()
    velocity = position.velocity.km_per_s
    
    # capture the timestamp after SenseHat information is collected
    after_date = datetime.timestamp(datetime.now())
    
    # write collected data to csv file
    data = (
      before_date,
      counter,
      location.latitude.degrees,
      location.longitude.degrees,
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
    add_csv_data(data_file, data)
    
    # log every 100th iteration, to see progress in logs but not too often (very quick loop)
    if counter % 100 == 0:
      logger.info(f"iteration {counter}")
    
    # update now timestamp for loop calculation and exit criteria
    now = datetime.timestamp(datetime.now(pytz.utc))
  except:
    logger.error(f'{e.__class__.__name__}: {e}')

logger.info("completed main loop")

# clear led matrix at end of run
sense.clear(Color('black').rgb_bytes)

