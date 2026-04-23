# openapi_client.APIInfoApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**api_info_api_get**](APIInfoApi.md#api_info_api_get) | **GET** /api | Api Info


# **api_info_api_get**
> object api_info_api_get()

Api Info

API information endpoint providing available endpoints.

Returns:
    dict: API endpoints and their descriptions

### Example


```python
import openapi_client
from openapi_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = openapi_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with openapi_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = openapi_client.APIInfoApi(api_client)

    try:
        # Api Info
        api_response = api_instance.api_info_api_get()
        print("The response of APIInfoApi->api_info_api_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling APIInfoApi->api_info_api_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

