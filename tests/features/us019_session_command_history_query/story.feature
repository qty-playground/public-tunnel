Feature: US-019 Session Command History Query
    As an AI assistant
    I want to list command history in a session
    So that I can review past operations

    Scenario: Query command history from session with executed commands
        Given commands have been executed in a session
        When I query the command history
        Then I should receive a list of command-ids
        And I should be able to query details for each command

    Scenario: Query command history from empty session
        Given no commands have been executed in a session  
        When I query the command history
        Then I should receive an empty list

    Scenario: Query command details using command-id from history
        Given commands have been executed in a session
        When I query the command history
        And I query details for a specific command-id from the list
        Then I should receive complete command details
        And the details should include execution status and results