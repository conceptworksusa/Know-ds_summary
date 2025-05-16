template = """
    Demographics Info : 
    The patient's date of birth is {PatientDateOfBirth}. The gender is {PatientGender}.
    The permanent address is {PatientAddress}, located in the city of {PatientCity},
    in the state of {PatientState}, with the ZIP code {50265}. The patient control number is {PatientControlNumber}.
    The service began on {ServiceDateFrom} and ended on {ServiceDateThrough}. The facility is {Facility},
    located at {FacilityAddress} in {FacilityCity}, {FacilityState}, with the ZIP code {FacilityZip}.
    The NPI is {NPI} and the tax ID is {TaxID}. The representative's name is {RepresentativeName}, representing the title {RepresentativeTitle} and 
    email {RepresentativeEmail}. The account number is {AccountNumber} and the medical record number is {MedicalRecordNumber}.
    The patient's first name is {PatientFirstName} and last name is {PatientLastName}. The full name is {PatientNameFirstLast} and the last first name is {PatientNameLastFirst}.
    """


d = """
The bill date is March 31,
2025. The subscriber's first name is Tamera and last name is Washington.
Remit Claim details: The guarantor's first name is null, last name is null,
address is null, city is null, state is null, ZIP code is null, phone is null, fax is null."""


data = {"DemographicsInfo": {
    "PatientDateOfBirth": "1963-03-31T00:00:00",
    "PatientGender": "F",
    "PatientAddress": "APT 1",
    "PatientCity": "WEST DES MOINES",
    "PatientState": "IA",
    "PatientZip": "50265",
    "PatientControlNumber": "42029493306",
    "ServiceDateFrom": "2024-07-07T00:00:00",
    "ServiceDateThrough": "2024-07-07T00:00:00",
    "Facility": "IMMC-METHODIST WEST",
    "FacilityAddress": "1660 60TH STREET",
    "NPI": "1598905762",
    "TaxID": "420680452",
    "RepresentativeName": null,
    "RepresentativeTitle": null,
    "RepresentativeEmail": null,
    "AccountNumber": "420294933",
    "MedicalRecordNumber": null,
    "PatientFirstName": "Tamera",
    "PatientLastName": "Washington",
    "PatientNameFirstLast": "Tamera Washington",
    "PatientNameLastFirst": "Washington, Tamera",
    "BillDate": "2025-03-31",
    "ClaimControlNumber": null,
    "FacilityCity": "WEST DES MOINES",
    "FacilityState": "IA",
    "FacilityZip": "502667700",
    "FacilityCityStateZip": "WEST DES MOINES, IA 502667700",
    "FacilityPhone": null,
    "GuarantorFirstName": null,
    "GuarantorLastName": null,
    "GuarantorAddress": null,
    "GuarantorCity": null,
    "GuarantorState": null,
    "GuarantorZip": null,
    "AttentionTo": null,
    "PayerName": "OSCAR MERCY ONE OON",
    "PayerAddress1": "PO BOX 843151",
    "PayerAddress2": null,
    "PayerCity": "KANSAS CITY",
    "PayerState": "MO",
    "PayerZip": "641843151",
    "PayerPhone": null,
    "PayerFax": null,
    "SubscriberFirstName": "TAMERA",
    "SubscriberLastName": "WASHINGTON",
    "SubscriberId": "OSC77523075",
    "SubscriberDateOfBirth": "1963-03-31T00:00:00",
    "SubscriberGroupName": "OSCAR MERCY ONE OON",
    "SubscriberGroupNumber": null
  }}
