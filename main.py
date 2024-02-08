import billboard
from datetime import datetime, timedelta
import pandas as pd
import bar_chart_race as bcr
import matplotlib.pyplot as plt
import matplotlib.animation
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import numpy as np
import random
from matplotlib.colors import to_rgba
import textwrap
import time

def get_top_songs(date):
    chart = billboard.ChartData('hot-100', date=date)
    return chart[0:10]

def dict_top_songs(start_date):
    song_dict = {}
    current_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    current_date = datetime.strftime(current_date_dt, "%Y-%m-%d")
    songs = get_top_songs(current_date)
    for rank, song in enumerate(songs):
        song_dict[rank] = {'artist': song.artist, 'title': song.title}
    return song_dict

def create_data(start_date, end_date):
    data_dict = {}

    current_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")

    while current_date_dt <= end_date_dt:
        print(current_date_dt)
        current_date = datetime.strftime(current_date_dt, "%Y-%m-%d")
        result_dict = dict_top_songs(current_date)
        data_dict[current_date] = result_dict
        current_date_dt += timedelta(days=7)
    return data_dict


def lineGraphData(all_data):
    new_dict = {}
    for date, val in all_data.items():
        for rank, data in val.items():
            key = data['title'] +" - " +data['artist']
            if key not in new_dict:
                new_dict[key] = []
    for date, val in all_data.items():
        for rank, data in val.items():
            key = data['title'] +" - " +data['artist']
            new_dict[key].append(rank)

        for song, dat in new_dict.items():
            if song not in [data['title'] + " - " + data['artist'] for data in val.values()]:
                dat.append(11)
    return new_dict

def createGraph(all_data, data, start_date, title):
    print("Making Graph")
    x = list(range(len(all_data.keys())))

    if "year" in title.lower():
        figsize = (16, 9)  # Horizontal YouTube video size
    else:
        figsize = (9, 16)  # Vertical YouTube short size
    fig, ax = plt.subplots(figsize=figsize)
    y_list = []
    y_1_list = []
    line_list = []
    text_list = []
    if "year" in title.lower():
        fontsize = 12
        interval=30
        frames = len(all_data.keys()) * 120
        x_fontsize=14
        x_labels_strf = "%#m/%#d"
    else:
        fontsize = 16
        interval=30
        x_fontsize=20
        x_labels_strf = "%m-%d"
        frames = len(all_data.keys()) * 70
    x_1 = np.linspace(0,len(x)-1,frames)
    for word,ranks in data.items():
        y = [rank + 1 for rank in ranks]
        y_list.append(ranks)
        y_1 = np.interp(x_1, x, y)
        y_1_list.append(np.interp(x_1, x, y))
        line1, = ax.plot(x_1, y_1, color=get_random_color(), linewidth=2.0)
        line_list.append(line1)
        wrapped_text = textwrap.fill(word, width=20)
        text_list.append(ax.text(1, 1, wrapped_text, fontsize=fontsize, verticalalignment='center'))

    ax.set_title(title, fontsize=20)

    def myupdating(i):
        for j in range(len(y_1_list)):
            if i < len(y_1_list[j]):
                line_list[j].set_data(x_1[:i],y_1_list[j][:i])
                text_list[j].set_position((x_1[i],y_1_list[j][i]))
                if y_1_list[j][i] > 10.4:
                    text_list[j].set_visible(False)
                else:
                    text_list[j].set_visible(True)

    print("Animation Creation")
    myanimation = FuncAnimation(fig,myupdating,frames=frames+1,interval=interval)
    ax.set_ylim(.5, 10.5)
    ax.set_ylabel("Rank", fontsize=20)
    ax.set_yticks(range(1, 11))
    ax.set_yticklabels([str(h) for h in range(1, 11)], fontsize=20)
    ax.invert_yaxis()

    ax.set_xticks(range(len(all_data.keys())))
    date_labels = [datetime.strptime(date, "%Y-%m-%d") for date in all_data.keys()]
    ax.set_xticklabels([date.strftime(x_labels_strf) for date in date_labels], fontsize=x_fontsize)
    if "year" in title.lower():
        for label in ax.get_xticklabels()[1::3]:
            label.set_y(label.get_position()[1] - 0.03)
        for label in ax.get_xticklabels()[2::3]:
            label.set_y(label.get_position()[1] - 0.06)
    else:
        for label in ax.get_xticklabels()[::2]:
            label.set_y(label.get_position()[1] - 0.03)
    print("Writing File")
    writer = FFMpegWriter(fps=30, metadata=dict(artist='Me'), bitrate=1800)
    file_name = title + ".mp4"
    myanimation.save(file_name, writer=writer)
    print("File Saved")
    return file_name

def get_random_color():
    return "#{:02x}{:02x}{:02x}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def main():
    start = time.time()
    #make it so it generates videos over year/season/month
    start_date, end_date, title = decide()
    print('Creating Data...')
    all_data = create_data(start_date, end_date)
    data = lineGraphData(all_data)
    thing = createGraph(all_data, data, start_date, title)
    print(time.time()-start)
    return thing

def decide():
    type = random.choice(['year']) #add year if works 'season', 'quarter'
    year = random.choice(list(range(1960, 2022)))
    title = ""
    if type == 'year':
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        title = f"Top Songs for the Year {year}"
    elif type == 'season':
        season = random.choice(['winter', 'spring', 'summer', 'autumn'])
        if season == 'winter':
            start_date = f"{year}-12-21"
            end_date = f"{year}-03-20"
        elif season == 'spring':
            start_date = f"{year}-03-21"
            end_date = f"{year}-06-20"
        elif season == 'summer':
            start_date = f"{year}-06-21"
            end_date = f"{year}-09-22"
        elif season == 'autumn':
            start_date = f"{year}-09-23"
            end_date = f"{year}-12-20"
        title = f"Top Songs for {season.title()} of {year}"
    elif type == 'quarter':
        import calendar
        quarter = random.choice([1, 2, 3, 4])
        quarter_start = (quarter - 1) * 3 + 1

        _, last_day = calendar.monthrange(year, quarter_start + 2)
        quarter_end = min(quarter_start + 2, last_day)
        start_date = f"{year}-{quarter_start:02d}-01"
        end_date = f"{year}-{quarter_end:02d}-{last_day}"
        title = f"Top Songs for Q{quarter} of {year}"
    print(start_date, end_date, title)
    return start_date, end_date, title
