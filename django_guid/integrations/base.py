from django.core.exceptions import ImproperlyConfigured


class Integration(object):
    """
    Integration base class.
    """

    identifier = None  # The name of your integration

    def __init__(self) -> None:
        if self.identifier is None:
            raise ImproperlyConfigured('`identifier` cannot be None')

    def validate(self) -> None:
        """
        Holds validation logic to be run when Django starts.
        """
        pass

    def setup(self) -> None:
        """
        Holds setup logic to be run once when the middleware is initialized.
        """
        pass

    def run(self, guid: str, **kwargs) -> None:
        """
        Code here is executed in the middleware, before the view is called.
        """
        raise ImproperlyConfigured(f'The integration `{self.identifier}` is missing a `run` method')

    def cleanup(self, **kwargs) -> None:
        """
        Code here is executed in the middleware, after the view is called.
        """
        pass
