# Copyright (c) 2025 Damien Boisvert (AlphaGameDeveloper)
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
from unittest import mock
import sys
import os
import json
import logging

# Add parent directory to path to import notifications module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from notifications import NotificationManager

# Configure logging for tests
logging.basicConfig(level=logging.CRITICAL)

class TestNotificationManager(unittest.TestCase):
    def setUp(self):
        self.webhook_url = "https://discord.com/api/webhooks/test"
        self.valid_webhook_response = {
            "name": "Test Webhook",
            "id": "123456789",
            "type": 1,
            "channel_id": "123456789",
            "guild_id": "123456789"
        }
    
    @mock.patch('notifications.http_get')
    def test_init_valid_webhook(self, mock_get):
        # Mock successful response
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.valid_webhook_response
        mock_get.return_value = mock_response
        
        # Test initialization with valid webhook
        manager = NotificationManager(discord_webhook_url=self.webhook_url)
        mock_get.assert_called_once_with(self.webhook_url)
        self.assertEqual(manager.discord_webhook_url, self.webhook_url)
    
    @mock.patch('notifications.http_get')
    def test_init_invalid_webhook_status_code(self, mock_get):
        # Mock HTTP error response
        mock_response = mock.Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Test initialization with invalid webhook (bad status code)
        with self.assertRaises(ValueError) as context:
            NotificationManager(discord_webhook_url=self.webhook_url)
        
        self.assertIn("Discord webhook URL is not valid", str(context.exception))
        mock_get.assert_called_once_with(self.webhook_url)
    
    @mock.patch('notifications.http_get')
    def test_init_webhook_connection_error(self, mock_get):
        # Mock connection error
        mock_get.side_effect = Exception("Connection error")
        
        # Test initialization with invalid webhook (connection error)
        with self.assertRaises(ValueError) as context:
            NotificationManager(discord_webhook_url=self.webhook_url)
        
        self.assertIn("Discord webhook URL is not valid", str(context.exception))
        mock_get.assert_called_once_with(self.webhook_url)
    
    def test_init_no_webhook(self):
        # Test initialization with no webhook
        manager = NotificationManager(discord_webhook_url=None)
        self.assertIsNone(manager.discord_webhook_url)
    
    @mock.patch('notifications.http_post')
    @mock.patch('notifications.http_get')
    def test_send_notification_text_only(self, mock_get, mock_post):
        # Mock successful initialization
        mock_get_response = mock.Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = self.valid_webhook_response
        mock_get.return_value = mock_get_response
        
        # Mock successful notification
        mock_post_response = mock.Mock()
        mock_post_response.status_code = 204
        mock_post.return_value = mock_post_response
        
        # Initialize manager and send notification
        manager = NotificationManager(discord_webhook_url=self.webhook_url)
        message = "Test notification message"
        manager.send_notification(message)
        
        # Verify the post request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], self.webhook_url)
        self.assertEqual(call_args[1]["json"]["content"], message)
    
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data=b'test image data')
    @mock.patch('notifications.http_post')
    @mock.patch('notifications.http_get')
    def test_send_notification_with_image(self, mock_get, mock_post, mock_file):
        # Mock successful initialization
        mock_get_response = mock.Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = self.valid_webhook_response
        mock_get.return_value = mock_get_response
        
        # Mock successful notification with image
        mock_post_response = mock.Mock()
        mock_post_response.status_code = 204
        mock_post.return_value = mock_post_response
        
        # Initialize manager and send notification with image
        manager = NotificationManager(discord_webhook_url=self.webhook_url)
        message = "Test notification with image"
        image_path = "test_image.png"
        manager.send_notification(message, image_path=image_path)
        
        # Verify the file was opened
        mock_file.assert_called_once_with(image_path, 'rb')
        
        # Verify the post request was made correctly
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertEqual(call_args[0][0], self.webhook_url)
        self.assertEqual(call_args[1]["data"]["content"], message)
        self.assertIn("files", call_args[1])
    
    @mock.patch('notifications.http_post')
    @mock.patch('notifications.http_get')
    def test_send_notification_failure(self, mock_get, mock_post):
        # Mock successful initialization
        mock_get_response = mock.Mock()
        mock_get_response.status_code = 200
        mock_get_response.json.return_value = self.valid_webhook_response
        mock_get.return_value = mock_get_response
        
        # Mock failed notification
        mock_post_response = mock.Mock()
        mock_post_response.status_code = 400
        mock_post_response.text = "Bad Request"
        mock_post.return_value = mock_post_response
        
        # Initialize manager and send notification
        manager = NotificationManager(discord_webhook_url=self.webhook_url)
        with self.assertLogs(logger='notifications', level='ERROR') as cm:
            manager.send_notification("Test failed notification")
        
        # Check that error was logged
        self.assertIn("Failed to send notification", cm.output[0])
    
    @mock.patch('notifications.http_get')
    def test_send_notification_no_webhook(self, mock_get):
        # Test sending notification with no webhook
        manager = NotificationManager(discord_webhook_url=None)
        with self.assertLogs(logger='notifications', level='WARNING') as cm:
            manager.send_notification("Test notification")
        
        # Check that warning was logged
        self.assertIn("No Discord webhook URL provided", cm.output[0])
        # Ensure no HTTP request was made
        mock_get.assert_not_called()

if __name__ == '__main__':
    unittest.main()

