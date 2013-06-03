import sys
sys.path.append("/home/hudson/projetos/yakinduparser/parser")

from lettuce import *
from should_dsl import should, should_not
from yakindu_parser import YakinduParser

@before.all
def create_statemachine():
	world.state_machine = YakinduParser('/home/hudson/projetos/yakinduparser/parser/spec/resources/refrigerator.odt')

@step(u'Given the refrigerator door is closed')
def given_the_refrigerator_door_is_closed(step):
    world.state_machine._get_initial_state() |should_not| be_empty
    world.state_machine._get_initial_state() |should| be_greater_than(1)
    world.state_machine._get_initial_state() |should| equal_to([['refrigerator', 'door', 'closed'],
                                                                ['refrigerator', 'door', 'closed']])

@step(u'And the light off is true')
def and_the_light_off_is_true(step):
    world.specification_list = []
    world.specification_list.append(world.state_machine._verify_specification_components())
    world.specification_list[0][0] |should| equal_to(['specification', 'light', 'off', True])

@step(u'And the light on is false')
def and_the_light_on_is_false(step):
    world.specification_list[0][1] |should| equal_to(['specification', 'light', 'on', False])

@step(u'And the thermostat power minimum is true')
def and_the_thermostat_power_minimum_is_true(step):
    world.specification_list[0][2] |should| equal_to(['specification', 'thermostat', 'power', 'minimum', True])

@step(u'And the thermostat power maximum is false')
def and_the_thermostat_power_maximum_is_false(step):
    world.specification_list[0][3] |should| equal_to(['specification', 'thermostat', 'power', 'maximum', False])
    

@step(u'When one opens the door')
def when_one_opens_the_door(step):
    pass #GUI action

@step(u'Then refrigerator door is opened')
def then_refrigerator_door_is_opened(step):
    world.state_machine._get_states_content() |should_not| be_empty()
    world.state_machine._get_states_content() |should| be_greater_than_or_equal_to(2)
    world.state_machine._get_states_content() |should| contain('refrigeratordooropened')

@step(u'And the light on is true')
def and_the_light_on_is_true(step):
    world.specification_list[0][4] |should| equal_to(['specification', 'light', 'on', True])

@step(u'And the light off is false')
def and_the_light_off_is_false(step):
    world.specification_list[0][5] |should| equal_to(['specification', 'light', 'off', False])

    
@step(u'And the thermostat power maximum is true')
def and_the_thermostat_power_maximum_is_true(step):
    world.specification_list[0][6] |should| equal_to(['specification', 'thermostat', 'power', 'maximum', True])

@step(u'And the thermostat power minimum is false')
def and_the_thermostat_power_minimum_is_false(step):
    world.specification_list[0][7] |should| equal_to(['specification', 'thermostat', 'power', 'minimum', False])
