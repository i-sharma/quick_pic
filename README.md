# Quick Pic

This repository contains the open source code for an API that fetches the URL of image from [Google Place Photos](https://developers.google.com/places/web-service/photos) efficiently to minimize your API usage. 

#### You need the following for this application to work

- Valid Google [API Key](https://developers.google.com/maps/documentation/javascript/get-api-key)
- [placeId](https://developers.google.com/places/place-id) and [photoref](https://developers.google.com/places/web-service/photos#photo_references) of the place that you want image for
- SQL Database server URL

Once you have the specified items ready, we are good to go.

#### Installation

1. Clone this repository
2. Create a Python3 virtual environment and activate it.
3. Install requirements
``pip install -r requirements.txt ``
4. Set environment variables
    - ###### Windows
        - ```set API_KEY=<YOUR_API_KEY>```
        - ```set DATABASE_URL=<YOUR_DATABASE_URL>```
    - ###### Linux
        - ```export API_KEY=<YOUR_API_KEY>```
        - ```export DATABASE_URL=<YOUR_DATABASE_URL>``` 

#### Usage

The following command will fire up an application server:
```uvicorn app.main:app```

- ##### URL 
    - ```/images/custom```
- ##### Method
    - ```GET```
- ##### URL Params
    - ###### Required
        - ```placeid``` PlaceId of the place that the photo corresponds to
        - ```photoref``` Photo Reference of the photo you want to fetch
    - ###### Optional
        - ```city``` City where the place resides
- ##### Success Response:
```
    {
        "status": "SUCCESS",
        "response": {
            "action_taken": "FOUND",
            "placeid": string,
            "photoref": string,
            "image_url": string,
            "n_requests": integer,
            "city": string
        }
    }
```
- ##### Failure Response:

```
    {
        "status": "FAILURE",
        "response": {
            "message" : ERROR_MESSAGE
        }
    } 
```

- ##### Sample Call
    - ```curl -XGET 'root_url/images/custom?placeid=<PLACEID>&photoref=<PHOTOREF>&city=<CITY>'```