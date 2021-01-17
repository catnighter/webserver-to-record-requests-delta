from flask import Flask
import time

app = Flask(__name__)
file_result = "/var/www/app1/rec.txt"

@app.route("/")
def index():
  return "reply from app1.py -mod1"

@app.route("/test")
def test():
  f0 = open(file_result, mode='a')
  timestamp = str(time.time()) + "\n"
  f0.write(timestamp)
  f0.flush()
  f0.close()
  return "test ok"

@app.route("/report")
def report():
  delta_all = "Delta between http requests (milli sec) <br> Delta over 1 sec is excluded <br> <br>"
  timestamp1 = ""
  timestamp2 = ""
  for timestamp2 in open(file_result, 'r'):
    if timestamp1 == "":
      timestamp1 = timestamp2
    else:
      timestamp1 = timestamp1.replace('"', '')
      timestamp2 = timestamp2.replace('"', '')
      delta = (float(timestamp2) - float(timestamp1)) * 1000
      if delta <= 1000:
        delta_n = str('{:.4f}'.format(delta)) + "<br>"
        delta_all += delta_n
      timestamp1 = timestamp2

  return(delta_all)

@app.route("/report2")
def report2():
  response = "Mean time of Delta between http requests (milli sec) <br> Delta over 1 sec is excluded <br> <br>"
  timestamp1 = ""
  timestamp2 = ""
  record_count = 0
  delta_sum = 0
  for timestamp2 in open(file_result, 'r'):
    if timestamp1 == "":
      timestamp1 = timestamp2
    else:
      timestamp1 = timestamp1.replace('"', '')
      timestamp2 = timestamp2.replace('"', '')
      delta = (float(timestamp2) - float(timestamp1)) * 1000
      if delta <= 1000:
        record_count += 1
        delta_sum += delta
      timestamp1 = timestamp2

  #calc mean time
  if delta_sum == 0:
    response += "There is no record."
  else:
    delta_mean = delta_sum / record_count
    response += str('{:.4f}'.format(delta_mean))

  return(response)

@app.route("/reset")
def reset():
  f0 = open(file_result, mode='w')
  f0.write("")
  f0.flush()
  f0.close()
  res = "Record file " + file_result + " was reset to null."
  return(res)

if __name__ == "__main__":
  app.run(host="0.0.0.0" ,port=5000)
