TOGGLE_CAPABILITY = {
    "version": "3",
    "interface": "Alexa.ToggleController",
    "properties": {
        "proactivelyReported": True,
        "retrievable": True,
    },
    "instance": "Blind.BlindState",
    "capabilityResources": {
        "friendlyNames": [
            {"@type": "text", "value": {"text": "tapparella", "locale": "it-IT"},}
        ]
    },
    "semantics": {
        "actionMappings": [
            {
                "@type": "ActionsToDirective",
                "actions": ["Alexa.Actions.Close"],
                "directive": {"name": "TurnOff", "payload": {}},
            },
            {
                "@type": "ActionsToDirective",
                "actions": ["Alexa.Actions.Open"],
                "directive": {"name": "TurnOn", "payload": {}},
            },
        ],
        "stateMappings": [
            {
                "@type": "StatesToValue",
                "states": ["Alexa.States.Closed"],
                "value": "OFF",
            },
            {"@type": "StatesToValue", "states": ["Alexa.States.Open"], "value": "ON",},
        ],
    },
}


RANGE_CAPABILITY = {
    "interface": "Alexa.RangeController",
    "instance": "Blind.Lift",
    "version": "3",
    "properties": {
        "supported": [{"name": "rangeValue"}],
        "proactivelyReported": True,
        "retrievable": True,
    },
    "capabilityResources": {
        "friendlyNames": [
            {"@type": "asset", "value": {"assetId": "Alexa.Setting.Opening"}}
        ]
    },
    "configuration": {
        "supportedRange": {"minimumValue": 0, "maximumValue": 100, "precision": 1},
        "unitOfMeasure": "Alexa.Unit.Percent",
    },
    "semantics": {
        "actionMappings": [
            {
                "@type": "ActionsToDirective",
                "actions": ["Alexa.Actions.Close"],
                "directive": {"name": "SetRangeValue", "payload": {"rangeValue": 0}},
            },
            {
                "@type": "ActionsToDirective",
                "actions": ["Alexa.Actions.Open"],
                "directive": {"name": "SetRangeValue", "payload": {"rangeValue": 100}},
            },
            {
                "@type": "ActionsToDirective",
                "actions": ["Alexa.Actions.Lower"],
                "directive": {
                    "name": "AdjustRangeValue",
                    "payload": {
                        "rangeValueDelta": -10,
                        "rangeValueDeltaDefault": False,
                    },
                },
            },
            {
                "@type": "ActionsToDirective",
                "actions": ["Alexa.Actions.Raise"],
                "directive": {
                    "name": "AdjustRangeValue",
                    "payload": {"rangeValueDelta": 10, "rangeValueDeltaDefault": False},
                },
            },
        ],
        "stateMappings": [
            {"@type": "StatesToValue", "states": ["Alexa.States.Closed"], "value": 0},
            {
                "@type": "StatesToRange",
                "states": ["Alexa.States.Open"],
                "range": {"minimumValue": 1, "maximumValue": 100},
            },
        ],
    },
}

MODE_CAPABILITY = {
    "interface": "Alexa.ModeController",
    "instance": "Blind.Calibrated",
    "proactively_reported": True,
    "retrievable": True,
    "capabilityResources": {
        "friendlyNames": [
            {"@type": "text", "value": {"text": "wash cycle", "locale": "en-US"}},
            {"@type": "text", "value": {"text": "wash setting", "locale": "en-US"}},
        ]
    },
    "configuration": {
        "ordered": False,
        "supportedModes": [
            {
                "value": "Blind.Calibrated",
                "modeResources": {
                    "friendlyNames": [
                        {
                            "@type": "text",
                            "value": {"text": "calibrata", "locale": "it-IT"},
                        }
                    ]
                },
            },
            {
                "value": "Blind.NotCalibrated",
                "modeResources": {
                    "friendlyNames": [
                        {
                            "@type": "text",
                            "value": {"text": "non calibrata", "locale": "it-IT"},
                        }
                    ]
                },
            },
        ],
    },
}
