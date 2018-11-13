from apps import create_api_app
cpi_app=create_api_app("apps.settings.DevAPIConfig")

if __name__ == '__main__':
    print(cpi_app.url_map)
    cpi_app.run(port=8080)