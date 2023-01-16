import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

spreadsheet_url = "https://docs.google.com/spreadsheets/d/your_spreadsheet_id"

sheet = client.open_by_url(spreadsheet_url).sheet1

data = sheet.get_all_values()

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']

current_week_indices = {day: days.index(day) + 6 for day in days}
next_week_indices = {day: days.index(day) + 11 for day in days}

now = datetime.datetime.now()
current_day = days[now.weekday()]

employees = {}
for row in data:
    name = row[2]
    role = row[3]
    if name not in employees:
        employees[name] = {"role": role}
    for day, index in current_week_indices.items():
        if day < current_day:
            continue
        value = row[index]
        if value and value not in ["OUT", "H"]:
            value = int(value)
            if value < 8:
                if "availability" not in employees[name]:
                    employees[name]["availability"] = {}
                if day not in employees[name]["availability"]:
                    employees[name]["availability"][day] = value
    for day, index in next_week_indices.items():
        value = row[index]
        if value and value not in ["OUT", "H"]:
            value = int(value)
            if value < 8:
                if "availability" not in employees[name]:
                    employees[name]["availability"] = {}
                if day not in employees[name]["availability"]:
                    employees[name]["availability"][day] = value

case_duration = input("How many hours will the case take? ")

employees_sorted = sorted(employees.items(), key=lambda x: sum(x[1]["availability"].values()), reverse=True)

filtered_employees = [(name, employee) for name, employee in employees_sorted if sum(employee["availability"].values()) >= int(case_duration)]

for name, employee in filtered_employees:
    print(f"{name}, Role: {employee['role']} - Availability: {employee['availability']}")