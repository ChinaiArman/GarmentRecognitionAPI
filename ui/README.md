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