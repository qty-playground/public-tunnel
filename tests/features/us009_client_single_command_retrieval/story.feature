Feature: Client Single Command Retrieval
  As a client
  I want to receive one command at a time when polling
  So that I can control my execution pace

  Scenario: Client receives exactly one command per polling request
    Given there are multiple commands in my queue
    When I send a polling request
    Then I should receive exactly one command
    And that command should be removed from the queue