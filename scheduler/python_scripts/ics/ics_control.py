from icalendar import Calendar, Event
from datetime import datetime
from pytz import timezone # Timezone
import sys
import random
import os

random.seed(2023) # For reproducibility
weekends = [4,5,11,12,18,19,25,26]
list_of_titles = ["Meeting with manager", "Discussion for Project A", "Phone call with business partner", "Customer support", "Discussion for Project B", "Team meeting"]
list_of_summaries = ["Prepare for presentation", "Eat well before the meeting", "Dress well!", "Alcohol provided", "No food!"]
tz = timezone('US/Eastern')

def generate_calendar():
    for i in range(int(sys.argv[3])):
        role = sys.argv[2]
        if i == 0: # Make it the lead role
            role = f"Senior {sys.argv[2]}"
        else:
            role = f"{sys.argv[2]}_{i}"
        # Formatting uppercase to be the first character only
        role = role.split()
        role = " ".join([x.lower() if x!= "UI_UX" else "UI_UX" for x in role])
        role = list(role)
        role[0] = role[0].upper()
        role = "".join(role)
        cal = Calendar() # Create calendar
        for day in range(1, 32): # for each day
            if day in weekends: # March specific
                continue
            visited = {k:0 for k in range(9, 17)}
            for _ in range(random.randint(1, 3)): # can have 1 to 3 events a day
                event = Event()
                event.add('title', list_of_titles[random.randint(0, len(list_of_titles)-1)])
                event.add('summary', list_of_summaries[random.randint(0, len(list_of_summaries)-1)])
                start_time = sorted(visited.keys(), key = lambda x: (visited[x], x))[0]
                if visited[start_time]: # Will only be true if all the slots are filled
                    continue
                event.add('dtstart', datetime(2023, 3, day, start_time, 0, 0, tzinfo=tz))
                end_time = random.randint(min(start_time+1, 17), min(start_time+3,17))
                for j in range(start_time, end_time+1): # Update the slots
                    visited[j] = 1
                event.add('dtend', datetime(2023, 3, day, end_time, 0, 0, tzinfo=tz))
                event['role'] = role
                cal.add_component(event)
        with open(f"{role}.ics", "wb") as f:
            f.write(cal.to_ical())

def getAvailableTime(list_of_paths):
    general_time_frames = {k:{k1:0 for k1 in range(9,18)} for k in range(1,32) if k not in weekends}
    lead_time_frames = {k:{k1:0 for k1 in range(9,18)} for k in range(1,32) if k not in weekends}
    for cal in list_of_paths:
        with open(cal, 'rb') as f:
            calendar = Calendar.from_ical(f.read())
            for component in calendar.walk():
                if component.name == "VEVENT":
                    start_date = component.get("dtstart").dt
                    end_date = component.get("dtend").dt
                    day = start_date.day
                    # weekday = start_date.weekday() # weekdays in indices
                    start_hour = start_date.hour
                    end_hour = end_date.hour
                    for i in range(start_hour, end_hour):
                        general_time_frames[day][i] += 1
                        if "Senior" in component.get("role"):
                            lead_time_frames[day][i] += 1
    available_time_list = {k:{day:[] for day in range(1,32) if day not in weekends} for k in ["General", "Senior"]}
    for day in general_time_frames:
        for hour in general_time_frames[day]:
            if general_time_frames[day][hour] == 0:
                available_time_list["General"][day].append(hour)
            if lead_time_frames[day][hour] == 0:
                available_time_list["Senior"][day].append(hour)
    return available_time_list

def get_maximum_contiguous(hour_list):
    if len(hour_list) == 1:
        return 1
    else:
        max_count = 1
        curr_count = 1
        for i in range(len(hour_list)-1):
            if hour_list[i+1] - hour_list[i] == 1: # Contiguous
                curr_count += 1
            else:
                max_count = max(max_count, curr_count)
                curr_count = 1
        return max(max_count, curr_count) # Final update

def get_time_slot(list_of_time_slots, hours_needed):
    new_arr = [list_of_time_slots[0]]
    if hours_needed == 1:
        return new_arr
    for i in range(len(list_of_time_slots)-1):
        if list_of_time_slots[i+1] - list_of_time_slots[i] == 1:
            new_arr.append(list_of_time_slots[i+1])
            if len(new_arr) == hours_needed:
                return new_arr
        else:
            new_arr = [list_of_time_slots[i+1]]
    return new_arr

def find_time_slot(today, offset, group_type, hours_needed, available_time_list):
    ret = []
    end = min(31, today+offset)
    for day in range(today, end+1):
        if day in weekends:
            continue
        max_time = get_maximum_contiguous(available_time_list[group_type][day])
        if hours_needed <= max_time:
            ret.append({day : get_time_slot(available_time_list[group_type][day], hours_needed)})
    return ret

def add_new_event(path_to_ics_dir, role, title, summary, day, start_hour, end_hour):
    for cal_file in os.listdir(path_to_ics_dir):
        print(f"{role} : {cal_file}")
        if cal_file.startswith(role):
            with open(f"{path_to_ics_dir}/{cal_file}", "rb") as f:
                calendar = Calendar.from_ical(f.read())
                event = Event()
                event.add('title', title)
                event.add('summary', summary)
                event.add('dtstart', datetime(2023, 3, day, start_hour, 0, 0, tzinfo=tz))
                event.add('dtend', datetime(2023, 3, day, end_hour, 0, 0, tzinfo=tz))
                event['role'] = role
                calendar.add_component(event)
            with open(f"{path_to_ics_dir}/{cal_file}", "wb") as f:
                f.write(calendar.to_ical())
    return

def main():
    if sys.argv[1] == "generate":
        generate_calendar() # Generate the arguments
    elif sys.argv[1] == "available": # Get available time slots
        available_time_list= getAvailableTime(sys.argv[2:])
        time_slots = find_time_slot(12, 30, "General", 6, available_time_list) # starting day, offset days, type of meeting (Senior, General), number of hours needed, list of available times
        print(time_slots)
    elif sys.argv[1] == "add": # Add new data
        role = sys.argv[2]
        add_new_event("./ics_files", role, "ASDASDASD", 1, 10, 12)

if __name__ == "__main__":
    main()
