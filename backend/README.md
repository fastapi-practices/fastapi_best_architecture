# FastAPI Best Architecture - Backend

## Docker

1. Make sure you're at the root of the project
2. Run the following Docker command to build container:

   ```shell
   docker build -f Dockerfile -t fba_backend_independent .
   ```

3. Start container

   Native boot needs to change `127.0.0.1` in `.env` to `host.docker.internal`

   ```shell
   docker run -d -p 8000:8000 --name fba_server fba_backend_independent
   ```
