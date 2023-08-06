
import os
import re
import io
import json
from pathlib import Path

import requests
from requests import ReadTimeout, ConnectTimeout, HTTPError, Timeout 

def esprem_rpc( apiendpoint : str , endpoint: str, params_dict , rq_id : int = 0 , timeout = 60 ) :

    #f = open("/tmp/input.json", "w")
    #f.write(json.dumps(params_dict))
    #f.close()

    headers = { "content-type" : "application/json" }
    
    payload = {
                "method" : endpoint ,
                "params": params_dict ,
                "jsonrpc": "2.0" ,
                "id": rq_id ,
    }

    ################################################################

    try :

        #response = requests.post( url , json = payload , headers = headers , timeout = timeout ).json( )
#        response = requests.post( url , verify=False,json = payload , headers = headers , timeout = timeout )
#        response = requests.post( apiendpoint , verify=False, json = payload , headers = headers , timeout = timeout )
        response = requests.post( apiendpoint , json = payload , headers = headers , timeout = timeout )

        if(response.status_code != 200 ) :

            response = {
                            "_error" : {
                                "error" : True ,
                                "error_code" : "status_code" ,
                                "error_msg" : response.text ,
                            }
            }    

            return( response )    

    except requests.ConnectionError as e:

        response = {
                        "_error" : {
                            "error" : True ,
                            "error_code" : "ConnectionError" ,
                            "error_msg" : str( e ) ,
                        }
        }    
        return( response )    

    except requests.HTTPError as e:

        response = {
                        "_error" : {
                            "error" : True ,
                            "error_code" : "HTTPError" ,
                            "error_msg" : str( e ) ,
                        }
        }    
        return( response )    
    except requests.exceptions.InvalidSchema as e:

        response = {
                        "_error" : {
                            "error" : True ,
                            "error_code" : "InvalidSchema" ,
                            "error_msg" : str(e) ,
                        }
        }    
        return( response )    
    except requests.exceptions.InvalidURL as e:

        response = {
                        "_error" : {
                            "error" : True ,
                            "error_code" : "InvalidURL " ,
                            "error_msg" : str(e) ,
                        }
        }    
        return( response )    
    except requests.exceptions.MissingSchema as e:

        response = {
                        "_error" : {
                            "error" : True ,
                            "error_code" : "MissingSchema " ,
                            "error_msg" : str(e) ,
                        }
        }    
        return( response )    
    #except( ConnectTimeout, HTTPError, ReadTimeout, Timeout ) :

    ################################################################

    # url, data=json.dumps(payload), headers=headers).json()

    response=response.json()
    if( "result" in response ) :
        #f = open("/tmp/output.json", "w")
        #f.write(json.dumps(response))
        #f.close()
        return( response[ "result" ] )
    
    return( response[ "error" ] )


def trepem_deserial(targetpath, trepem_resp):
    """Deserializes the trepem server response dictionary into
    output files in the filesystem.

    Parameters
    ----------
    targetpath
        String target path in which to write the outputs hierarchy.
    trepem_resp The trepem response dictionary.

    Returns
    -------
        None
    """
    targetpath = targetpath + "/"
    if not os.path.exists(targetpath):
        os.makedirs(targetpath)
        os.makedirs(targetpath + "/trepem")
        os.makedirs(targetpath + "/mulassis")
        os.makedirs(targetpath + "/trajectory")
        os.makedirs(targetpath + "/mcict")
    else:
        print("Output diretory already exists aborting.")
        return
    for filename, string in trepem_resp.items():
        with open(targetpath + filename, "w+") as targetfile:
            targetfile.write(string)
    return


def esprem_deserial(targetpath, dictin):
    """Deserializes the esprem server response dictionary into output files in
    the filesystem.

    Parameters
    ----------
    targetpath
        Target path in which to write the outputs hierarchy.
    trepem_resp
        The trepem response dictionary.

    Returns
    -------
        None
    """
    Path(targetpath).mkdir(parents=True, exist_ok=True)

    for filename, string in dictin.items():
        filename = targetpath / Path(filename)
        filename.parent.mkdir(parents=True, exist_ok=True)
        with filename.open("w") as myfd:
            myfd.write(str(string))
    return


def get_mulassis_block(ml_output: str, block_name_str: str) -> str:
    """From the Mulassis output file, get the analysis block output.
    first match only until End of block.

    Parameters
    ----------
    ml_output
        The mulassis result file as a string.
    block_name_str
        The output block name, any of: {"DOSE ANALYSIS",
        "NID ANALYSIS", "PULSE-HEIGHT ANALYSIS"}

    Returns
    -------
        The block string.
    """
    with io.StringIO(ml_output) as ml_f:
        return re.findall(block_name_str + '(.*?)End of', ml_f.read(), re.S)[0]



