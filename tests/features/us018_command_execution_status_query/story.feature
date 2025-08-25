Feature: US-018 Command Execution Status Query
    As an AI assistant
    I want to query command execution status
    So that I can track progress of long-running tasks

    Scenario: Query pending command status
        Given I have submitted a command that is pending execution
        When I query the command status using command-id
        Then I should receive current execution status
        And I should know that the command is pending

    Scenario: Query running command status
        Given I have a command that is currently running
        When I query the command status using command-id
        Then I should receive current execution status
        And I should know that the command is running

    Scenario: Query completed command status
        Given I have a command that has been completed
        When I query the command status using command-id
        Then I should receive current execution status
        And I should know that the command is completed

    Scenario: Query non-existent command status
        Given I have a non-existent command-id
        When I query the command status using that command-id
        Then I should receive an appropriate error response
        And the error should indicate that the command was not found