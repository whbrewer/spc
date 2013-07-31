# stakeholders: computational_scientist, scientist

Feature: Build templates
    In order to build web app
    As computational_scientist
    We'll implement some modules

    Scenario: Factorial of 0
        Given I have the number 0
        When I compute its factorial
        Then I see the number 1
