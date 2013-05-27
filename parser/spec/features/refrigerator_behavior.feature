Feature: Refrigerator Process Model
  As a Refrigerator
  People open and close the refrigerator's door
  I want to check if the components behavior are the expected
  In order to check the behavior of the refrigerator


  Scenario: The refrigerator door is closed 
    Given the refrigerator door is closed
    And the light off is true
    And the light on is false
    And the thermostat power minimum is true
    And the thermostat power maximum is false
    When one opens the door
    Then refrigerator door is opened
    And the light off is false
    And the light on is true 
    And the thermostat power minimum is false
    And the thermostat power maximum is true

  Scenario: The refrigerator door is opened
    Given the refrigerator door is opened
      And the light off is false
      And the light on is true
      And the thermostat power minimum is false
      And the thermostat power maximum is true
      When one closes the door
      Then refrigerator door is closed
      And the light off is true
      And the light on is false 
      And the thermostat power minimum is true
      And the thermostat power maximum is false