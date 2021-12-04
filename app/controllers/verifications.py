
class WrongOptionError(Exception):
    def __init__(self, value): 
       self.value = value 
      
    def __str__(self):
        return(repr(self.value))


class WrongKeyError(Exception):
    def __init__(self, value): 
       self.value = value 
      
    def __str__(self):
        return(repr(self.value))



def limitation(kwargs, method="post"):
    if method == "post":
        control = {"11","12","21","22"}
        key = str(kwargs['importance']) + str(kwargs['urgency'])
        if key not in control:
            resp = {"error":{"valid_options":{"importance":[1,2],"urgency":[1,2]}, "received_options":{"importance":kwargs['importance'],"urgency":kwargs['urgency']}}}
            raise WrongOptionError(resp)

        eisen = {"11":"Do It First", "12":"Schedule It", "21":"Delegate It","22":"Delete It"}
        

        return eisen[key]
    else:
        
        i = str(kwargs.get('importance', None))
        u = str(kwargs.get('urgency', None))
        if i != 'None' or u != 'None':
            if i in {'1','2'} or u in {'1','2'}:
                return True
            else:
                if i != 'None':
                    resp = {
                        "error":{"valid_options":{"importance":[1,2]},
                                "received_options":{"importance":int(i)}}}
                    raise WrongOptionError(resp)
                if u != 'None':
                    resp = {
                        "error":{"valid_options":{"urgency":[1,2]},
                                "received_options":{"urgency":int(u)}}}
                    raise WrongOptionError(resp)
                if i != 'None' and u != 'None':
                    resp = {
                        "error":{"valid_options":{"importance":[1,2],"urgency":[1,2]},
                        "received_options":{"importance":int(i),"urgency":int(u)}}}                
                    raise WrongOptionError(resp)


def verify_keys(kwargs, option, method="post"):
    
    options = {
        "task":{'name','importance','urgency','description', 'duration', 'categories'},
        "category":{'name', 'description'}
        
    }

    keys = set(kwargs.keys())

    if method == "post":
        if not options[option].issubset(keys):
            error = list(keys - options[option])
            
            raise WrongKeyError({"wrong_keys_sent":error, "available_keys":list(options[option])})
                    
    else:
        
        if not keys.issubset(options[option]):
            error = list(keys - options[option])
            raise WrongKeyError({"wrong_keys_sent":error, "available_keys":list(options[option])})
        
        else:
            return True;



