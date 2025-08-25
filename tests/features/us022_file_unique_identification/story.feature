Feature: File Unique Identification
  As an AI assistant
  I want files identified by unique file-id
  So that I can handle duplicate filenames correctly

  @wip
  Scenario: Multiple files with same name should have unique file-ids
    Given multiple files with the same name "test.txt" are uploaded to a session
    When I query the files in the session
    Then each file should have a unique file-id
    And I should be able to distinguish files by their metadata

  @wip
  Scenario: Files with same name in different sessions should be distinguishable
    Given a file named "data.json" is uploaded to session "session-1"
    And a file named "data.json" is uploaded to session "session-2"
    When I query files from both sessions
    Then each file should have a unique file-id
    And the files should be isolated by session

  @wip
  Scenario: File metadata should allow file identification when names are identical
    Given multiple files with identical names but different content are uploaded
    When I query file metadata
    Then each file should show unique file-id, size, and upload timestamp
    And I should be able to select specific files by their unique characteristics