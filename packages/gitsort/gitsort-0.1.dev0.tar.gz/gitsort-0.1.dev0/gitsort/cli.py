import click
from click_aliases import ClickAliasedGroup
from gettext import ngettext


class AliasChoice(click.ParamType):
    name = "choice"
    """
    A choice which support aliases.
    
    Aliases are specified by the '|' character and the default is the first.
    For example:
        type=AliasChoice(["ASC|ASCENDING|A"])
    This means that 'ASCENDING' and 'A' is an alias for 'ASC' and typing either will
    return 'ASC'.
    """
    def __init__(self, choices, case_sensitive=True):
        self.choices = choices
        self.case_sensitive = case_sensitive

    def convert(self, value, param, ctx):
        # Match through normalization and case sensitivity
        # first do token_normalize_func, then lowercase
        # preserve original `value` to produce an accurate message in
        # `self.fail`
        normed_value = value
        normed_choices = {}
        for choice in self.choices:
            aliases = choice.split("|")
            for alias in aliases:
                normed_choices[alias] = aliases[0]

        if ctx is not None and ctx.token_normalize_func is not None:
            normed_value = ctx.token_normalize_func(value)
            normed_choices = {
                ctx.token_normalize_func(normed_choice): original
                for normed_choice, original in normed_choices.items()
            }

        if not self.case_sensitive:
            normed_value = normed_value.casefold()
            normed_choices = {
                normed_choice.casefold(): original
                for normed_choice, original in normed_choices.items()
            }

        if normed_value in normed_choices:
            return normed_choices[normed_value]

        choices_str_list = []
        for choice in self.choices:
            aliases = choice.split("|")
            if len(aliases) > 1:
                choices_str_list.append(
                    aliases[0] + f" ({','.join(aliases[1:])})"
                )
            else:
                choices_str_list.append(aliases[0])
        choices_str = ", ".join(map(repr, choices_str_list))
        self.fail(
            ngettext(
                "{value!r} is not {choice}.",
                "{value!r} is not one of {choices}.",
                len(self.choices),
            ).format(value=value, choice=choices_str, choices=choices_str),
            param,
            ctx,
        )


issue_sort = click.option(
    "-s", "--sort", type=AliasChoice(
        ["COMMENTS|COMMENT|C", "CREATED_AT|CREATED", "UPDATED_AT|UPDATED|U"], case_sensitive=False
    ),
    default="COMMENTS", show_default=True,
    help="""Sort order of repositories. Sort methods include:

    \b
    * Name       - Sort by name
    * Stars      - Sort by star count
    * Pushed at  - Sort by push count
    * Updated at - Sort by update time
    * Created at - Sort by creation time
    """
)


repository_sort = click.option(
    "-s", "--sort", type=AliasChoice([
        "NAME|N", "PUSHED_AT|PUSHED|P", "UPDATED_AT|UPDATED|U", "CREATED_AT|CREATED|C",
        "STARGAZERS|STARS|STAR|S"
    ], case_sensitive=False),
    default="STARGAZERS", show_default=True,
    help="""Sort order of repositories. Sort methods include:
    
    \b
    * Name       - Sort by name
    * Stars      - Sort by star count
    * Pushed at  - Sort by push count
    * Updated at - Sort by update time
    * Created at - Sort by creation time
    """
)


url = click.argument(
    "url", type=click.STRING, required=True, metavar="URL_OR_REPO_PATH",
)


@click.group(cls=ClickAliasedGroup)
@click.option(
    "--per-page", "-p", type=click.INT, default=10, show_default=True,
    help="Number of items to be displayed in the table."
)
@click.option(
    "-f", "--first", type=click.INT, default=30, show_default=True,
    help="Retrieve the first number of elements of query. Decrease this number if the request times out."
)
@click.option(
    "-o", "--order", type=AliasChoice(["ASC|ASCENDING|A", "DESC|DESCENDING|D"], case_sensitive=False), default="DESC",
    show_default=True,
    help="The direction of ordering"
)
@click.option(
    "-F", "--field", type=click.STRING, default=None, show_default=True,
    help="Any additional connections, for example `after: <cursor>`"
)
@click.pass_context
def cli(ctx, **kwargs) -> None:
    """
    Sort various Github things
    """
    ctx.obj = kwargs

def development():
    print("In development")


@cli.command(aliases=["fork", "f"])
@url
@repository_sort
@click.pass_obj
def forks(obj, **kwargs):
    """Sort each fork of a repository."""
    options = {**obj, **kwargs}
    print(options)


@cli.command(aliases=["issue", "i"])
@url
@issue_sort
@click.pass_obj
def issues(obj, **kwargs):
    """Sort issues of a repository"""
    options = {**obj, **kwargs}
    print(options)


@cli.command(aliases=["pr", "p"])
@url
@issue_sort
@click.pass_obj
def pull_requests(obj, **kwargs):
    """Sort pull requests of a repository"""
    options = {**obj, **kwargs}
    print(options)


@cli.command(aliases=["repos", "repo", "r"])
@url
@repository_sort
@click.pass_obj
def repositories(obj, **kwargs):
    """Sort repositories of an user or organization"""
    options = {**obj, **kwargs}
    print(options)


@cli.command(aliases=["set-token", "t"])
@click.argument("token")
def token(token, **kwargs):
    """
    Set your Github personal access token in order to access
    private repositories and extend the usage of the GraphQL API.
    """
    import os
    from dotenv import load_dotenv
    from os.path import join, dirname

    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    gitsort_token = os.environ.get("GITSORT_TOKEN")
    if not gitsort_token:
        with open(dotenv_path, "w") as f:
            f.write(f"GITSORT_TOKEN={token}")
        print("Github Token set!")
    else:
        inp = input("Github token already set! Do you want to update it? [y/n] ").lower()
        while inp not in ["y", "n"]:
            print("Invalid answer")
            inp = input("Github token already set! Do you want to update it? [y/n] ").lower()
        if inp == "y":
            with open(dotenv_path, "w") as f:
                f.write(f"GITSORT_TOKEN={token}")
            print("Github Token updated!")
