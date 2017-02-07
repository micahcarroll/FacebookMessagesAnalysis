import sys
import time
from bs4 import BeautifulSoup, SoupStrainer
import parser
from ggplot import *
import scipy.stats as ss
import pdb
from utils import *
import setup
import plotly.plotly as py
import plotly.tools as tls
from plotly.graph_objs import *

username, apikey = setup.main()
py.sign_in(username, apikey)

MY_NAME = "Micah Twyc Carroll" # your name as it appears on Facebook
max_people_per_convo = 2

with open('facebook-dump/html/messages.htm', 'r') as message_file:
    messages_htm = message_file.read()

print("File opened")

bs_struct = BeautifulSoup(messages_htm, "html.parser")
threads = bs_struct.find_all("div", {"class": "thread"})

print("You have {} threads".format(len(threads)))

# The following code might take 1-2 minutes to run, largely depending on the size of your messages.htm
friends_message_count = {} #initialize a counter {friend: [number_of_messages_to, number_of_messages_from]}
for thread in threads:
    friends_in_thread = [name.strip() for name in thread.contents[0].split(",")]
    if too_big_of_group(friends_in_thread, max_people_per_convo):
        continue
    for friend in friends_in_thread:
        friends_message_count[friend] = friends_message_count.get(friend, [0, 0])
    for m in thread.find_all("div", {"class": "message"}):
        user = m.find("span", {"class": "user"})
        friend_name = user.text
        if friend_name == MY_NAME:
            update_message_to_friends(friends_message_count, friends_in_thread, MY_NAME)
        elif "facebook" not in friend_name:
            update_message_from_friend(friends_message_count, friend_name, MY_NAME)

print("After filtering by max num of people in the conversation, we are considering {} threads".format(len(friends_message_count)))

top_x = 10
sorted_top_friends_to = sorted(friends_message_count.items(), key= lambda x: x[1][0], reverse=True)[0:top_x]
sorted_top_friends_from = sorted(friends_message_count.items(), key=lambda x: x[1][1], reverse=True)[0:top_x]
print(sorted_top_friends_to)
print(sorted_top_friends_from)

top_friends_to_key = set([friend[0] for friend in sorted_top_friends_to])
top_friends_from_key = set([friend[0] for friend in sorted_top_friends_from])

##########
# Pt .2 ##
##########
print("Starting secondary analysis")

my_lp = parser.LeadaParser(threads, MY_NAME)

unstacked_from, unstacked_to, unstacked_total = my_lp.extract_top_friends_series(top_friends_from_key, top_friends_to_key)
print(unstacked_from.head())

my_from_line = pd.melt(unstacked_from, id_vars=['date'])
print(ggplot(aes(x='date', y='value', colour="name"), data=my_from_line) + geom_line() + ggtitle('Messages "From" Over Time'))

ranked_df_body = unstacked_total.apply(lambda x: x[1:], axis=1)
ranked_df_body = ranked_df_body.apply(lambda x: ss.rankdata(x, method='min'), axis=1)
print(len(ranked_df_body))
ranked_df_body['date'] = unstacked_total['date']

ranked_unstacked_total = ranked_df_body # rename for clarify
my_total_ranked_line = pd.melt(ranked_unstacked_total, id_vars=['date'])
print(ggplot(aes(x='date', y='value', colour="name"), data=my_total_ranked_line) + \
    scale_x_date(breaks=date_breaks('6 months'), labels='%b %Y') + \
    geom_line(size=3) + \
    ggtitle('Ranking over Time'))

plot = ggplot(aes(x='date', y='value', colour="name", ylim=10), data=my_total_ranked_line) + \
    scale_x_date(breaks=date_breaks('6 months'), labels='%b %Y') + \
    geom_line(size=3) + \
    ggtitle('Ranking over Time')
fig = plot.draw()
py.iplot_mpl(fig)
