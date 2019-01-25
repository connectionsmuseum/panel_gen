from flask import make_response, abort
import panel_gen

# Handler for /app GET
def read_status():
   result = panel_gen.get_info() 
   if result != False:
       return result
   else:
       abort(
            406,
            "Failed to get info",
        )

def start(**kwargs):
    switch = kwargs.get("switch", "")
    mode = kwargs.get("mode", "")
    source = kwargs.get("source", "")

    if mode == "demo":
        result = panel_gen.api_start(switch, mode="demo")
    elif mode != "demo":
        result = panel_gen.api_start(switch)    

    if result != False:
        if source == "web":
            return 'See Other', 303, {'Location': '/'}
        else:
            return result 
    else:
        abort(
            406,
            "Failed to create switch. May already be running.",
        )

def stop(**kwargs):
    switch = kwargs.get("switch", "")
    source = kwargs.get("source", "")
    
    result = panel_gen.api_stop(switch)

    if result != False:
        if source == "web":
            return 'See Other', 303, {'Location': '/'}
        else:
            return result 
    else:
        if source == "web":
            return 'See Other', 303, {'Location': '/'}
        else:
            abort(
                406,
                "Failed to create switch. May already be running.",
            )

def web_start(**kwargs):
    switch = kwargs.get("switch", "")
    mode = kwargs.get("mode", "")
    if mode == "demo":
        result = panel_gen.api_start(switch, mode="demo")
    elif mode != "demo":
        result = panel_gen.api_start(switch)    
    if result != False:
        return 'See Other', 303, {'Location': '/'}
    else:
        abort(
            406,
            "Failed to create switch. May already be running.",
        )

def web_stop(**kwargs):
    switch = kwargs.get("switch", "")
    result = panel_gen.api_stop(switch)
    if result != False:
        return 'See Other', 303, {'Location': '/'}
    else:
        abort(
            406,
            "Failed to stop switch. Maybe already stopped.",
        )
def api_pause():
    result = panel_gen.api_pause()
    if result != False:
        return result
    else:
        abort(
            406,
            "Failed to pause app. May already be paused.",
        )


def api_resume():
    result = panel_gen.api_resume()
    if result != False:
        return result
    else:
        abort(
            406,
            "Failed to resume app. May already be running.",
        )

def call(**kwargs):
    switch = kwargs.get("switch", "")
    destination = kwargs.get("destination", "")
    result = panel_gen.call_now(switch, destination)
    if result != False:
        return result
    else:
        abort(
            406,
            "Call failed for some reason. This message is very unhelpful",
        )
