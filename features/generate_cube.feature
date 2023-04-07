Feature: Generate Cube
"""
  Generate Cube will test for generating cubes from root page
"""

  Scenario Outline: Success test for generating cube with size <size>
    Given I navigate to root page
    When I choose size <size>
    And I enter valid seed
    And I click on Start button
    Then Cube with size <size> is generated
    Examples:
      | size |
      | 2    |
      | 3    |
      | 4    |
      | 5    |

  Scenario Outline: Failure test for generating  cube with size <size>
    Given I navigate to root page
    When I choose size <size>
    And I enter seed "<seed>"
    And I click on Start button
    Then Error message is generated
    Examples: Too short seed
      | size | seed    |
      | 2    | seed123 |
      | 3    | seed123 |
      | 4    | seed123 |
      | 5    | seed123 |
    Examples: Too long seed
      | size | seed      |
      | 2    | seed12345 |
      | 3    | seed12345 |
      | 4    | seed12345 |
      | 5    | seed12345 |
    Examples: Seed have valid length but have invalid symbol
      | size | seed     |
      | 2    | seed!234 |
      | 3    | seed!234 |
      | 4    | seed!234 |
      | 5    | seed!234 |
