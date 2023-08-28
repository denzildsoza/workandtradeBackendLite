from fyers_apiv3 import fyersModel
from fyers_apiv3.FyersWebsocket import data_ws
from constants import CredentialsConstants,LogpathConstants,ApiConstants

def generateFyersInstance(authCode):
    FyersInstance = fyers = None
    


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

        fyers = data_ws.FyersDataSocket(
            access_token=wsAccessToken,  # Access token in the format "appid:accesstoken"
            log_path=LogpathConstants.fyerslogpath,  # Path to save logs. Leave empty to auto-create logs in the current directory.
            litemode=True,  # Lite mode disabled. Set to True if you want a lite response.
            write_to_file=False,  # Save response in a log file instead of printing it.
            reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
            on_connect=onopen,  # Callback function to subscribe to data upon connection.
            # on_close=onclose,  # Callback function to handle WebSocket connection close events.
            # on_error=onerror,  # Callback function to handle WebSocket errors.
            # on_message=onmessage,  # Callback function to handle incoming messages from the WebSocket.
        )
        fyers.connect()
        return FyersInstance,fyers
    except Exception as error:
        print(error)
        return FyersInstance, fyers
    


if __name__ == "__main__":  
    print(generateFyersInstance())
