#!/usr/bin/env python3
"""
Home Assistant Add-on: LG Dev Session Auto Renew
Main script to automatically renew LG webOS Developer Mode sessions
"""

import json
import logging
import time
import requests
import schedule
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

CONFIG_PATH = Path('/data/options.json')

def load_config():
    """Load configuration from Home Assistant options"""
    try:
        with open(CONFIG_PATH, 'r') as config_file:
            config = json.load(config_file)
            logger.info("Configuration loaded successfully")
            logger.info(f"URL: {config.get('url', 'Not set')}")
            logger.info(f"Interval: {config.get('interval_hours', 48)} hours")
            return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found at {CONFIG_PATH}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse configuration: {e}")
        sys.exit(1)

def renew_session(url):
    """Make a GET request to renew the LG Developer session"""
    try:
        logger.info(f"Attempting to renew LG Developer session: {url}")
        
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Parse JSON response
        try:
            json_response = response.json()
            logger.info(f"API Response: {json_response}")
            
            # Check if the response indicates success
            result = json_response.get('result', '').lower()
            error_code = json_response.get('errorCode', '')
            error_msg = json_response.get('errorMsg', '')
            
            if result == 'success' and error_code == '200':
                logger.info("✅ Session renewal successful!")
                # Only log the message if it's meaningful (not just "GNL" or similar codes)
                if error_msg and error_msg not in ['GNL', 'OK', '']:
                    logger.info(f"Response message: {error_msg}")
                else:
                    logger.info("LG Developer session has been successfully renewed")
                return True
            else:
                logger.error(f"❌ Session renewal failed according to API response")
                logger.error(f"Result: {result}, Error Code: {error_code}, Error Message: {error_msg}")
                return False
                
        except (ValueError, KeyError) as json_error:
            # If response is not JSON or missing expected fields, log raw response
            logger.warning(f"Could not parse JSON response: {json_error}")
            logger.info(f"Raw response: {response.text}")
            logger.info(f"HTTP Status: {response.status_code} - assuming success")
            return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to renew session: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during session renewal: {e}")
        return False

def main():
    """Main application loop"""
    logger.info("Starting LG Dev Session Auto Renew Add-on")
    
    # Load configuration
    config = load_config()
    url = config.get('url')
    interval_hours = config.get('interval_hours', 48)
    
    if not url:
        logger.error("URL is required but not provided in configuration")
        sys.exit(1)
    
    # Validate URL format
    if not url.startswith(('http://', 'https://')):
        logger.error("URL must start with http:// or https://")
        sys.exit(1)
    
    # Create a wrapper function for scheduled renewals with better logging
    def scheduled_renewal():
        logger.info("🔄 Scheduled session renewal starting...")
        success = renew_session(url)
        if success:
            logger.info("📅 Scheduled session renewal completed successfully")
        else:
            logger.error("📅 Scheduled session renewal failed")
        return success
    
    # Schedule the renewal job
    schedule.every(interval_hours).hours.do(scheduled_renewal)
    
    # Run initial renewal
    logger.info("Performing initial session renewal...")
    initial_success = renew_session(url)
    
    if initial_success:
        logger.info("🎉 Initial session renewal completed successfully")
    else:
        logger.warning("⚠️ Initial session renewal failed - will retry according to schedule")
    
    # Main loop
    logger.info(f"Session renewal scheduled every {interval_hours} hours")
    logger.info("Add-on is running. Press Ctrl+C to stop.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("Add-on stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
