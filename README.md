
# CLI utils to convert an mcp server to a skill

Input: mcp-server url, auth type (dynamic oauth, api key, none)
Output: app.py (MCP App Class), SKILL.md ( How to use mcp server)


## Workings

Uses fastmcp to Connect to the MCB server and then eject the MCB as a class. For example if it's a github mcp server, the class is going to be called github app. Each method is exposed as a function of this class. The class initialization defines how to connect to that And initializes the first MCP client.
The OAuth is an input parameter of the class used in initialization. It can be of type OAuth or API key. If it is OAuth, its dynamic oauth. If it's an API key, it uses that. It's a standard API key. 

The interface is just a CLI that the user uses to create an mcp skill from mcp url. It should ask for URL type; it should also ask for authentication type. Try connecting first and then use the list tools to see all the available tools and then convert them into Python types. 
The entire thing is published as a Python cli package.

## Setup

Uses UV to manage the Python dependencies.

Only supports tools from MCP. (resources, prompts, etc will come soon)
