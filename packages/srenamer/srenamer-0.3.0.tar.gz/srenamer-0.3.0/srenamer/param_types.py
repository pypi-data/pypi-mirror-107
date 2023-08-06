import click
import re


class ApiKeyParamType(click.ParamType):
    name = "api-key"

    def convert(self, value, param, ctx):
        found = re.match(r"[0-9a-f]{32}", value)

        if not found:
            self.fail(
                f"{value} is not a 32-character hexadecimal string",
                param,
                ctx,
            )

        return value


class ExtParamType(click.ParamType):
    name = "extension"

    def convert(self, value, param, ctx):
        found = re.match(r"^$|^.[A-Za-z]", value)

        if not found:
            self.fail(
                f"{value} isn't a string that starts with '.' and consist only letters"
            )

        return value
