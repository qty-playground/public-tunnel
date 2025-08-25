Feature: AI File Upload Feature
  As an AI assistant
  I want to upload files to session
  So that clients can access shared resources

  Scenario: AI assistant uploads file to session
    Given I have a file to share
    When I upload the file to a session
    Then the file should be stored with unique file-id
    And clients in the session should be able to download it