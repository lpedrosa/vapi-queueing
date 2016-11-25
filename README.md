# Call queueing example application

Simple example that shows how one can leverage the VAPI to build a simple call queueing application.

The idea behind it, is to:

* queue inbound calls when they dial a number
* unqueue them once the agent is ready to take those calls

For this we need:

* nexmo application id
* a private key for minting JWTs
* a nexmo number that will be the entry point of our application
