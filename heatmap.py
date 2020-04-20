from imdb import IMDb
from itertools import repeat
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import statistics


def tv_show_analysis(search_term):
    
    ia = IMDb()
    
    movie_search = search_term.title()
    
    all_data = ia.search_movie(movie_search)
    
    movie_id = all_data[0].movieID
    
    episodes = ia.get_movie_episodes(movie_id)
    seasons = episodes['data']['episodes']
    
    season_eps = []
    episode_ids = []
    
    j = 0
    while j < len(seasons):
        for x in seasons:
            season_eps.append(len(seasons[x]))
            for f in seasons[x]:
                episode_ids.append(seasons[x][f].movieID)
            j += 1
    
    season_eps_extend = []
    
    q = 0
    while q < len(season_eps):
        season_eps_extend.extend(repeat(q + 1, season_eps[q]))
        q += 1
    
    rating = []
    
    voting_demographics = ia.get_movie_vote_details(movie_id)
    
    age_ratings = []
    age_categories = ['Under 18', '18-29', '30-44', '45+']
    
    try:
        age_ratings.append(voting_demographics['data']['demographics']['aged under 18']['rating'])
    except:
        age_categories.pop(0)
    
    try:
        age_ratings.append(voting_demographics['data']['demographics']['aged 18 29']['rating'])
    except:
        age_categories.pop(1)
    
    try:
        age_ratings.append(voting_demographics['data']['demographics']['aged 30 44']['rating'])
    except:
        age_categories.pop(2)
    
    try:
        age_ratings.append(voting_demographics['data']['demographics']['aged 45 plus']['rating'])
    except:
        age_categories.pop(3)
    
    p = 0
    while p < len(episode_ids):
        try:
            rating.append(ia.get_movie_vote_details(episode_ids[p])['data']['arithmetic mean'])
            p += 1
        except:
            episode_ids.pop(p)
            season_eps_extend.pop(p)
            p += 1
    
    min_rating_index = rating.index(min(rating))
    min_rating_episode = ia.get_movie(episode_ids[min_rating_index])
    min_episode = str(min_rating_episode) + " (" + str(round(min(rating), 1)) + ")"
    
    max_rating_index = rating.index(max(rating))
    max_rating_episode = ia.get_movie(episode_ids[max_rating_index])
    max_episode = str(max_rating_episode) + " (" + str(round(max(rating), 1)) + ")"
    average_rating = round(statistics.mean(rating), 1)
    
    episodes = []
    myset = list(set(season_eps_extend))
    test = []
    for x in myset:
        test.append(season_eps_extend.count(x))
    
    for x in test:
        for j in range(1, x + 1):
            episodes.append(j)
    
    df = pd.DataFrame(list(zip(episodes, season_eps_extend, rating)), columns=['Episode', 'Season', 'Rating'])
    
    data = df.pivot("Episode", "Season", "Rating")
    
    figsize = (8.333 + 3.333 * max(season_eps_extend)), (6.666 + 0.8333 * max(episodes))
    font_size = round(22 / (8.333 + 3.333 * max(season_eps_extend)) * (6.666 + 0.8333 * max(episodes)))
    plt.style.use('dark_background')
    plt.rcParams['figure.facecolor'] = 'grey'
    plt.figure(figsize=figsize)
    font = {'family': 'DejaVu Sans',
            'weight': 'normal',
            'size': font_size}
    plt.rc('font', **font)
    ax = sns.heatmap(data, square=True, vmin=0, vmax=10, cmap="RdYlGn", annot=True, linewidths=.2,
                     annot_kws={"size": round((24.55 - .2758 * max(season_eps_extend)))})
    ax.set(ylim=(0, max(episodes)))
    ax.xaxis.set_ticks_position("top")
    ax.xaxis.set_label_position('top')
    plt.gca().invert_yaxis()
    ax.xaxis.labelpad = font_size
    ax.yaxis.labelpad = font_size
    ax.xaxis.label.set_size(round(font_size * 1.25))
    ax.yaxis.label.set_size(round(font_size * 1.25))
    plt.rcParams['figure.facecolor'] = 'grey'
    
    plot_name = 'test.png'
    plt.savefig(plot_name, facecolor=(0.15, 0.15, 0.15))
    
    plt.style.use('dark_background')
    
    plt_size = (figsize[0] * 0.45, figsize[1] * 0.45)
    plt.rcParams.update({'font.size': round(figsize[0] * 0.45 * figsize[1] * 0.45 * .3)})
    fig = plt.figure(figsize=plt_size)
    ax = fig.add_subplot(111)
    ax.bar(age_categories, age_ratings, label=age_ratings)
    ax.set(ylim=(1, 10.5))
    ax.axes.get_yaxis().set_visible(False)
    plt.title("Average Rating by Age Group")
    
    
    try:
        plt.annotate(str(age_ratings[0]), (-.15, age_ratings[0] + .25))
    except:
        pass
    
    try:
        plt.annotate(str(age_ratings[1]), (.85, age_ratings[1] + .25))
    except:
        pass
    
    try:
        plt.annotate(str(age_ratings[2]), (1.85, age_ratings[2] + .25))
    except:
        pass
    
    try:
        plt.annotate(str(age_ratings[3]), (2.85, age_ratings[3] + .25))
    except:
        pass
    
    line_name = 'line.png'
    plt.savefig(line_name, facecolor=(0.15, 0.15, 0.15))
    
    season_rating = []
    
    season_nums = []
    
    for x in myset:
        num = season_eps.count(x)
        season_nums.append(num)
    
    ep_count = 0
    season_index = 0
    while season_index < (len(season_eps) - 1):
        s = slice(int(ep_count), int((season_eps[season_index]) + sum(season_eps[0:season_index])))
        avg = statistics.mean(rating[s])
        season_rating.append(avg)
        ep_count += (season_eps[season_index])
        season_index += 1
    
    file1 = plot_name
    file2 = line_name
    
    best_season = season_rating.index(max(season_rating)) + 1
    worst_season = season_rating.index(min(season_rating)) + 1
    
    im2 = Image.open(file2)
    
    im1 = Image.open(file1)
    
    w1, h1 = im1.size
    w2, h2 = im2.size
    
    offset = (int(-15), ((h1 - h2) * 8) // 9)
    offset_text_title = (int(w2 * .1), ((h1 - h2) * 1) // 6)
    offset_text_body = (int(w2 * .1), ((h1 - h2) * 2) // 6)
    
    im1.paste(im2, offset)
    
    draw = ImageDraw.Draw((im1))
    
    title_font_size = (w1 * h1 * 0.00001857) + 32.142
    body_font_size = title_font_size * 0.58333
    
    title_font = ImageFont.truetype("/Users/cartermeetze/PycharmProjects/shows/open-sans/OpenSans-Semibold.ttf",
                                    round(title_font_size))
    
    font_width = 0.45
    body_font_height = 0.35
    
    while title_font.getsize(movie_search)[0] > font_width * im1.size[0]:
        title_font_size -= 1
        title_font = ImageFont.truetype("/Users/cartermeetze/PycharmProjects/shows/open-sans/OpenSans-Semibold.ttf",
                                        round(title_font_size))
    
    body_font = ImageFont.truetype("/Users/cartermeetze/PycharmProjects/shows/open-sans/OpenSans-Light.ttf",
                                   round(body_font_size))
    
    draw.text(offset_text_title, movie_search + " \n", font=title_font)
    
    body = "\n" + "Average Rating: " + str(average_rating) + "\n" + "\n" \
                                                                    "Best Season: " + str(best_season) + " (" + str(
        round(max(season_rating), 1)) + ")" + "\n" + "\n" \
                                                     "Worst Season: " + str(worst_season) + " (" + str(
        round(min(season_rating), 1)) + ")"
    
    while body_font.getsize("Average Rating: " + str(average_rating))[0] > font_width * im1.size[0]:
        body_font_size -= 1
        body_font = ImageFont.truetype("/Users/cartermeetze/PycharmProjects/shows/open-sans/OpenSans-Light.ttf",
                                       round(body_font_size))
    
    while body_font.getsize("Average Rating: " + str(average_rating))[1] * 6 > body_font_height * im1.size[1]:
        body_font_size -= 1
        body_font = ImageFont.truetype("/Users/cartermeetze/PycharmProjects/shows/open-sans/OpenSans-Light.ttf",
                                       round(body_font_size))
    
    draw.text(offset_text_body, body, font=body_font)

    signature_offset = (0, h1 - (h1 * 0.045))
    signature_font = ImageFont.truetype("/Users/cartermeetze/PycharmProjects/shows/open-sans/OpenSans-Light.ttf",
                                        round(body_font_size * 0.75))
    
    draw.text(signature_offset, "https://www.linkedin.com/in/carter-meetze/", font=signature_font)

    file_name = movie_search + " Analysis.png"
    im1.save(file_name)
    
    return file_name + " Created"


tv_show_analysis('billions')

