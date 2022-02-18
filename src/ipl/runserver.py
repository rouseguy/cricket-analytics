import subprocess                                                               
                                                                                
def main():                                                                   
    cmd =['streamlit', 'run', 'src/ipl/app.py', '--server.port','5000']                                                                 
    subprocess.run(cmd)                                                    

main()