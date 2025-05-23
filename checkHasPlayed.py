import requests
import json

class AuthError(Exception):
    def __init__(self, exitcode):
        super().__init__(f"Something went wrong with the request, returned exitcode {exitcode}")
        self.exitcode = exitcode

class ResponseError(Exception):
    def __init__(self, quantity):
        super().__init__(f"Requested ID from one username, got {quantity}")
        self.quantity = quantity

def hasPlayed(userId : str) -> bool:
    badgeId = 2124529364

    requestUrl = f"https://badges.roblox.com/v1/users/{userId}/badges/{badgeId}/awarded-date"
    request = requests.get(requestUrl)

    return (request.status_code == 200)

def getFriends(userId : int) -> list[int]:
    """
    Gets player's friends
    ## Parameters\n
      **userId** \n
      `int` UserId of player to get friends list of\n
    ## Returns\n
      **`list[str]`**\n
      List of UserIds in given player
    """
    requestUrl = f"https://friends.roblox.com/v1/users/{userId}/friends/"
    request = requests.get(requestUrl)

    request.raise_for_status()
    
    requestData : dict = json.loads(request.text)

    friendsList = [{"id" : friend["id"], "name" : friend["name"]} for friend in requestData["data"]]
    return friendsList

def usernameToId(username : str) -> str:
    requestUrl = "https://users.roblox.com/v1/usernames/users"
    requestInfo = {
        "usernames" : [username],
        "excludeBannedUsers" : True
    }
    request : requests.Response = requests.post(requestUrl, json=requestInfo)
    responseData : list = json.loads(request.text)["data"]

    if responseData.__len__() != 1:
        raise ResponseError(responseData.__len__())
    
    return str(responseData[0]["id"])

def main():
    userId : str = input("Please provide a userId or username to check who in their friends list has played\n")
    try:
        int(userId)
    except ValueError:
        userId = usernameToId(userId)
        print(f"User ID found: {userId}")

    userHasPlayed = hasPlayed(userId)
    if userHasPlayed:
        print("Requested user has played themselves, getting friends...")
    else:
        print("Requested user has not played, getting friends...")

    friends = getFriends(userId)
    playedList = [user["name"] for user in friends if hasPlayed(user["id"])]

    print(playedList)
    input("Press enter to continue...\n")

if __name__ == "__main__":
    main()
