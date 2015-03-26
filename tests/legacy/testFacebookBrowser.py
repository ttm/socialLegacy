import social as S

# put facebook user and password in ~/.social/fb/profile
# or login on the browser window that will appear
# or input login as arguments:
sb=S.ScrapyBrowser()
# input user id and max number of friends reachable from your profile
friends=sb.getFriends()
