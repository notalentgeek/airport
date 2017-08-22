import requests, sys, optparse
def callPublicFlightAPI(options):
    url = "https://api.schiphol.nl/public-flights/flights"
    querystring = {"app_id": options.app_id,"app_key": options.app_key}
    headers = {
        'resourceversion': "v3"
    }
    try:
        response = requests.request("GET", url, headers= headers, params=querystring)
    except requests.exceptions.ConnectionError as error:
        print(error)
        sys.exit()
    if response.status_code == 200:
        flightList = response.json()
        print(type(flightList))

        for (key, value) in flightList.items(): print(key)
        #print(flightList["schemaVersion"])
        print(len(flightList["flights"]))

        #print(flightList)
        #print(len(flightList))
        #print("found {} flights.".format(len(flightList["flights"])))
        for flight in flightList["flights"]:
            #print("="*50)
            #print("Found flight with name: {} scheduled on: {} at {}".format(flight["flightName"], flight["scheduleDate"], flight["scheduleTime"]))
            print(flight)
            #print("="*50)
    else:
        print("Oops something went wrong\nHttp response code: {}\n{}".format(response.status_code, response.text))
if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-i", "--app_id", dest="app_id", help="App id used to call the API")
    parser.add_option("-k", "--app_key", dest="app_key", help="App key used to call the API")
    (options,args) = parser.parse_args()
    if options.app_id is None:
        parser.error("Please provide an app id (-i, --app_id)")
    if options.app_key is None:
        parser.error("Please provide an app key (-key, --app_key)")
    #print(options)
    callPublicFlightAPI(options)