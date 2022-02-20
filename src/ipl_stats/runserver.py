import subprocess                                                               
import os
absolute_path = os.path.abspath(__file__)
                                                            
def main():                                                                   
    cmd =['streamlit', 'run', os.path.dirname(absolute_path)+'/app.py', '--server.port','5000']                                                                 
    subprocess.run(cmd)                                                    
