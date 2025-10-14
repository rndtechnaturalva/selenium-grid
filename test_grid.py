"""
Example Python test script for Selenium Grid
Run tests against the Docker Compose Selenium Grid
"""

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


class TestSeleniumGrid:
    
    # Grid URL - update if your grid is running elsewhere
    GRID_URL = "http://localhost:4444/wd/hub"
    
    @pytest.fixture(params=["chrome", "firefox", "edge"])
    def driver(self, request):
        """Fixture that provides WebDriver instances for different browsers"""
        browser = request.param
        
        if browser == "chrome":
            options = ChromeOptions()
            options.add_argument("--headless")  # Remove for GUI mode
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Remote(
                command_executor=self.GRID_URL,
                options=options
            )
        elif browser == "firefox":
            options = FirefoxOptions()
            options.add_argument("--headless")  # Remove for GUI mode
            driver = webdriver.Remote(
                command_executor=self.GRID_URL,
                options=options
            )
        elif browser == "edge":
            options = EdgeOptions()
            options.add_argument("--headless")  # Remove for GUI mode
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Remote(
                command_executor=self.GRID_URL,
                options=options
            )
        
        yield driver
        driver.quit()
    
    def test_google_search(self, driver):
        """Test Google search functionality"""
        driver.get("https://www.google.com")
        
        # Accept cookies if present (for GDPR compliance)
        try:
            accept_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'I agree')]"))
            )
            accept_button.click()
        except:
            pass  # No cookies dialog found
        
        # Find search box and perform search
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        search_box.send_keys("Selenium Grid Docker")
        search_box.submit()
        
        # Wait for results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search"))
        )
        
        assert "Selenium Grid Docker" in driver.title
    
    def test_example_com(self, driver):
        """Test example.com website"""
        driver.get("https://example.com")
        
        # Check title
        assert "Example Domain" in driver.title
        
        # Check heading
        heading = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        assert "Example Domain" in heading.text
    
    def test_httpbin_user_agent(self, driver):
        """Test user agent detection"""
        driver.get("https://httpbin.org/user-agent")
        
        # Get the response body
        body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "pre"))
        )
        
        response_text = body.text.lower()
        
        # Check that response contains user agent info
        assert "user-agent" in response_text
        
        # Check browser-specific user agent strings
        browser_name = driver.capabilities.get('browserName', '').lower()
        if browser_name == 'chrome':
            assert 'chrome' in response_text
        elif browser_name == 'firefox':
            assert 'firefox' in response_text
        elif browser_name == 'msedge':
            assert 'edge' in response_text


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])