from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws
from constants import CredentialsConstants,LogpathConstants,ApiConstants

def generateFyersInstance(authCode):
    FyersInstance = fyers = None
    print(authCode)


    def onerror(message):
        """
        Callback function to handle WebSocket errors.

        Parameters:
            message (dict): The error message received from the WebSocket.


        """
        print("Error:", message)


    def onclose(message):
        """
        Callback function to handle WebSocket connection close events.
        """
        print("Connection closed:", message)


    def onopen():
        """
        Callback function to subscribe to data type and symbols upon WebSocket connection.

        """
        print('opened')
        # Specify the data type and symbols you want to subscribe to
        data_type = "SymbolUpdate"

        # Subscribe to the specified symbols and data type
        symbols = ApiConstants.IndexSymbolsList
        fyers.subscribe(symbols=symbols, data_type=data_type)

        # Keep the socket running to receive real-time data
        fyers.keep_running()

    if not authCode:
        return FyersInstance, fyers
    try:
    #     session = fyersModel.SessionModel(
    #         client_id=CredentialsConstants.clientId,
    #         secret_key=CredentialsConstants.secretKey,
    #         redirect_uri=CredentialsConstants.redirectUrl,
    #         grant_type=CredentialsConstants.grantType,
    #         response_type=CredentialsConstants.code,
    #         state=CredentialsConstants.state,
    #     )
    #     response = session.generate_authcode()
    #     session.set_token(authCode)
    #     response = session.generate_token()
    #     # accessToken = response["access_token"]
        accessToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJhcGkuZnllcnMuaW4iLCJpYXQiOjE2OTMyMzg4MzIsImV4cCI6MTY5MzI2OTAxMiwibmJmIjoxNjkzMjM4ODMyLCJhdWQiOlsieDowIiwieDoxIiwieDoyIiwiZDoxIiwiZDoyIiwieDoxIiwieDowIl0sInN1YiI6ImFjY2Vzc190b2tlbiIsImF0X2hhc2giOiJnQUFBQUFCazdNWXdvOU5UbDlra1R0S1BzZDdIdTJaS1JTSlNXRVRfcDRHWXJrcmtrd3dtXzNac1l2WkFLcG1RWUpDd1liQ0hRTWxfQy05S2szQ2NNM2hzTnI0YlNpZXU5NWVFRnpfa2tJRXpqaWRzX3ZWYTNpVT0iLCJkaXNwbGF5X25hbWUiOiJERU5aSUwgRFNPVVpBIiwib21zIjoiSzEiLCJoc21fa2V5IjoiYjVkOTdlYTE1YmY5MWRhMzUxOTJmODUzZTNiNWQ2YTEwMGQyYzc2OTEwMTk3MjIyZWVlZjY5ZjIiLCJmeV9pZCI6IlhEMDg2ODUiLCJhcHBUeXBlIjoxMDAsInBvYV9mbGFnIjoiTiJ9.a6n-CDNMuULq6SBZch47sxmx1QulkR4rBA0il1NHZcY"
        print(accessToken)
        wsAccessToken = f"{CredentialsConstants.clientId}:{accessToken}"
        FyersInstance = fyersModel.FyersModel(
            client_id=CredentialsConstants.clientId, token=accessToken, log_path=LogpathConstants.fyerslogpath
        )

        return FyersInstance,wsAccessToken
    except Exception as error:
        print(error)
        return FyersInstance, fyers
    


if __name__ == "__main__":  
    print(generateFyersInstance())
