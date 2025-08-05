# Dify Python MCP Server - IoT CNC Data Integration

A Model Context Protocol (MCP) server that provides tools for interacting with IoT CNC Data API. This server enables Dify to retrieve and analyze CNC machine data from the IoT Management system.

## Features

### IoT CNC Data Tools

- **get_iot_cnc_data**: Retrieve CNC data with pagination and equipment filtering
- **get_iot_cnc_data_by_id**: Get specific CNC data record by ID
- **get_iot_equipment_list**: List all available equipment IDs
- **search_cnc_data**: Advanced search with multiple filters (operation mode, alarms, workpiece count)
- **get_equipment_summary**: Generate summary statistics for equipment performance

### Additional Tools

- **Email notifications**: Send alerts and reports via SMTP
- **Data processing**: Transform and analyze CNC data

## Quick Start

### Using Docker (Recommended)

1. **Clone and build**:
   ```bash
   git clone <repository-url>
   cd dify-python-mcp-server
   docker compose up --build
   ```

2. **Access the server**:
   - Main server: http://localhost:6018
   - Health check: http://localhost:6018/health

### Manual Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment** (copy `.env` and modify if needed):
   ```bash
   cp .env.example .env
   ```

3. **Run the server**:
   ```bash
   python -m src.main
   ```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `EXTERNAL_API_BASE_URL` | IoT CNC Data API base URL | `http://iot.datawits.net:8000/api/method/frappe.integrations.api_dify.` |
| `EXTERNAL_API_KEY` | API key (not required for guest access) | `not_required_guest_access` |
| `SERVER_PORT` | Server port | `6018` |
| `LOG_LEVEL` | Logging level | `INFO` |

### IoT API Configuration

The server is pre-configured to work with the IoT CNC Data API at `iot.datawits.net`. The API endpoints used are:

- `get_iot_cnc_data` - Retrieve CNC data with optional filtering
- `get_iot_cnc_data_by_id` - Get specific record by ID  
- `get_iot_equipment_list` - List available equipment

## Usage Examples

### Dify Integration

Connect this MCP server to Dify to enable CNC data analysis:

1. **Add MCP server** in Dify settings:
   - Server URL: `http://your-server:6018`
   - Available tools will be automatically discovered

2. **Use in conversations**:
   ```
   "Show me the latest CNC data for equipment CNC001"
   "Get a summary of equipment CNC002 performance"
   "List all available CNC equipment"
   "Find CNC records with alarms in AUTO mode"
   ```

### Direct API Usage

You can also use the server directly via HTTP:

```bash
# Get equipment list
curl -X POST http://localhost:6018/tools/get_iot_equipment_list \
  -H "Content-Type: application/json" \
  -d '{}'

# Get CNC data for specific equipment
curl -X POST http://localhost:6018/tools/get_iot_cnc_data \
  -H "Content-Type: application/json" \
  -d '{"equipment_id": "cnc-dw-16-0009", "limit": 10}'

# Search with filters
curl -X POST http://localhost:6018/tools/search_cnc_data \
  -H "Content-Type: application/json" \
  -d '{"operation_mode": "AUTO", "has_alarm": false, "limit": 50}'
```

## Data Structure

### CNC Data Record

```json
{
  "id": "cnc-CNC001-0001",
  "equipment_id": "CNC001", 
  "workpiece_count": 150,
  "runtime": "08:30:00",
  "cutting_time": "06:45:30",
  "cnc_model": "DMG MORI NLX2500",
  "current_tool_no": "T0101",
  "operation_mode": "AUTO",
  "run_mode": "CONTINUOUS",
  "rapid_override": "100%",
  "spindle_actual_rpm": "2500",
  "feed_actual_rate": "1200",
  "spindle_load": "75%",
  "x_axis_load": "45%",
  "y_axis_load": "30%",
  "z_axis_load": "60%",
  "alarm_code": null,
  "alarm_message": null,
  "created_at": "2025-01-21 10:30:00",
  "updated_at": "2025-01-21 14:15:00"
}
```

## Development

### Project Structure

```
src/
├── config/          # Configuration management
├── tools/           # MCP tool implementations
│   ├── external_api.py    # IoT CNC API tools
│   ├── notification.py    # Email tools
│   └── data_processor.py  # Data processing tools
├── utils/           # Utilities
└── main.py         # MCP server entry point
```

### Adding New Tools

1. Create tool in appropriate module under `src/tools/`
2. Add tool schema to `get_tools()` method
3. Implement tool logic in `execute_tool()` method
4. Add validation if needed in `src/utils/validation.py`

### Testing

```bash
# Run tests
pytest

# Test with MCP inspector (requires Node.js 14+)
npx @modelcontextprotocol/inspector python -m src.main
```

## Troubleshooting

### Common Issues

1. **Container won't start**: Check Docker logs and ensure ports aren't in use
2. **API connection failed**: Verify `EXTERNAL_API_BASE_URL` is accessible
3. **No data returned**: Check if equipment IDs exist using `get_iot_equipment_list`

### Logs

```bash
# Docker logs
docker compose logs -f mcp-server

# Local logs
tail -f logs/app.log
```

## License

[Add license information]

## Support

For issues and questions:
- Check the logs for error details
- Verify API connectivity to `iot.datawits.net:8000`
- Review the IoT API documentation for data formats
