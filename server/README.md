# VENV Installation Instructions
1. Install VENV
    - ```cd server```
    - ```python3 -m venv .venv```
    - ```cd .venv```
2. Activate VENV Instance:
    - Mac:
        - Activation command: ```source bin/activate```
        - Deactivation command: ```source bin/deactivate```
    - Windows:
        - Activation command: ```Scripts\activate.bat```
        - Deactivation command: ```Scripts\deactivate.bat```
    Your interpreter should now be set to the Virtual Environment instance of python.
    - ```cd ..```
3. Install Packages:
    - Installation command: ```pip install -r requirement.txt```
    - Update command: ```pip freeze > requirement.txt```
4. Test: 
    - ```python app.py``` > Visit port 5000