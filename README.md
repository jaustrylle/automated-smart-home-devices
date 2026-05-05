# automated-smart-home-devices
Improving Transparency and Customization in Automated Smart Home Devices through an FOL Rule-Based AI System

How to run locally:
1. Install Streamlit
pip install streamlit
2. Run the app
streamlit run app.py
OR TO BYPASS PATH: python -m streamlit run app.py
4. Open your browser
http://localhost:8501

How to run via Google Colab (with a tunnel):
1. Install dependencies
!pip install streamlit pyngrok
2. Create the app file
%%writefile app.py
[put the streamlit code here]
3. Run and expose Streamlit
from pyngrok import ngrok
import os
public_url = ngrok.connect(8501)
print(public_url)
os.system("streamlit run app.py --server.port 8501 &")
