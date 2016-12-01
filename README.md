# Call queueing example application

Simple example that shows how one can leverage the VAPI to build a simple call queueing application.

The idea behind it, is to:

* queue inbound calls when they dial a number
* unqueue them once the agent is ready to take those calls

For this we need:

* nexmo application id
* a private key for minting JWTs
* a nexmo number that will be the entry point of our application

# Reasoning

Every time someone rings the nexmo LVN that points to this application, we direct that call to a conversation. On that conversation we play a simple holding tune using the `stream` action.

At the same time we capture the `conversation_id` and `call_id` of the call and submit this to an internal application queue.

When an agent is ready to take the call (currently represented as a scheduled task that polls the queue), it unqueues the call information.

It then transfers that `call_id` into a conversation with the agent already waiting for the caller (currently represented as a named conversation, in which we play a tts message representing the agent).
