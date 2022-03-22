import click

from utils.data_types import Response


class StateRepository:
    def __init__(self, env, votes):
        self.responses = []
        for mode, vote in votes:
            click.echo(f"({mode}, {vote})")
            self.responses.append(Response(arm=env.arms[mode], reward=vote))

    def append(self, response: Response):
        self.responses.append(response)
