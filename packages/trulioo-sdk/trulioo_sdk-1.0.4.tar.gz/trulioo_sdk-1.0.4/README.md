# Trulioo Python SDK

- Package version: 1.0.4
- API version: v1
- Build package: org.openapitools.codegen.languages.PythonClientCodegen

## Installation & Usage

Python 3.6 or later is required.

### With [pip](https://pip.pypa.io/en/stable/)

```shell
pip install trulioo_sdk
```

### With [Setuptools](http://pypi.python.org/pypi/setuptools)

In the root of this SDK, run:

```shell
python setup.py install --user
```

## Sample Application

Check out our sample application for this SDK in the
[sample-app](https://github.com/Trulioo/sdk-python/tree/1.0.4/sample-app) folder.


## Getting Started

### Example of testing authentication

```python
from trulioo_sdk import Configuration, ApiException
from trulioo_sdk.apis import ConnectionApi

config = Configuration()

# Configure API key authorization
config.api_key["ApiKeyAuth"] = "YOUR-X-TRULIOO-API-KEY"

# Configure mode: "trial" or "live"
mode = "trial"

# Construct instance of ApiClient with config
api_client = ApiClient(config)

# Construct instance of ConnectionApi with api_client
connectionApi = ConnectionApi(api_client)

# Call ConnectionApi#test_authentication
try:
    result = connectionApi.test_authentication(mode)
    print(result)
except ApiException as e:
    print("Exception when calling ConnectionApi#testAuthentication\n")
    print("Status code:      " + str(e.status))
    print("Reason:           " + str(e.body))
    print("Response headers: " + str(e.headers))
```

## Testing

This project uses [tox](https://tox.readthedocs.io/en/latest/) for consistent testing. Install with `pip install tox`,
then run:

```bash
python -m tox
```

## Documentation for APIs

All URIs are relative to *https://gateway.trulioo.com*.

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*BusinessApi* | [**get_business_search_result**](docs/BusinessApi.md#get_business_search_result) | **GET** /{mode}/business/v1/search/transactionrecord/{id} | Get Business Search Result
*BusinessApi* | [**search**](docs/BusinessApi.md#search) | **POST** /{mode}/business/v1/search | Search
*ConfigurationApi* | [**get_business_registration_numbers**](docs/ConfigurationApi.md#get_business_registration_numbers) | **GET** /{mode}/configuration/v1/businessregistrationnumbers/{countryCode}/{jurisdictionCode} | Get Business Registration Numbers
*ConfigurationApi* | [**get_consents**](docs/ConfigurationApi.md#get_consents) | **GET** /{mode}/configuration/v1/consents/{configurationName}/{countryCode} | Get Consents
*ConfigurationApi* | [**get_country_codes**](docs/ConfigurationApi.md#get_country_codes) | **GET** /{mode}/configuration/v1/countrycodes/{configurationName} | Get Country Codes
*ConfigurationApi* | [**get_country_subdivisions**](docs/ConfigurationApi.md#get_country_subdivisions) | **GET** /{mode}/configuration/v1/countrysubdivisions/{countryCode} | Get Country Subdivisions
*ConfigurationApi* | [**get_datasources**](docs/ConfigurationApi.md#get_datasources) | **GET** /{mode}/configuration/v1/datasources/{configurationName}/{countryCode} | Get Datasources
*ConfigurationApi* | [**get_detailed_consents**](docs/ConfigurationApi.md#get_detailed_consents) | **GET** /{mode}/configuration/v1/detailedConsents/{configurationName}/{countryCode} | Get Detailed Consents
*ConfigurationApi* | [**get_document_types**](docs/ConfigurationApi.md#get_document_types) | **GET** /{mode}/configuration/v1/documentTypes/{countryCode} | Get Document Types
*ConfigurationApi* | [**get_fields**](docs/ConfigurationApi.md#get_fields) | **GET** /{mode}/configuration/v1/fields/{configurationName}/{countryCode} | Get Fields
*ConfigurationApi* | [**get_recommended_fields**](docs/ConfigurationApi.md#get_recommended_fields) | **GET** /{mode}/configuration/v1/recommendedfields/{configurationName}/{countryCode} | Get Recommended Fields
*ConfigurationApi* | [**get_test_entities**](docs/ConfigurationApi.md#get_test_entities) | **GET** /{mode}/configuration/v1/testentities/{configurationName}/{countryCode} | Get Test Entities
*ConnectionApi* | [**connection_async_callback_url**](docs/ConnectionApi.md#connection_async_callback_url) | **POST** /{mode}/connection/v1/async-callback | Connection Async Callback Url
*ConnectionApi* | [**say_hello**](docs/ConnectionApi.md#say_hello) | **GET** /{mode}/connection/v1/sayhello/{name} | Say Hello
*ConnectionApi* | [**test_authentication**](docs/ConnectionApi.md#test_authentication) | **GET** /{mode}/connection/v1/testauthentication | Test Authentication
*VerificationsApi* | [**document_download**](docs/VerificationsApi.md#document_download) | **GET** /{mode}/verifications/v1/documentdownload/{transactionRecordId}/{fieldName} | Document Download
*VerificationsApi* | [**get_transaction_record**](docs/VerificationsApi.md#get_transaction_record) | **GET** /{mode}/verifications/v1/transactionrecord/{id} | Get Transaction Record
*VerificationsApi* | [**get_transaction_record_address**](docs/VerificationsApi.md#get_transaction_record_address) | **GET** /{mode}/verifications/v1/transactionrecord/{id}/withaddress | Get Transaction Record Address
*VerificationsApi* | [**get_transaction_record_document**](docs/VerificationsApi.md#get_transaction_record_document) | **GET** /{mode}/verifications/v1/transactionrecord/{transactionRecordID}/{documentField} | Get Transaction Record Document
*VerificationsApi* | [**get_transaction_record_verbose**](docs/VerificationsApi.md#get_transaction_record_verbose) | **GET** /{mode}/verifications/v1/transactionrecord/{id}/verbose | Get Transaction Record Verbose
*VerificationsApi* | [**get_transaction_status**](docs/VerificationsApi.md#get_transaction_status) | **GET** /{mode}/verifications/v1/transaction/{id}/status | Get Transaction Status
*VerificationsApi* | [**verify**](docs/VerificationsApi.md#verify) | **POST** /{mode}/verifications/v1/verify | Verify

## Documentation For Models

 - [Address](docs/Address.md)
 - [AppendedField](docs/AppendedField.md)
 - [Business](docs/Business.md)
 - [BusinessRecord](docs/BusinessRecord.md)
 - [BusinessRegistrationNumber](docs/BusinessRegistrationNumber.md)
 - [BusinessRegistrationNumberMask](docs/BusinessRegistrationNumberMask.md)
 - [BusinessResult](docs/BusinessResult.md)
 - [BusinessSearchRequest](docs/BusinessSearchRequest.md)
 - [BusinessSearchRequestBusinessSearchModel](docs/BusinessSearchRequestBusinessSearchModel.md)
 - [BusinessSearchResponse](docs/BusinessSearchResponse.md)
 - [BusinessSearchResponseIndustryCode](docs/BusinessSearchResponseIndustryCode.md)
 - [Communication](docs/Communication.md)
 - [Consent](docs/Consent.md)
 - [CountrySubdivision](docs/CountrySubdivision.md)
 - [DataField](docs/DataField.md)
 - [DataFields](docs/DataFields.md)
 - [DatasourceField](docs/DatasourceField.md)
 - [DatasourceResult](docs/DatasourceResult.md)
 - [Document](docs/Document.md)
 - [DriverLicence](docs/DriverLicence.md)
 - [Location](docs/Location.md)
 - [LocationAdditionalFields](docs/LocationAdditionalFields.md)
 - [NationalId](docs/NationalId.md)
 - [NormalizedDatasourceField](docs/NormalizedDatasourceField.md)
 - [NormalizedDatasourceGroupCountry](docs/NormalizedDatasourceGroupCountry.md)
 - [Passport](docs/Passport.md)
 - [PersonInfo](docs/PersonInfo.md)
 - [PersonInfoAdditionalFields](docs/PersonInfoAdditionalFields.md)
 - [Record](docs/Record.md)
 - [RecordRule](docs/RecordRule.md)
 - [Result](docs/Result.md)
 - [ServiceError](docs/ServiceError.md)
 - [TestEntityDataFields](docs/TestEntityDataFields.md)
 - [TransactionRecordResult](docs/TransactionRecordResult.md)
 - [TransactionRecordResultAllOf](docs/TransactionRecordResultAllOf.md)
 - [TransactionStatus](docs/TransactionStatus.md)
 - [VerifyRequest](docs/VerifyRequest.md)
 - [VerifyResult](docs/VerifyResult.md)

## Documentation For Authorization

## ApiKeyAuth

- **Type**: API key
- **API key parameter name**: x-trulioo-api-key
- **Location**: HTTP header
