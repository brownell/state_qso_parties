'''
Constants to help with processing the Cabrillo format logs. These constants are used to validate the header fields and QSO lines in the logs.
We cannot use the python-cabrillo library because it does not support the fields that are added in the log upload process.
'''
HEADERS = {
    CALLSIGN: AA0AW
    CONTEST: LA-QSO-PARTY
    CATEGORY-POWER: LOW
    CATEGORY-BAND: ALL
    CATEGORY-MODE: MIXED
    CATEGORY-STATION: FIXED
    CATEGORY-OPERATOR: SINGLE-OP
    CATEGORY-ASSISTED: NON-ASSISTED
    CATEGORY-TRANSMITTER: ONE
    CATEGORY-TIME
    CATEGORY-OVERLAY
    EMAIL: aa0aw@arrl.net
    CLUB: Minnesota Wireless Assn
    LOCATION: MN
    CLAIMED-SCORE: 1278
    OPERATORS: AA0AW
    NAME: Douglas Nelson
    ADDRESS: 1411 101st Avenue West
    ADDRESS-CITY: Duluth
    ADDRESS-STATE-PROVINCE: MN
    ADDRESS-POSTALCODE: 55808
    ADDRESS-COUNTRY: USA
    GRID-LOCATOR: EN36VQ
    CREATED-BY: N1MM Logger+ 1.0.11154.0
    SOAPBOX
    X-
}