# Global Variables
SERVICE_NAME := template
SERVICE_HOST := 0.0.0.0
SERVICE_PORT := 8000

DAPR_APP_ID := ${SERVICE_NAME}
DAPR_HTTP_PORT := 3500
# DAPR_GRPC_PORT := 
DAPR_APP_PORT := ${SERVICE_PORT}
DAPR_APP_PROTOCOL := http
# DAPR_CONFIG := 
DAPR_LOG_LEVEL := info

DAPR_CMD := dapr run -a ${DAPR_APP_ID} -p ${DAPR_APP_PORT} -P ${DAPR_APP_PROTOCOL} --log-level ${DAPR_LOG_LEVEL}
SERVER_CMD := uvicorn --host ${SERVICE_HOST} --port ${SERVICE_PORT} service.main:app

# Run dapr sidecar for development
dapr:
	${DAPR_CMD}

# Start service in dev mode
dev:
	${SERVER_CMD} --reload

# Start dapr dev 
dapr-dev:
	${DAPR_CMD} -- ${SERVER_CMD} --reload

# Start dapr service
start:
	@${DAPR_CMD} -- ${SERVER_CMD}
