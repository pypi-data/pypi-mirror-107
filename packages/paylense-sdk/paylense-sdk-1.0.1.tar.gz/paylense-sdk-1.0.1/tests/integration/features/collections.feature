Feature: Collections
    Scenario: Request a payment from a consumer (Payer)
        Given I have a valid APP-ID, username and password
        When I request for a payment with the following payment details
            | note         | amount | message | mobile     |
            | test payment | 600    | message | 0782631873 |

        And  I check for transaction Status
        Then It should be successful

    Scenario: Failed Transfer
        Given I have a valid APP-ID, username and password
        When I enter the following payment details
            | note         | amount | message | mobile     |
            | test payment | 600    | message | 0782631873 |

        And  I check for transaction Status
        Then It should be successful

    Scenario: Non Mtn | Airtel mobile
        Given I have a valid APP-ID, username and password
        When I enter the following payment details
            | note         | amount | message | mobile     |
            | test payment | 600    | message | 0782631873 |

        And  I check for transaction Status
        Then It should be successful




