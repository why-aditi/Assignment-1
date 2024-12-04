from flask import jsonify
import datetime
from dateutil.relativedelta import relativedelta
import statistics

def analysis(data, heading):
    try:
        per = ((data[-1][heading] - data[0][heading]) / data[0][heading])*100
    except (KeyError, ZeroDivisionError):
        return {"error": f"Unable to calculate percentage change for heading '{heading}'"}, 400
    
    return per

def compare_mean(data1, data2, heading):
    count1, count2 = 0, 0
    for i in range(len(data1)):
        d1 = data1[i]
        count1 += float(d1[heading])
    for j in range(len(data2)):
        d2 = data2[j]
        count2 += float(d2[heading])
    c1 = count1/len(data1)
    c2 = count2/len(data2)
    
    try:
        p = ((c2-c1)/c1)*100
    except (KeyError, ZeroDivisionError):
        return {"error": f"Unable to calculate percentage change for heading '{heading}'"}, 400
    
    value = p    
    return value


def compare_var(data1, data2, heading):
    d1, d2 = [], []
    
    for datapoint in data1:
        d1.append(float(datapoint[heading])) 
    
    for datapoint in data2:
        d2.append(float(datapoint[heading]))  
    
    c1 = statistics.variance(d1)
    c2 = statistics.variance(d2)
    
    try:
        p = ((c2-c1)/c1)*100
    except (KeyError, ZeroDivisionError):
        return {"error": f"Unable to calculate percentage change for heading '{heading}'"}, 400
    
    value = p    
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


def format_comp(start, end):
    try:
        start_time = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S')
        end_time = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S')
        return start_time, end_time
    except ValueError:
        raise ValueError(f"Invalid date format. Expected 'YYYY-MM-DDTHH:MM:SS' but got {start} and {end}.")
