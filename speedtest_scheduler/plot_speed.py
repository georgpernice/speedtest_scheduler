import matplotlib.pyplot as plt
import numpy as np
import re

pattern_time = re.compile(r"[0-9][0-9]\:[0-9][0-9]")
pattern_date = re.compile(r"[0-9][0-9]\-[0-9][0-9]\-[0-9][0-9]")
pattern_upload = re.compile(r"Up\:\s[0-9]+\.[0-9]+")
pattern_download = re.compile(r"Down\:\s[0-9]+\.[0-9]+")
data = []
dates = []
times = []
upload_speeds = []
download_speeds = []
with open("redirected_urls.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        data.append(line)
for line in data:
    dates.append(pattern_date.search(line).group())
    times.append(pattern_time.search(line).group(0))
    upload_speeds.append(float(pattern_upload.search(line).group(0)[4:]))
    download_speeds.append(float(pattern_download.search(line).group(0)[6:]))


print()
print(dates, " = dates")
print(times, " = times")
print(upload_speeds, " = upload_speeds")
print(download_speeds, " = download_speeds")
days = [
    2000 + 365 * int(date[0:2]) + 30 * int(date[3:5]) + int(date[6:8]) for date in dates
]
minutes = [
    int(time[3:]) + 60 * int(time[:2]) + 24 * 60 * int(day)
    for time, date, day in zip(times, dates, days)
]
print(days, " = days")
print(minutes, " = minutes")
xpoints = np.array(minutes)
ypoints = np.array(download_speeds)
plt.plot(xpoints, np.array(upload_speeds), marker="o", label="Upload Speeds")
plt.plot(xpoints, np.array(download_speeds), marker="x", label="Download Speeds")

plt.title("Wifi Speeds over Minutes since Christ Birth")
plt.xlabel("Minutes since Christ Birth")
plt.ylabel("Wifi Speeds [Mbps]")
plt.grid()
plt.legend()
plt.show()
