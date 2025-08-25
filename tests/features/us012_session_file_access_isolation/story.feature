Feature: Session File Access Isolation
  As a user
  I want file access restricted to my session
  So that data privacy is maintained

  Scenario: Users can only access files within their session
    Given files are uploaded to a session
    When users try to access files
    Then only users within the same session should have access
    And cross-session file access should be denied