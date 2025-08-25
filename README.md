# Pakistani WhatsApp Number Tester

A Node.js tool that generates and tests Pakistani phone numbers to check their WhatsApp registration status.

## Features

- Generates random Pakistani phone numbers with realistic patterns
- Tests numbers against WhatsApp API to check registration status
- Configurable number of tests and timeout settings
- Clean console output with status indicators

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pak-whatsapp-tester.git
cd pak-whatsapp-tester
```

2. Install dependencies:
```bash
npm install
```

## Usage

Run the script:
```bash
npm start
```

Or directly with Node.js:
```bash
node index.js
```

## Configuration

You can modify these constants in `index.js`:

- `NUM_COUNT`: Number of phone numbers to test (default: 15)
- `HTTP_TIMEOUT`: Timeout for HTTP requests in milliseconds (default: 5000)
- `NEGATIVE_REGEX`: Regular expression to detect unregistered numbers

## How it works

1. Generates Pakistani phone numbers with country code 92 (300-349 area codes)
2. Creates unique 7-digit subscriber numbers with specific patterns
3. Tests each number by making requests to WhatsApp's API
4. Reports whether each number is registered on WhatsApp

## Sample Output

```
Testing 15 numbers...

01. Local: 0315123456 | waLink: https://api.whatsapp.com/send/?phone=92315123456... -> ✅ Registered
02. Local: 0301987654 | waLink: https://api.whatsapp.com/send/?phone=92301987654... -> ❌ Not Registered
...
```

## License

MIT License

## Disclaimer

This tool is for educational purposes only. Please respect WhatsApp's terms of service and privacy policies. Do not use this tool for spam or harassment.
