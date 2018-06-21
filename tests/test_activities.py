from mixmorph import Event


def test_should_call_activity_when_event_received(activities_statechart, sc_processor):

    with rabbitmq_actor:
        msg_data = {"type": [{"name":"acoustic", "instrument": [{"name": "GUITAR"}, {"name":"VIOLIN"}]}]}

        sc_processor.on(Event(event_id='alpha'))
        rabbitmq_actor.assert_called_with(queue='default', kwargs=msg_data)
