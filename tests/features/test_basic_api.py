"""Step definitions for basic API feature tests"""

import pytest
from pytest_bdd import scenarios, given, when, then
from conftest import BDDPhase


# Load scenarios from feature file
scenarios('basic_api.feature')


@given('the API server is running')
def api_server_running(context):
    """The TestClient automatically handles server lifecycle"""
    # Server is automatically running via TestClient
    # No additional setup needed
    pass


@when('I call the root endpoint')
def call_root_endpoint(context):
    """Call the API root endpoint"""
    context.phase = BDDPhase.WHEN
    context.response = context.test_client.get("/")


@when('I call the health endpoint')
def call_health_endpoint(context):
    """Call the API health endpoint"""
    context.phase = BDDPhase.WHEN
    context.response = context.test_client.get("/health")


@then('I should get a running message')
def verify_running_message(context):
    """Verify the root endpoint returns running message"""
    context.phase = BDDPhase.THEN
    assert context.response.status_code == 200
    assert context.response.json() == {"message": "Public Tunnel API is running"}


@then('I should get a healthy status')
def verify_healthy_status(context):
    """Verify the health endpoint returns healthy status"""
    context.phase = BDDPhase.THEN
    assert context.response.status_code == 200
    assert context.response.json() == {"status": "healthy"}