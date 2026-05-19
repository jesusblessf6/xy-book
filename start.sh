#!/bin/bash
# Start all XY-Book backend services
# Usage: ./start.sh [stop]

set -e

SERVICES_DIR="$(cd "$(dirname "$0")/services" && pwd)"

# Service definitions: name port module
declare -a SERVICES=(
    "community 8001 xybook_community.main:app"
    "agents    8002 xybook_agents.main:app"
    "pipeline  8004 xybook_pipeline.main:app"
    "experiments 8005 xybook_experiments.main:app"
    "gateway   8000 xybook_gateway.main:app"
)

PIDS=()

start_services() {
    echo "=== Starting XY-Book services ==="

    # Start Redis if not running
    if ! redis-cli ping > /dev/null 2>&1; then
        echo "Starting Redis..."
        brew services start redis
        sleep 1
    fi

    # Check PostgreSQL
    if ! pg_isready > /dev/null 2>&1; then
        echo "Starting PostgreSQL..."
        brew services start postgresql@16
        sleep 2
    fi

    for entry in "${SERVICES[@]}"; do
        read -r name port module <<< "$entry"
        echo "Starting $name on :$port ..."
        cd "$SERVICES_DIR/xybook-$name"
        nohup uvicorn "$module" --host 0.0.0.0 --port "$port" --reload \
            > "/tmp/xybook-$name.log" 2>&1 &
        PIDS+=($!)
        echo "  PID=$! log=/tmp/xybook-$name.log"
        sleep 0.5
    done

    echo ""
    echo "=== All services started ==="
    echo "Gateway:      http://localhost:8000"
    echo "Community:    http://localhost:8001"
    echo "Agents:       http://localhost:8002"
    echo "Pipeline:     http://localhost:8004"
    echo "Experiments:  http://localhost:8005"
    echo ""
    echo "Community Web:  cd services/xybook-community-web && npm run dev"
    echo "Admin Web:      cd services/xybook-admin-web && npm run dev"
}

stop_services() {
    echo "=== Stopping XY-Book services ==="
    for entry in "${SERVICES[@]}"; do
        read -r name port module <<< "$entry"
        pid=$(lsof -ti :$port 2>/dev/null || true)
        if [ -n "$pid" ]; then
            echo "Stopping $name (PID $pid) ..."
            kill $pid 2>/dev/null || true
        fi
    done
    echo "All services stopped."
}

health_check() {
    echo "=== Health Check ==="
    for entry in "${SERVICES[@]}"; do
        read -r name port module <<< "$entry"
        status=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:$port/health" 2>/dev/null || echo "000")
        if [ "$status" = "200" ]; then
            echo "  $name (:$port) ✅"
        else
            echo "  $name (:$port) ❌ (HTTP $status)"
        fi
    done
}

case "${1:-start}" in
    start)
        start_services
        sleep 3
        health_check
        ;;
    stop)
        stop_services
        ;;
    health)
        health_check
        ;;
    *)
        echo "Usage: $0 [start|stop|health]"
        exit 1
        ;;
esac
