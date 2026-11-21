# source: https://github.com/ohjelmistotuotanto-jyu/tehtavat
# Use with RobotFramework


class StubIO:
    def __init__(self, inputs=None):
        self.inputs = inputs or []
        self.outputs = []

    def write(self, value):
        self.outputs.append(value)

    def read(self, _prompt):
        if self.inputs:
            return self.inputs.pop(0)
        return ""

    def add_input(self, value):
        self.inputs.append(value)
