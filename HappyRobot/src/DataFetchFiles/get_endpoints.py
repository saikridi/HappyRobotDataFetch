from fastapi import HTTPException
from pydantic import BaseModel
import pandas as pd
from .get_max_price_loads import get_optimal_loads, LoadSelectionResponse


class LoadFilterValues(BaseModel):
    """Filter values for the loads"""
    origin_city: str
    destination_city: str
    origin_state: str
    destination_state: str
    max_load_weight: int

class LoadRequest(BaseModel):
    """Request for the loads"""
    filter_values: LoadFilterValues

class LoadDetails(BaseModel):
    """Response for the loads"""
    loads: list
    total_amount: float
    total_weight: int
    total_loads: int

class LoadOptions(BaseModel):
    """Options for the loads"""
    option1: LoadDetails
    option2: LoadDetails

class Response(BaseModel):
    """Response for the loads"""
    user_request: LoadRequest
    response: LoadOptions
    load_details_type: str


"""
Response Framing Functions.
"""
def get_empty_load_response():
    return LoadDetails(loads=[], total_amount=0, total_weight=0, total_loads=0)

def get_single_load_response(loads: pd.DataFrame):
    loads = loads.head(1)
    return LoadDetails(loads=loads.to_dict(orient="records"), 
                       total_amount=loads.loadboard_rate.sum(), 
                       total_weight=loads.weights.sum(), 
                       total_loads=len(loads))

def get_multiple_load_response(loads: LoadSelectionResponse):
    return LoadDetails(loads=loads.selected_loads, 
                       total_amount=loads.total_amount, 
                       total_weight=loads.total_weight, 
                       total_loads=loads.total_loads)

"""
Response functions.
"""
def return_empty_load_response(request: LoadRequest):
    """Return the empty load response"""
    return Response(user_request=request, 
                    response=LoadOptions(option1=get_empty_load_response(),
                                        option2=get_empty_load_response()),
                    load_details_type="empty")

def return_single_load_response(request: LoadRequest, loads: pd.DataFrame):
    """Return the single load response"""
    return Response(user_request=request, 
                    response=LoadOptions(option1=get_single_load_response(loads),
                                        option2=get_empty_load_response()),
                    load_details_type="single")

def return_multiple_load_response(request: LoadRequest, loads1: LoadSelectionResponse, loads2: pd.DataFrame):
    """Return the multiple load response"""
    return Response(user_request=request, 
                    response=LoadOptions(option1=get_multiple_load_response(loads1),
                                        option2=get_single_load_response(loads2)),
                    load_details_type="multiple")

"""
GET Carrier Functions.
"""
async def get_carrier(request: LoadRequest, df: pd.DataFrame):
    """Get the loads"""
    filter_values = request.filter_values
    try:        
        loads = df[(df["origin_city"].str.lower() == filter_values.origin_city.lower()) & 
                    (df["destination_city"].str.lower() == filter_values.destination_city.lower()) & 
                    (df["origin_state"].str.lower() == filter_values.origin_state.lower()) & 
                    (df["destination_state"].str.lower() == filter_values.destination_state.lower()) &
                    (df["weights"] < filter_values.max_load_weight)]

        # Sorting the loads in a descending order by rate
        loads = loads.sort_values(by="loadboard_rate", ascending=False)

        # Early return if no carrier is found
        if loads.empty:
            return return_empty_load_response(request)
           
        # Check for the base cases
        if len(loads) == 1:
            return return_single_load_response(request, loads)
        else:
            optimal_load1= get_optimal_loads(filter_values.max_load_weight, loads)
            optimal_load2= loads.head(1)
            return return_multiple_load_response(request, optimal_load1, optimal_load2)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving carrier: {str(e)}")    