import requests, time, json
# O2A - Data flow Orchestrator to Agent

# f"{lProtocolStr}://{lHostStr}:{lPortInt}/pyOpenRPA/Agent/O2A"
# Request BODY:
# { "HostNameUpperStr": "", "UserUpperStr": "" }
# Response BODY:
# QUEUE ITEM
#                 # {
#                 #    "Def":"DefAliasTest", # def link or def alias (look gSettings["Processor"]["AliasDefDict"])
#                 #    "ArgList":[1,2,3], # Args list
#                 #    "ArgDict":{"ttt":1,"222":2,"dsd":3} # Args dictionary
#                 #    "ArgGSettings": # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
#                 #    "ArgLogger": None # Name of GSettings attribute: str (ArgDict) or index (for ArgList)
#                 # },

def O2A_Loop(inGSettings):
    lL = inGSettings["Logger"]
    lActivityLastGUIDStr = "" # Init empty ActivityLastGUIDStr
    while inGSettings["O2ADict"]["IsOnlineBool"]:
        # Send request to the orchestrator server
        lRequestBody = None
        try:
            lProtocolStr= "https" if inGSettings["OrchestratorDict"]["IsHTTPSBool"] else "http"
            lHostStr = inGSettings["OrchestratorDict"]["HostStr"]
            lPortInt = inGSettings["OrchestratorDict"]["PortInt"]
            lURLStr=f"{lProtocolStr}://{lHostStr}:{lPortInt}/pyOpenRPA/Agent/O2A"
            lDataDict = { "HostNameUpperStr": inGSettings["AgentDict"]["HostNameUpperStr"], "UserUpperStr": inGSettings["AgentDict"]["UserUpperStr"], "ActivityLastGUIDStr": lActivityLastGUIDStr}
            lResponse = requests.post(url= lURLStr, cookies = {"AuthToken":inGSettings["OrchestratorDict"]["SuperTokenStr"]}, json=lDataDict)
            if lResponse.status_code != 200:
                if lL: lL.warning(f"Agent can not connect to Orchestrator. Below the response from the orchestrator:{lResponse}")
                time.sleep(inGSettings["O2ADict"]["RetryTimeoutSecFloat"])
            else:
                lRequestBody = lResponse.text
                lQueueItem = lResponse.json() # Try to get JSON
                # Append QUEUE item in ProcessorDict > ActivityList
                lActivityLastGUIDStr = lQueueItem["GUIDStr"]
                inGSettings["ProcessorDict"]["ActivityList"].append(lQueueItem)
                if lL: lL.debug(f"ActivityItem was received from orchestrator: {lQueueItem}");
        except requests.exceptions.ConnectionError as e:
            if lL: lL.error(f"O2A Connection error - orchestrator is not available. Sleep for {inGSettings['A2ODict']['RetryTimeoutSecFloat']} s.")
            time.sleep(inGSettings["O2ADict"]["RetryTimeoutSecFloat"])
        except ConnectionResetError as e:
            if lL: lL.error(f"O2A Connection error - orchestrator is not available. Sleep for {inGSettings['A2ODict']['RetryTimeoutSecFloat']} s.")
            time.sleep(inGSettings["O2ADict"]["RetryTimeoutSecFloat"])
        except json.decoder.JSONDecodeError as e:
            if lL: lL.error(f"See body of the recieved content from the Orchestrator: {lRequestBody}")
            time.sleep(inGSettings["O2ADict"]["RetryTimeoutSecFloat"])
        except Exception as e:
            if lL: lL.exception(f"O2A Error handler. Sleep for {inGSettings['A2ODict']['RetryTimeoutSecFloat']} s.")
            time.sleep(inGSettings["O2ADict"]["RetryTimeoutSecFloat"])