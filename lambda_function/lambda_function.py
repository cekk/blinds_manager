# -*- coding: utf-8 -*-
from alexa.skills.smarthome import AlexaResponse
from capabilities_settings import MODE_CAPABILITY
from capabilities_settings import RANGE_CAPABILITY
from capabilities_settings import TOGGLE_CAPABILITY

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
            togglecontroller = adr.create_payload_endpoint_capability(
                **TOGGLE_CAPABILITY
            )
            rangecontroller = adr.create_payload_endpoint_capability(**RANGE_CAPABILITY)
            # capability_alexa_modecontroller = adr.create_payload_endpoint_capability(
            #     **MODE_CAPABILITY
            # )

            for blind in res.json():
                adr.add_payload_endpoint(
                    friendly_name=blind.get("name"),
                    endpoint_id=blind.get("id"),
                    description="Remote controlled blind",
                    capabilities=[capability_alexa, rangecontroller],
                    display_categories=["INTERIOR_BLIND"],
                )
            return send_response(adr.get())

    # if namespace == "Alexa.ToggleController":
    #     # Note: This sample always returns a success response for either a request to TurnOff or TurnOn
    #     device_id = request["directive"]["endpoint"]["endpointId"]
    #     action = "close" if name == "TurnOff" else "open"
    #     call_api(
    #         endpoint="roller/{device_id}/{action}".format(
    #             device_id=device_id, action=action
    #         )
    #     )
    #     correlation_token = request["directive"]["header"]["correlationToken"]

    #     apcr = AlexaResponse(correlation_token=correlation_token)
    #     state_value = "OFF" if name == "TurnOff" else "ON"
    #     apcr.add_context_property(
    #         namespace="Alexa.ToggleController", name="toggleState", value=state_value,
    #     )
    #     return send_response(apcr.get())

    if namespace == "Alexa.RangeController":
        # Note: This sample always returns a success response for either a request to TurnOff or TurnOn
        device_id = request["directive"]["endpoint"]["endpointId"]
        if name == 'AdjustRangeValue':
            value = request["directive"]["payload"]["rangeValueDelta"]
        else:
            value = request["directive"]["payload"]["rangeValue"]
        res = call_api(
            endpoint="blind/position",
            method="POST",
            data={"id": device_id, "value": int(value), "type": name},
        )
        print("-- RESPONSE --")
        print(res.json())
        correlation_token = request["directive"]["header"]["correlationToken"]

        # apcr = AlexaResponse(correlation_token=correlation_token)
        # state_value = "OFF" if name == "TurnOff" else "ON"
        # apcr.add_context_property(
        #     namespace="Alexa.RangeController", name="toggleState", value=state_value,
        # )
        # return send_response(apcr.get())


def send_response(response):
    # TODO Validate the response
    print("lambda_handler response -----")
    print(json.dumps(response))
    return response


def call_api(endpoint, method="GET", data={}):
    auth_token = jwt.encode({"identity": skill_id}, token_secret, algorithm="HS256")
    hed = {"Authorization": b"Bearer " + auth_token}
    url = "{api_endpoint}/{endpoint}".format(
        api_endpoint=api_endpoint, endpoint=endpoint
    )
    print("lambda_handler CALL API -----")
    print("URL: {url}".format(url=url))
    if data:
        print("DATA: {data}".format(data=data))
    if method == "GET":
        return requests.get(url, headers=hed)
    else:
        return requests.post(url, headers=hed, data=data)

