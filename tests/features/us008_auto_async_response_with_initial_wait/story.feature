Feature: Auto Async Response with Initial Wait
  As a server
  I want to wait briefly for command completion before switching to async response
  So that fast commands return immediately while slow commands use polling

  Scenario: Fast command returns immediately within threshold
    Given a command is submitted
    When execution completes within the configured threshold
    Then the result should be returned immediately

  Scenario: Slow command switches to async mode
    Given a command is submitted  
    When execution exceeds the threshold
    Then a command-id should be returned for polling