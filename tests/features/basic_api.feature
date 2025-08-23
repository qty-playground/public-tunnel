Feature: Basic API Endpoints
  As a client of the Public Tunnel API
  I want to access basic endpoints
  So that I can verify the service is running

  Scenario: Check API root endpoint
    Given the API server is running
    When I call the root endpoint
    Then I should get a running message

  Scenario: Check health endpoint
    Given the API server is running  
    When I call the health endpoint
    Then I should get a healthy status