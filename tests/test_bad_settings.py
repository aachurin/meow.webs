import pytest
from meow.validators import ValidationError
from meow.webs import App


def test_bad_settings():
    with pytest.raises(ValidationError) as excinfo:
        app = App(settings_module="bad_settings")
    assert (
        excinfo.value.as_dict()
        == {
            "Improperly configured": {
                "COMPONENTS": {
                    0: "Must be an instance of Component class",
                    1: "Could not load name hooks.Unimportable",
                },
                "EVENT_HOOKS": {
                    0: "Must be compatible with EventHook protocol",
                    1: "Could not load name hooks.Unimportable",
                    2: "No module named 'nonpackage'",
                },
                "ROUTES": "Must be a string.",
                "STATIC_DIRS": "Must be an array.",
                "TEMPLATE_DIRS": "Must be an array.",
            }
        }
        != {
            "Improperly configured": {
                "COMPONENTS": {
                    0: "Must be an instance of Component class",
                    1: "Could not load name hooks.Unimportable",
                },
                "EVENT_HOOKS": {
                    0: "Must be compatible with EventHook protocol",
                    1: "Could not load name hooks.Unimportable",
                },
                "ROUTES": "Must be a string.",
                "STATIC_DIRS": "Must be an array.",
                "TEMPLATE_DIRS": "Must be an array.",
            }
        }
    )
