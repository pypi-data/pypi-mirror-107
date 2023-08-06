from pioreactor.background_jobs.subjobs.dosing_automation import DosingAutomationContrib
from pioreactor.config import config



__all__ = ['MyCustomDosingAutomation']


# the class doesn't need to be in __init__, but your __init__ should reference the class, typically
# by importing it into the __init__. This is needed so the class is "registered" with pioreactor codebase.
class MyCustomDosingAutomation(DosingAutomationContrib):
    """
    This is just an example class of a dosing automation - it doesn't do anything but print.

    On the RPi's command line, you can invoke this class using

    $ pio run dosing_control --dosing-automation my_custom_dosing_automation --volume 1.0

    And if installed correctly, you'll find this also in the Pioreactor web UI.
    """

    key = "my_custom_dosing_automation"

    def __init__(self, volume):
        self.volume = volume

    def execute(self):
        print(f"I'm executing {self.volume} now...")
        print(f"This config value is set in additional_config.ini: {config['custom_dosing']['test_value']}")


