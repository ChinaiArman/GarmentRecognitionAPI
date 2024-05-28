# Swagger UI
This folder contains the UI assets for the Swagger API documentation.

The files in this folder are served by the flask server.

## File Explanations
- ```static/swagger.yaml```

    YAML file that contains the Swagger API definition for the server's API endpoints. Modify this file if changes to the API are made to ensure that the API documentation is always up to date. In particular, the ```server``` section should be updated if the API server is hosted on a different URL in the future.

- ```static/dist/swagger-initializer.js```

    The main configuration file for the Swagger UI. Use this file to configure the UI by modifying the configuration object passed as an argument to ```SwaggerUIBundle({ ... })```. Of particular importance is the ```url``` parameter in the configuration object, which is set to the URL pointing to the API definition file (```swagger.yaml```) described above. This is important if the Swagger UI is hosted on a publicly accessible server. In that case, the ```url``` parameter should be set to the location of the swagger API definition file (```swagger.yaml```) on that server.

- ```static/swagger-custom.js```

    Contains user-defined JavaScript plugins for customizing the Swagger UI. The plugins defined here are passed to the configuration object in ```static/dist/swagger-initializer.js``` using the ```plugins``` parameter.

- ```static/swagger-custom.css```

    Contains CSS declarations for customizing appearance of the Swagger UI.

- ```static/swagger-custom-dark.css```

    Contains CSS declarations for adding a dark mode feature to the Swagger UI.

- ```templates/index.html```

    HTML file that is initially served by the flask server. Used as a template to link to all the other static assets in this folder.

- the ```dist``` folder
    
    This folder contains all the UI assets and bundles distributed by Swagger UI from their repo [here](https://github.com/swagger-api/swagger-ui).

## Additional Notes
- Ensure the swagger.yaml file is always up-to-date with the latest API changes to provide accurate documentation.
- Customize the swagger-custom.js file to enhance the functionality of the Swagger UI with additional plugins.
- Adjust the swagger-custom.css and swagger-custom-dark.css files to fit the desired look and feel of the Swagger UI, including support for both light and dark modes.
- The index.html file is essential for integrating all the custom styles and scripts into the Swagger UI.

## Requirements

### Libraries
Ensure you have the required Python libraries installed:
```sh
cd server                           # Change to the server directory
pip install -r requirements.txt     # Install the required libraries
```

### Environment Variables
Ensure the following environment variables are set in a .env file:
```sh
AZURE_VISION_ENDPOINT= ""   # your_azure_vision_endpoint
AZURE_VISION_KEY_1=""       # your_azure_vision_key
AZURE_VISION_KEY_2=""       # your_azure_vision_key
RAPID_API_KEY=""            # your_rapid_api_key
EMBEDDED_MODEL=""           # your_embedded_model
DATA_SOURCE_FILE=""         # your_data_source_file
PYTHONPATH="server"         # Set the PYTHONPATH to "server"
```

## Usage
1. Start the server by running the following command:
```sh
cd ..                   # Return to the root directory
python server/app.py    # Start the server
```

## Deployment

The Swagger frontend can be deployed to GitHub Pages or any other static site hosting service.
- A guide to deploying the Swagger UI to GitHub can be found [here](https://github.com/peter-evans/swagger-github-pages).
- Swagger can also be deployed on any major cloud platform such as Azure or AWS.
    - A guide to deploying Swagger on AWS can be found [here](https://aws.amazon.com/blogs/devops/deploy-and-manage-openapi-swagger-restful-apis-with-the-aws-cloud-development-kit/).
    - A guide to deploying Swagger on Azure can be found [here](https://blog.cellenza.com/en/cloud/how-to-quickly-deploy-swagger-documentation-for-your-api-in-azure/).

The Swagger YAML file can be found [here](https://github.com/ChinaiArman/GarmentRecognitionAPI/blob/main/ui/static/swagger.yaml). Ensure that all references to the server are updated to the deployed server URL.