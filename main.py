import sys
import time
from bs4 import BeautifulSoup, SoupStrainer
from utils import *
import parser
import pandas as pd
#from ggplot import *
import scipy.stats as ss
import pdb

MY_NAME = "Micah Twyc Carroll" # your name as it appears on Facebook
max_people_per_convo = 2

with open('facebook-dump/html/messages.htm', 'r') as message_file:
    messages_htm = message_file.read()

print("File opened")

bs_struct = BeautifulSoup(messages_htm, "html.parser")
threads = bs_struct.find_all("div", {"class": "thread"})

print "You have {} threads".format(len(threads))

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

print "After filtering by max num of people in the conversation, we are considering {} threads".format(len(friends_message_count))

top_x = 4
sorted_top_friends_to = sorted(friends_message_count.items(), key= lambda x: x[1][0], reverse=True)[0:top_x]
sorted_top_friends_from = sorted(friends_message_count.items(), key=lambda x: x[1][1], reverse=True)[0:top_x]
print sorted_top_friends_to
print sorted_top_friends_from

top_friends_to_key = set([friend[0] for friend in sorted_top_friends_to])
top_friends_from_key = set([friend[0] for friend in sorted_top_friends_from])

##########
# Pt .2 ##
##########
print "Starting secondary analysis"

my_lp = parser.LeadaParser(threads, MY_NAME)

unstacked_from, unstacked_to, unstacked_total = my_lp.extract_top_friends_series(top_friends_from_key, top_friends_to_key)
print unstacked_from.head()
