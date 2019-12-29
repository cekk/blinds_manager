# -*- coding: utf-8 -*-
from alexa.skills.smarthome import AlexaResponse

import boto3
import json
import jwt
import os
import requests

api_endpoint = os.environ["API_ENDPOINT"]
skill_id = os.environ["SKILL_ID"]
token_secret = os.environ["TOKEN_SECRET"]


def lambda_handler(request, context):

    # Dump the request for logging - check the CloudWatch logs
    print("lambda_handler request  -----")
    print(json.dumps(request))

    if context is not None:
        print("lambda_handler context  -----")
        print(context)

    # Validate we have an Alexa directive
    if "directive" not in request:
        aer = AlexaResponse(
            name="ErrorResponse",
            payload={
                "type": "INVALID_DIRECTIVE",
                "message": "Missing key: directive, Is the request a valid Alexa Directive?",
            },
        )
        return send_response(aer.get())

    # Check the payload version
    payload_version = request["directive"]["header"]["payloadVersion"]
    if payload_version != "3":
        aer = AlexaResponse(
            name="ErrorResponse",
            payload={
                "type": "INTERNAL_ERROR",
                "message": "This skill only supports Smart Home API version 3",
            },
        )
        return send_response(aer.get())

    # Crack open the request and see what is being requested
    name = request["directive"]["header"]["name"]
    namespace = request["directive"]["header"]["namespace"]

    # Handle the incoming request from Alexa based on the namespace

    if namespace == "Alexa.Authorization":
        if name == "AcceptGrant":
            # Note: This sample accepts any grant request
            # In your implementation you would use the code and token to get and store access tokens
            grant_code = request["directive"]["payload"]["grant"]["code"]
            grantee_token = request["directive"]["payload"]["grantee"]["token"]
            aar = AlexaResponse(
                namespace="Alexa.Authorization", name="AcceptGrant.Response"
            )
            return send_response(aar.get())

    if namespace == "Alexa.Discovery":
        if name == "Discover":
            res = call_api(endpoint="blinds")

            adr = AlexaResponse(namespace="Alexa.Discovery", name="Discover.Response")
            capability_alexa = adr.create_payload_endpoint_capability()
            capability_alexa_togglecontroller = adr.create_payload_endpoint_capability(
                interface="Alexa.ToggleController",
                supported=[{"name": "toggleState"}],
                instance="Blind.BlindState",
                capability_resources={
                    "friendlyNames": [
                        {
                            "@type": "text",
                            "value": {"text": "tapparella", "locale": "it-IT"},
                        }
                    ]
                },
                semantics={
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
                        {
                            "@type": "StatesToValue",
                            "states": ["Alexa.States.Open"],
                            "value": "ON",
                        },
                    ],
                },
            )

            for blind in res.json():
                adr.add_payload_endpoint(
                    friendly_name=blind.get("name"),
                    endpoint_id=blind.get("id"),
                    description="Remote controlled blind",
                    capabilities=[capability_alexa, capability_alexa_togglecontroller],
                    display_categories=["INTERIOR_BLIND"],
                )
            return send_response(adr.get())

    if namespace == "Alexa.ToggleController":
        # Note: This sample always returns a success response for either a request to TurnOff or TurnOn
        device_id = request["directive"]["endpoint"]["endpointId"]
        action = "close" if name == "TurnOff" else "open"
        call_api(
            endpoint="roller/{device_id}/{action}".format(
                device_id=device_id, action=action
            )
        )
        correlation_token = request["directive"]["header"]["correlationToken"]

        apcr = AlexaResponse(correlation_token=correlation_token)
        state_value = "OFF" if name == "TurnOff" else "ON"
        apcr.add_context_property(
            namespace="Alexa.ToggleController", name="toggleState", value=state_value,
        )
        return send_response(apcr.get())


def send_response(response):
    # TODO Validate the response
    print("lambda_handler response -----")
    print(json.dumps(response))
    return response


def call_api(endpoint):
    auth_token = jwt.encode({"identity": skill_id}, token_secret, algorithm="HS256")
    hed = {"Authorization": b"Bearer " + auth_token}
    url = "{api_endpoint}/{endpoint}".format(
        api_endpoint=api_endpoint, endpoint=endpoint
    )
    print("lambda_handler CALL API -----")
    print(url)
    requests.get(url, headers=hed)

