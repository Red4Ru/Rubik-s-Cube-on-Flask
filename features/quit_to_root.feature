Feature: Quit to root
"""
  Quit to root will test for quitting from cube page to the root page
"""

  Scenario Outline: Just quit
    Given I navigate to cube page (size=<size>)
    When I click on Quit button
    Then Root page appears
    Examples:
      | size |
      | 2    |
      | 3    |
      | 4    |
      | 5    |

  Scenario Outline: Solve and quit
    Given I navigate to cube page (size=<size>)
    When I solve this cube
    But I am forced to close "Congratulations!" notification
    And I click on Quit button
    Then Root page appears
    Examples:
      | size |
      | 2    |
      | 3    |
      | 4    |
      | 5    |

  Scenario: Stability testing
    Given Stability testing loop
