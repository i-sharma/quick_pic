from fastapi import FastAPI

app = FastAPI()


@app.get("/images/custom")
async def root(placeid : str = '', photoref : str = ''):
    if placeid == '' and photoref == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the fields placeid and photoref are both empty or you may have misspelled the names of query parameters in your request' 
        }
    elif placeid == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the field placeid  is empty or you may have misspelled the name of this field in your request' 
        }
    elif photoref == '':
        return {
            'status': 'INVALID_QUERY',
            'message': 'please check if the field photoref field is empty or you may have misspelled the name of this field in your request' 
        }
    return {
        'status' : 'SUCCESS', 
        'placeid' : placeid,
        'photoref' : photoref
    }