const fs = require('fs');
const path = require('path');

class Logger {
  constructor(logDirectory = process.cwd()) {
    const currentDate = new Date().toISOString().slice(0, 10);
    this.logFileName =  `${currentDate}.log`;
    this.logFilePath = path.join(logDirectory, this.logFileName);
  }

  log(level, message, data, functionName) {
    const logEntry = {
      level,
      datetime: new Date().toISOString(),
      message,
      data,
      functionName,
    };

    const logString = JSON.stringify(logEntry) + '\n';

    fs.appendFile(this.logFilePath, logString, (err) => {
      if (err) {
        console.error('Failed to write to log file:', err);
      }
    });
  }

  debug(message, data, functionName) {
    this.log('debug', message, data, functionName);
  }

  info(message, data, functionName) {
    this.log('info', message, data, functionName);
  }

  warn(message, data, functionName) {
    this.log('warn', message, data, functionName);
  }

  error(message, data, functionName) {
    this.log('error', message, data, functionName);
  }
}

// Usage example
// const logger = new Logger(undefined); // Log file will be created in the current working directory with the name "YYYY-MM-DD.log"
// logger.debug('Debug message', { example: 'data' }, 'myFunction');
// logger.info('Info message', null, 'myFunction');
// logger.warn('Warning message', { example: 'data' }, 'myFunction');
// logger.error('Error message', { example: 'data' }, 'myFunction');

// const customLogDirectory = '/home/nihar/fyers_project/node SDK/logger';
// const customLogger = new Logger(customLogDirectory);
// customLogger.debug('Custom debug message', null, 'myFunction');
// customLogger.info('Custom info message', { example: 'data' }, 'myFunction');

module.exports = Logger