# Selenium Grid Docker Compose

This project sets up a Selenium Grid environment using Docker Compose with multiple browser nodes.

## Architecture

- **Selenium Hub**: Central point that receives test requests and distributes them to available nodes
- **Chrome Nodes**: 2 replicas handling Chrome browser tests
- **Firefox Nodes**: 2 replicas handling Firefox browser tests  
- **Edge Node**: 1 instance handling Microsoft Edge browser tests

## Quick Start

1. Start the Selenium Grid:
```bash
docker-compose up -d
```

2. Check the status:
```bash
docker-compose ps
```

3. Access the Selenium Grid Console:
   - Open your browser and go to: http://localhost:4444/ui
   - This shows available nodes and running sessions

4. Stop the grid:
```bash
docker-compose down
```

## Endpoints

- **Grid Console**: http://localhost:4444/ui
- **Hub API**: http://localhost:4444/wd/hub
- **Grid Status**: http://localhost:4444/status

## Configuration

### Port Mapping
- `4442`: Event Bus (Publish)
- `4443`: Event Bus (Subscribe) 
- `4444`: Hub Web Interface and WebDriver API

### Environment Variables

**Hub Configuration:**
- `GRID_MAX_SESSION=16`: Maximum concurrent sessions
- `GRID_BROWSER_TIMEOUT=300`: Browser timeout in seconds
- `GRID_TIMEOUT=300`: Grid timeout in seconds

**Node Configuration:**
- `NODE_MAX_INSTANCES=2`: Max browser instances per node
- `NODE_MAX_SESSION=2`: Max sessions per node
- `HUB_HOST=selenium-hub`: Hub hostname
- `HUB_PORT=4444`: Hub port

## Scaling

To scale specific browser nodes:

```bash
# Scale Chrome nodes to 3 instances
docker-compose up -d --scale chrome=3

# Scale Firefox nodes to 4 instances
docker-compose up -d --scale firefox=4
```

## Example Test Connection

Connect your tests to the grid using:
- **Remote WebDriver URL**: http://localhost:4444/wd/hub

### Java Example
```java
ChromeOptions options = new ChromeOptions();
WebDriver driver = new RemoteWebDriver(new URL("http://localhost:4444/wd/hub"), options);
```

### Python Example
```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    options=chrome_options
)
```

### C# Example
```csharp
var options = new ChromeOptions();
var driver = new RemoteWebDriver(new Uri("http://localhost:4444/wd/hub"), options);
```

## Troubleshooting

### Check logs
```bash
# View hub logs
docker-compose logs selenium-hub

# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f
```

### Common Issues

1. **Nodes not connecting**: Ensure the hub is fully started before nodes attempt to connect
2. **Out of memory**: Increase Docker memory allocation or reduce `NODE_MAX_INSTANCES`
3. **Session timeout**: Adjust `GRID_BROWSER_TIMEOUT` and `GRID_TIMEOUT` values

### Performance Tips

1. **Memory**: Each browser instance uses ~1GB RAM
2. **CPU**: Ensure adequate CPU cores for parallel execution
3. **Network**: Use bridge network for better isolation
4. **Storage**: Mount `/dev/shm` for better performance

## Security Notes

- This setup is for development/testing environments
- For production, consider:
  - Adding authentication
  - Using HTTPS
  - Network security policies
  - Resource limits

## Monitoring

Monitor your grid through:
- Grid Console UI at http://localhost:4444/ui
- Docker stats: `docker stats`
- Container health: `docker-compose ps`