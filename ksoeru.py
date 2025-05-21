#:KSOEUR
#smp-api.iyouke.comAuthorization
#by:A


import os
import requests
from datetime import datetime

# 
def get_proclamation():
    primary_url = "https://github.com/3288588344/toulu/raw/refs/heads/main/tl.txt"
    backup_url = "https://tfapi.cn/TL/tl.json"
    try:
        response = requests.get(primary_url, timeout=10)
        if response.status_code == 200:
            print("\n" + "=" * 45)
            print(" ")
            print("=" * 45)
            print(response.text)
            print("=" * 45 + "\n")
            print("...\n")
            return
    except requests.exceptions.RequestException as e:
        print(f": {e}, ...")

    try:
        response = requests.get(backup_url, timeout=10)
        if response.status_code == 200:
            print("\n" + "=" * 45)
            print(" ")
            print("=" * 45)
            print(response.text)
            print("=" * 45 + "\n")
            print("...\n")
        else:
            print(f" : {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f" : {e}, ")


# 
def get_account_info_and_points(authorization):
    # 
    user_info_url = "https://smp-api.iyouke.com/dtapi/p/user/userInfo"
    user_info_headers = {
        "Host": "smp-api.iyouke.com",
        "Authorization": authorization,
        "Appid": "wx00796053aa93af0c",
        "Version": "2.9.40",
        "EnvVersion": "release",
        "Xy-Extra-Data": "appid=wx00796053aa93af0c;version=2.9.40;envVersion=release;senceId=1007",
        "Content-Type": "application/json; charset=utf-8",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try:
        user_info_response = requests.get(user_info_url, headers=user_info_headers)
        if user_info_response.status_code == 200:
            user_info = user_info_response.json()
            
        else:
            print(f"{user_info_response.status_code}")
            print(f"{user_info_response.text}")
            return None
    except Exception as e:
        print(f"{e}")
        print(f"{user_info_response.text}") if 'user_info_response' in locals() else print("")
        return None

    # 
    points_url = "https://smp-api.iyouke.com/dtapi/points/user/centerInfo"
    points_headers = {
        "Host": "smp-api.iyouke.com",
        "Authorization": authorization,
        "Appid": "wx00796053aa93af0c",
        "Version": "2.9.40",
        "EnvVersion": "release",
        "Xy-Extra-Data": "appid=wx00796053aa93af0c;version=2.9.40;envVersion=release;senceId=1007",
        "Content-Type": "application/json; charset=utf-8",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try:
        points_response = requests.get(points_url, headers=points_headers)
        if points_response.status_code == 200:
            points_info = points_response.json()
            
        else:
            print(f"{points_response.status_code}")
            print(f"{points_response.text}")
            points_info = None
    except Exception as e:
        print(f"{e}")
        print(f"{points_response.text}") if 'points_response' in locals() else print("")
        points_info = None

    # 
    mobile = user_info.get("userMobile", "")
    nick_name = user_info.get("nickName", "")
    print(f"{mobile}{nick_name}")
    if points_info and points_info.get("success"):
        points_balance = points_info.get("data", {}).get("pointsBalance", 0)
        print(f"{points_balance}")
    else:
        print("")

    return {
        "mobile": mobile,
        "nick_name": nick_name,
        "points_balance": points_info.get("data", {}).get("pointsBalance", "") if points_info else ""
    }


# 
def check_in(authorization):
    current_date = datetime.now().strftime("%Y-%m-%d")
    formatted_date = current_date.replace('-', '%2F')
    url = f"https://smp-api.iyouke.com/dtapi/pointsSign/user/sign?date={formatted_date}"
    headers = {
        "Host": "smp-api.iyouke.com",
        "Authorization": authorization,
        "Appid": "wx00796053aa93af0c",
        "Version": "2.9.40",
        "EnvVersion": "release",
        "Xy-Extra-Data": "appid=wx00796053aa93af0c;version=2.9.40;envVersion=release;senceId=1007",
        "Content-Type": "application/json; charset=utf-8",
        "Referer": "https://servicewechat.com/wx00796053aa93af0c/52/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br"
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            
            return response.json()
        else:
            print(f"{response.status_code}")
            print(f"{response.text}")
            return None
    except Exception as e:
        print(f"{e}")
        print(f"{response.text}") if 'response' in locals() else print("")
        return None


# 
if __name__ == "__main__":
    # 
    get_proclamation()

    #  authorization 
    tokens = os.getenv("KSOEUR", "").split("\n")
    if not tokens or all(not token.strip() for token in tokens):
        print("  KSOEUR ")
        exit(1)

    # 
    for token in tokens:
        token = token.strip()
        if not token:
            continue

        print(f"\n{'=' * 45}")
        print(f"")
        print(f"{'=' * 45}\n")

        account_data = get_account_info_and_points(token)
        if account_data:
            # 
            check_in_result = check_in(token)
            if check_in_result and check_in_result.get("success"):
                print(f"{check_in_result.get('data', {}).get('signReward', 0)}")
            else:
                if check_in_result and check_in_result.get("errorMsg"):
                    print(f"{check_in_result.get('errorMsg')}")
                else:
                    print("")
        else:
            print("")

        print(f"\n{'-' * 45}\n")

    print("")

