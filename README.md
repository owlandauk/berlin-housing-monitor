# Berlin Housing Monitor

An automated web scraper that monitors new housing listings in Berlin and sends notifications via email and Google Sheets.

## Features

- 🏠 Scrapes housing listings from home-in-berlin.de
- 📧 Email notifications for new listings
- 📊 Automatic Google Sheets integration
- 🔄 Automated scheduling with n8n
- 🐳 Docker containerized

## Setup

### Prerequisites

- Docker and Docker Compose
- Google Cloud Console account (for Sheets API)
- Gmail account (for email notifications)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/owlandauk/berlin-housing-monitor.git
cd berlin-housing-monitor
```

2. Build and run the n8n container with Python support:
```bash
docker-compose up -d
```

3. Access n8n at http://localhost:5678
<img width="2681" height="521" alt="image" src="https://github.com/user-attachments/assets/2895bd12-6044-4653-bede-f47b16c99ba9" />

### Configuration

1. **Google Sheets Setup:**
   - Create a service account in Google Cloud Console
   - Enable Google Sheets API
   - Download JSON credentials
   - Share your Google Sheet with the service account email

2. **Gmail Setup:**
   - Enable Gmail API or use App Password
   - Configure OAuth2 credentials

3. **Import n8n Workflow:**
   - Import the workflow from `n8n-workflow.json`
   - Configure credentials for Google Sheets and Gmail

## Project Structure

```
berlin-housing-monitor/
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── scripts/
│   └── run_spider.py
├── n8n-workflow.json
├── README.md
└── requirements.txt
```

## Usage

The system runs automatically based on the schedule configured in n8n (default: every hour).

### Manual Testing

Test the spider directly:
```bash
python scripts/run_spider.py
```

## Workflow

1. **Schedule Trigger** → Runs every hour
2. **Execute Command** → Runs the Python spider
3. **Code Node** → Processes the JSON output  
4. **IF Node** → Checks for new listings
5. **Gmail Node** → Sends email notification (if new listings)
6. **Google Sheets** → Updates spreadsheet with all listings

## License

MIT License
