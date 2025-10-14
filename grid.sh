#!/bin/bash

# Selenium Grid Management Script

case $1 in
  "start")
    echo "Starting Selenium Grid..."
    docker-compose up -d
    echo "Grid started! Access console at: http://localhost:4444/ui"
    ;;
  "stop")
    echo "Stopping Selenium Grid..."
    docker-compose down
    ;;
  "restart")
    echo "Restarting Selenium Grid..."
    docker-compose restart
    ;;
  "status")
    echo "Selenium Grid Status:"
    docker-compose ps
    ;;
  "logs")
    if [ -z "$2" ]; then
      docker-compose logs
    else
      docker-compose logs $2
    fi
    ;;
  "scale")
    if [ -z "$2" ] || [ -z "$3" ]; then
      echo "Usage: ./grid.sh scale <service> <replicas>"
      echo "Example: ./grid.sh scale chrome 3"
    else
      docker-compose up -d --scale $2=$3
    fi
    ;;
  "clean")
    echo "Cleaning up Selenium Grid..."
    docker-compose down -v --remove-orphans
    docker system prune -f
    ;;
  *)
    echo "Selenium Grid Management Script"
    echo ""
    echo "Usage: $0 {start|stop|restart|status|logs|scale|clean}"
    echo ""
    echo "Commands:"
    echo "  start     - Start the Selenium Grid"
    echo "  stop      - Stop the Selenium Grid" 
    echo "  restart   - Restart the Selenium Grid"
    echo "  status    - Show grid status"
    echo "  logs      - Show logs (optionally specify service name)"
    echo "  scale     - Scale a service (usage: scale <service> <replicas>)"
    echo "  clean     - Stop and remove all containers, volumes, and orphans"
    echo ""
    echo "Examples:"
    echo "  $0 start"
    echo "  $0 logs selenium-hub"
    echo "  $0 scale chrome 3"
    ;;
esac