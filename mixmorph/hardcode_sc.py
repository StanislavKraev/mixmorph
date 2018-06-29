from mixmorph import Statechart, Transition, Event, State


class HardcodeSC(Statechart):
    def __init__(self):
        states = {'a', 'b', 'c'}
        initial_state = 'b'
        state_transitions = {
            'a': [
                Transition(Event('alpha'), State('b'), self.activity_x),
            ],
            'b': [
                Transition(Event('alpha'), State('a'), self.activity_y),
            ]
        }
        super().__init__(states, initial_state, state_transitions)

    def activity_x(self):
        print("activity_x")

    def activity_y(self):
        print("activity_y")