from flask import jsonify
import datetime
from dateutil.relativedelta import relativedelta

def analysis(data, heading):
    try:
        per = ((data[-1][heading] - data[0][heading]) / data[0][heading]) * 100
    except (KeyError, ZeroDivisionError):
        return {"error": f"Unable to calculate percentage change for heading '{heading}'"}, 400

    if per > 0:
        value = f"{abs(per):.2f}% increase"
    elif per < 0:
        value = f"{abs(per):.2f}% decrease"
    else: 
        value = 'same'

    return value

def compare(data1, data2, heading):
    count1, count2 = 0, 0
    for i in range(len(data1)):
        d1 = data1[i]
        count1 += d1[heading]
    for j in range(len(data2)):
        d2 = data2[j]
        count2 += d2[heading]
    c1 = count1/len(data1)
    c2 = count2/len(data2)
    
    try:
        p1 = ((c1-c2)/c1)*100
        p2 = ((c1-c2)/c1)*100
    except (KeyError, ZeroDivisionError):
        return {"error": f"Unable to calculate percentage change for heading '{heading}'"}, 400
    
    if c1 > c2:
        value = f"Window 1 is greater than Window 2 by {abs(p2):.2f}%"
    elif c1 < c2:
        value = f"Window 2 is greater than Window 1 by {abs(p1): .2f}%"
    else:
        value = f"Window 1 and Window 2 show similar trend"
        
    return value

def format(st, window):
    try:
        st = datetime.datetime.strptime(st, '%Y-%m-%dT%H:%M:%S')  
    except ValueError:
        return jsonify({"error": "Invalid startTime format. Use 'YYYY-MM-DDTHH:MM:SS'"}), 400
    
    try: 
        duration = int(window[:-1])
        unit = window[-1]
    except ValueError:
        return jsonify({"error": "Invalid window format. Use formats like '3d', '2m', '1h'"}), 400
    
    if unit == 'm':
        et = st + relativedelta(months=duration)
    elif unit == 'd':
        et = st + relativedelta(days=duration)
    elif unit == 'h':
        et = st + relativedelta(hours=duration)
    else:
        return jsonify({"error": "Invalid window unit. Use 'm', 'd', or 'h'"}), 400
    
    return st, et