from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws
from constants import CredentialsConstants,LogpathConstants


def generateFyersInstance(authCode):
    FyersInstance = FyersWebsocketInstance = None
    if not authCode:
        return FyersInstance, FyersWebsocketInstance
    # authCode = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkubG9naW4uZnllcnMuaW4iLCJpYXQiOjE2OTI2MzY3MTcsImV4cCI6MTY5MjY2NjcxNywibmJmIjoxNjkyNjM2MTE3LCJhdWQiOiJbXCJ4OjBcIiwgXCJ4OjFcIiwgXCJ4OjJcIiwgXCJkOjFcIiwgXCJkOjJcIiwgXCJ4OjFcIiwgXCJ4OjBcIl0iLCJzdWIiOiJhdXRoX2NvZGUiLCJkaXNwbGF5X25hbWUiOiJYRDA4Njg1Iiwib21zIjoiSzEiLCJoc21fa2V5IjoiYjVkOTdlYTE1YmY5MWRhMzUxOTJmODUzZTNiNWQ2YTEwMGQyYzc2OTEwMTk3MjIyZWVlZjY5ZjIiLCJub25jZSI6IiIsImFwcF9pZCI6IjNIMDIxT1E4WkkiLCJ1dWlkIjoiODc2ZTQ4ZGRmMzUyNGExYTg5MmMyOTZiNjZhNGQwMzkiLCJpcEFkZHIiOiIwLjAuMC4wIiwic2NvcGUiOiIifQ.h4XtU3gfWLuR0xrG1v_c_jR0Q48puRU_8otgZzx4lSQ"
    try:
        session = fyersModel.SessionModel(
            client_id=CredentialsConstants.clientId,
            secret_key=CredentialsConstants.secretKey,
            redirect_uri=CredentialsConstants.redirectUrl,
            grant_type=CredentialsConstants.grantType,
            response_type=CredentialsConstants.code,
            state=CredentialsConstants.state,
        )
        response = session.generate_authcode()
        session.set_token(authCode)
        response = session.generate_token()
        accessToken = response["access_token"]
        print(accessToken)
        wsAccessToken = f"{CredentialsConstants.clientId}:{accessToken}"
        FyersInstance = fyersModel.FyersModel(
            client_id=CredentialsConstants.clientId, token=accessToken, log_path=LogpathConstants.fyerslogpath
        )
        FyersWebsocketInstance = data_ws.FyersDataSocket(
            access_token=wsAccessToken,  # Access token in the format "appid:accesstoken"
            log_path=LogpathConstants.fyerslogpath,  # Path to save logs. Leave empty to auto-create logs in the current directory.
            litemode=True,  # Lite mode disabled. Set to True if you want a lite response.
            write_to_file=False,  # Save response in a log file instead of printing it.
            reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
            # on_connect=onopen,  # Callback function to subscribe to data upon connection.
            # on_close=onclose,  # Callback function to handle WebSocket connection close events.
            # on_error=onerror,  # Callback function to handle WebSocket errors.
            # on_message=onmessage,  # Callback function to handle incoming messages from the WebSocket.
        )
        return FyersInstance, FyersWebsocketInstance
    except Exception as error:
        print(error)
        return FyersInstance, FyersWebsocketInstance
    


if __name__ == "__main__":  
    print(generateFyersInstance())
