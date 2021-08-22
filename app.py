
########################################################################################################################
#
#   CHAINLINK RELAY APP - EXTERNAL INITIATOR & ADAPTOR
#
########################################################################################################################


# =======================================================================================================================
#   IMPORT STATEMENTS AND ENVIRONMENT INITIALIZATION
# =======================================================================================================================


from flask import Flask, Response, request, jsonify
from modules.config_loader import *
import modules.jobs as _jobs
import modules.external_adaptor as external_adaptor
import modules.external_initiator as external_initiator

(
    CHAINLINK_ACCESS_KEY,
    CHAINLINK_ACCESS_SECRET,
    CHAINLINK_IP
) = get_env("config.json")

app = Flask(__name__)


# ======================================================================================================================
#   APPLICATION ROUTES - ENDPOINTS REQUIRED BY CHAINLINK NODE
# ======================================================================================================================


@app.route("/", methods=["GET"])
def check():
    """
    Health check endpoint.
    """

    return Response(status=200)


@app.route("/jobs", methods=["POST"])
def jobs():
    """
    Called by Chainlink node when a job is created using this app's external initiator
    """

    req = request.get_json()
    _jobs.add_job(req["jobId"])
    return Response(status=200)


@app.route("/temp", methods=["GET"])
def temp():
    """
    Called by Chainlink node while running a job
    """

    return jsonify({"temp": 42})


# =======================================================================================================================
#   APPLICATION ROUTES - ENDPOINTS FOR REQUESTS FROM CHAINLINK NODE -> 'EXTERNAL ADAPTOR'
# =======================================================================================================================


@app.route("/echo", methods=["POST"])
def echo():
    """
    echo_bridge

    Endpoint to echo 'message' field in request body from Chainlink node to desired output function.
    Note:   This endpoint is set up as a bridge in the Chainlink Node Operator UI.
    """

    req = request.get_json()
    print("Request received to echo route:")
    print(f"{req}")
    external_adaptor.echo(req['data']["message"])
    return jsonify({})


@app.route("/start", methods=["POST"])
def start():
    """
    start_bridge

    Endpoint for request from Chainlink node to start an offchain computation process.
    Note:   This endpoint is set up as a bridge in the Chainlink Node Operator UI.
    """

    req = request.get_json()
    print("Request received to start route:")
    print(f"{req}")
    contract_address = req['data']["contractAddress"]
    process_id = req['data']["processId"]
    external_adaptor.start_process(contract_address, process_id)
    return jsonify({})


@app.route("/stop", methods=["POST"])
def stop():
    """
    stop_bridge

    Endpoint for request from Chainlink node to stop an offchain computation process.
    Note:   This endpoint is set up as a bridge in the Chainlink Node Operator UI.
    """

    req = request.get_json()
    print("Request received to stop route:")
    print(f"{req}")
    contract_address = req['data']["contractAddress"]
    process_id = req['data']["processId"]
    external_adaptor.stop_process(contract_address, process_id)
    return jsonify({})


@app.route("/callback", methods=["POST"])
def callback():
    """
    callback_bridge

    Endpoint for a request from a Chainlink node, which includes a jobID in the request body data.
    The jobID is to be used in a job request to the node.
    Note:   This endpoint is set up as a bridge in the Chainlink Node Operator UI.
            Request params from the bridge request must include a "callbackJobId" field, which specifies the
            job that will be run by the node upon receiving the callback.
    """

    req = request.get_json()
    print("Request received to callback route:")
    print(f"{req}")
    callback_job_id = req['data']["callbackJobId"]
    external_initiator.call_chainlink_node(
        callback_job_id,
        CHAINLINK_ACCESS_KEY,
        CHAINLINK_ACCESS_SECRET,
        CHAINLINK_IP
    )
    return jsonify({})


# ======================================================================================================================
#   APPLICATION ROUTES - ENDPOINTS TO CALL CHAINLINK NODE -> 'EXTERNAL INITIATOR'
# ======================================================================================================================


@app.route("/test", methods=["POST"])
def test():
    """
    test

    Endpoint for sending a request to the Chainlink Node to trigger a job run for the "jobId" specified in the
    request body.
    Note:   An external initiator must have already been created for the node in docker admin named "test", which
            points at the port this app is listening on.
    """

    req = request.get_json()
    print("Request received to test route:")
    print(f"{req}")
    callback_job_id = req["jobId"]
    response = external_initiator.call_chainlink_node(
        callback_job_id,
        CHAINLINK_ACCESS_KEY,
        CHAINLINK_ACCESS_SECRET,
        CHAINLINK_IP
    )
    print(f"Response from request to Chainlink node:")
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    return Response(status=200)
