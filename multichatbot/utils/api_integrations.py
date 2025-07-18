import os
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import json
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseAPI(ABC):
    """Abstract base class for all API integrations."""
    
    def __init__(self):
        self.config = self._load_config()
        self.session = requests.Session()
        self.session.headers.update(self._get_default_headers())
        
    def _load_config(self) -> Dict[str, Any]:
        """Load API configuration from config file or environment variables."""
        config_path = Path('config') / 'api_config.json'
        try:
            if config_path.exists():
                with config_path.open() as f:
                    return json.load(f).get(self.__class__.__name__, {})
            return {}
        except Exception as e:
            logger.warning(f"Failed to load config: {e}")
            return {}
    
    def _get_default_headers(self) -> Dict[str, str]:
        """Get default headers for API requests."""
        return {
            'Content-Type': 'application/json',
            'User-Agent': 'DomainChat/1.0'
        }
    
    @abstractmethod
    def authenticate(self):
        """Authenticate with the API service."""
        pass
    
    @abstractmethod
    def make_request(self, endpoint: str, params: Optional[Dict] = None):
        """Make a request to the API endpoint."""
        pass
    
    def _handle_response(self, response: requests.Response):
        """Handle API response with error checking."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            raise
        except Exception as err:
            logger.error(f"Other error occurred: {err}")
            raise

class FinanceAPI(BaseAPI):
    """API integration for financial data services."""
    
    BASE_URL = "https://api.examplefinance.com/v1"
    
    def authenticate(self):
        api_key = os.getenv('FINANCE_API_KEY') or self.config.get('api_key')
        if not api_key:
            raise ValueError("Finance API key not configured")
        self.session.headers.update({'X-API-KEY': api_key})
    
    def make_request(self, endpoint: str, params: Optional[Dict] = None):
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Finance API request failed: {e}")
            return None
    
    def get_stock_quote(self, symbol: str):
        """Get current stock quote for a symbol."""
        return self.make_request(f"stocks/{symbol}/quote")
    
    def get_market_news(self, limit: int = 5):
        """Get recent market news articles."""
        return self.make_request("news/market", {'limit': limit})

class MedicalAPI(BaseAPI):
    """API integration for medical information services."""
    
    BASE_URL = "https://api.examplemedical.com/v2"
    
    def authenticate(self):
        client_id = os.getenv('MEDICAL_API_CLIENT_ID') or self.config.get('client_id')
        client_secret = os.getenv('MEDICAL_API_CLIENT_SECRET') or self.config.get('client_secret')
        
        if not client_id or not client_secret:
            raise ValueError("Medical API credentials not configured")
            
        # Get OAuth token
        auth_url = f"{self.BASE_URL}/oauth/token"
        response = requests.post(auth_url, data={
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        })
        
        token_data = self._handle_response(response)
        self.session.headers.update({
            'Authorization': f"Bearer {token_data['access_token']}"
        })
    
    def make_request(self, endpoint: str, params: Optional[Dict] = None):
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Medical API request failed: {e}")
            return None
    
    def search_medical_info(self, query: str):
        """Search for medical information."""
        return self.make_request("information/search", {'q': query})
    
    def get_symptom_check(self, symptoms: list):
        """Get information about symptoms."""
        return self.make_request("symptoms/check", {'symptoms': ','.join(symptoms)})

class AgricultureAPI(BaseAPI):
    """API integration for agricultural data services."""
    
    BASE_URL = "https://api.exampleagri.com/v3"
    
    def authenticate(self):
        api_key = os.getenv('AGRICULTURE_API_KEY') or self.config.get('api_key')
        if not api_key:
            raise ValueError("Agriculture API key not configured")
        self.session.headers.update({'X-API-KEY': api_key})
    
    def make_request(self, endpoint: str, params: Optional[Dict] = None):
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Agriculture API request failed: {e}")
            return None
    
    def get_crop_info(self, crop_name: str):
        """Get information about specific crops."""
        return self.make_request(f"crops/{crop_name}")
    
    def get_weather_impact(self, location: str, crop: str):
        """Get weather impact analysis for crops."""
        return self.make_request("weather/impact", {
            'location': location,
            'crop': crop
        })

class ShoppingAPI(BaseAPI):
    """API integration for e-commerce services."""
    
    BASE_URL = "https://api.exampleshopping.com/v1"
    
    def authenticate(self):
        affiliate_id = os.getenv('SHOPPING_AFFILIATE_ID') or self.config.get('affiliate_id')
        if not affiliate_id:
            raise ValueError("Shopping affiliate ID not configured")
        self.session.headers.update({'X-Affiliate-ID': affiliate_id})
    
    def make_request(self, endpoint: str, params: Optional[Dict] = None):
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            response = self.session.get(url, params=params)
            return self._handle_response(response)
        except Exception as e:
            logger.error(f"Shopping API request failed: {e}")
            return None
    
    def search_products(self, query: str, limit: int = 5):
        """Search for products."""
        return self.make_request("products/search", {
            'q': query,
            'limit': limit
        })
    
    def get_product_details(self, product_id: str):
        """Get detailed product information."""
        return self.make_request(f"products/{product_id}")

# Additional API classes follow the same pattern for other domains
class EducationAPI(BaseAPI):
    """API integration for educational resources."""
    pass

class LegalAPI(BaseAPI):
    """API integration for legal information."""
    pass

class SustainabilityAPI(BaseAPI):
    """API integration for sustainability data."""
    pass

class TravelAPI(BaseAPI):
    """API integration for travel services."""
    pass

class HRAPI(BaseAPI):
    """API integration for HR services."""
    pass

class MentalHealthAPI(BaseAPI):
    """API integration for mental health resources."""
    pass