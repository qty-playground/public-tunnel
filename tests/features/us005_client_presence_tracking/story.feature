Feature: Client Presence Tracking
  As a server
  I want to track client presence through polling
  So that I can maintain accurate client status

  Scenario: Client presence is tracked through polling
    Given a client is polling regularly
    When the client sends polling requests
    Then I should update the client's last_seen timestamp
    And the client should be marked as online