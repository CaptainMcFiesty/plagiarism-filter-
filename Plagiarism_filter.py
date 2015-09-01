import praw
import OAuth2Util
import time
import requests
import re

plag_names = []
INTERVAL = 1 #minutes
running = True
subname = 'photoshopbattles' #Your subreddit
backupsubname = 'plagiarismcontrol' #Bot needs access to this priavte sub
user_pat = re.compile('/u/[A-Za-z0-9]+')
LOOP = 60/INTERVAL #Number of times to loop before updating sb list
loops = LOOP
user_agent = "Plagiarism filterr by /u/Captain_McFiesty ver 0.1"

r = praw.Reddit(user_agent)
o = OAuth2Util.OAuth2Util(r)

def do_code():
    refresh_check()
    for comment in praw.helpers.comment_stream(r, subname,limit=None):
        for user in plagnames:
            if comment.author.name == user:
                comment.remove(spam=False)
    return

def refresh_check():
    global loops
    if(loops >= LOOP):
        print("Updating list")
        get_users()
        loops = 0
    else:
        loops += 1
    return

def get_users():
    plag_names.clear()
    wiki = r.get_wiki_page(backupsubname,'plagnames')
    text = wiki.content_md
    users = re.findall(user_pat, text)
    for user in users:
        plag_names.append(user[3:])
    return

while running:
    print("Local time: ", time.asctime(time.localtime(time.time())))
    try:
        o.refresh()
        do_code()
    except KeyboardInterrupt:
        running = False
    except (praw.errors.APIException):
        print("[ERROR]: APIException")
    except (praw.errors.HTTPException):
        print("[ERROR]: HTTPException")
        time.sleep(INTERVAL/2*60)
        continue
    except (praw.errors.PRAWException):
        print("[ERROR]: PRAWException")
        time.sleep(INTERVAL/2*60)
        continue
    except (requests.exceptions.ConnectionError):
        print("Internet down")
        time.sleep(INTERVAL/2*60)
        continue
    except (Exception):
        print("[ERROR]: Other error")
        break
    time.sleep(INTERVAL*60)
