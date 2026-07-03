"""
Main entry point for Network Health Monitor
"""

import logging
import yaml
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function - Entry point for the application"""
    
    logger.info("="*70)
    logger.info("🚀 Network Health Monitor Started")
    logger.info(f"📅 Timestamp: {datetime.now().isoformat()}")
    logger.info("="*70)
    
    try:
        # Load device configuration
        with open('config/devices.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        logger.info(f"✅ Loaded {len(config['devices'])} devices from configuration")
        
        # List all configured devices
        logger.info("\n📋 Configured Devices:")
        logger.info("-" * 70)
        
        for device in config['devices']:
            logger.info(f"  • {device['name']:20} ({device['vendor']:10}) - {device['description']}")
        
        logger.info("-" * 70)
        
        # TODO: Week 2 - Implement device connection logic
        # TODO: Week 2 - Implement metrics collection
        # TODO: Week 3 - Implement anomaly detection
        # TODO: Week 3 - Implement alerting
        
        logger.info("\n✅ Network Health Monitor initialized successfully!")
        logger.info("📝 Week 1: Architecture & Setup - COMPLETE ✅")
        logger.info("📝 Week 2: Core Functionality - NEXT")
        
    except FileNotFoundError:
        logger.error("❌ Configuration file 'config/devices.yaml' not found!")
        return False
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")
        return False
    
    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
