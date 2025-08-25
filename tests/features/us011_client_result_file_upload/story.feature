Feature: Client Result File Upload
  As a client
  I want to upload result files with metadata
  So that AI can identify and download relevant files

  Scenario: Client uploads execution result files with metadata
    Given I have execution results to share
    When I upload files as part of result reporting
    Then each file should have file-id, filename, and summary
    And the AI should be able to browse and download selectively