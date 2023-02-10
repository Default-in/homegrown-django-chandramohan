#Redirect URI: https://localhost:3000/users/auth/producthunt/callback

#API Key: ''

#API Secret: ''

#Token: 0U0YFe5-X_dzce0YuoeiOJcyrZfKiGu_m7XK7pwnSyA
#Expires: Never 

HEADERS = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {'0U0YFe5-X_dzce0YuoeiOJcyrZfKiGu_m7XK7pwnSyA'}",
        "Host": "api.producthunt.com"
    }

BASE_POSTS_URL = "https://api.producthunt.com/v1/posts/all?per_page=50&page="    

TOP_POSTS_URL = 'https://api.producthunt.com/v1/posts/all?sort_by=votes_count&order=desc&search[featured_month]='