from pytest_bdd import scenarios

from .given_commands_have_been_executed_in_a_session import *
from .given_no_commands_have_been_executed_in_a_session import *
from .when_i_query_the_command_history import *
from .when_i_query_details_for_a_specific_command_id_from_the_list import *
from .then_i_should_receive_a_list_of_command_ids import *
from .then_i_should_receive_an_empty_list import *
from .then_i_should_be_able_to_query_details_for_each_command import *
from .then_i_should_receive_complete_command_details import *
from .then_the_details_should_include_execution_status_and_results import *

scenarios("story.feature")