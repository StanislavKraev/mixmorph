from mixmorph import Statechart
from mixmorph.conditions import in_


class HardcodeSC(Statechart):
    def __init__(self):
        super().__init__()

        comp_s1 = self.add_statechart('left')
        comp_s2 = self.add_statechart('right')
        comp_s3 = self.add_statechart('center')

        comp_s1.add_state('s1')
        comp_s1.add_state('s2')

        comp_s2.add_state('s3')
        comp_s2.add_state('s4')

        comp_s3.add_state('s5')

        self.add_transition('s1', 'alpha', target='s2')
        self.add_transition('s2', 'beta', target='s1')

        self.add_transition('s3', 'alpha', target='s4')
        self.add_transition('s4', 'beta', target='s3', condition=in_('s2'))

        self.add_transition('s4', 'gamma', target='s5')
        self.add_transition('s5', 'alpha', targets=['s1', 's3'])

        self.initial_state = 's1', 's3'

    def activity_x(self):
        print("activity_x")

    def activity_y(self):
        print("activity_y")
