import subprocess                                                               
import os
absolute_path = os.path.abspath(__file__)
                                                            
def main(port = 5000):                                                                   
    cmd =['streamlit', 'run', os.path.dirname(absolute_path)+'/app.py', '--server.port','{0}'.format(port),'--theme.base','dark']                                                                 
    subprocess.run(cmd)                                                    
