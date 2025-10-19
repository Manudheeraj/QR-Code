"""
QR Code Generator Backend
Handles QR code generation with improved long-term file hosting
"""

import qrcode
from io import BytesIO
import requests
import json
class QRCodeGenerator:
    """Backend class that handles QR code generation logic."""
    
    def __init__(self, box_size=10, border=4):
        """
        Initialize the QR code generator with default settings.
        
        Args:
            box_size (int): Size of each box in the QR code
            border (int): Thickness of the border
        """
        self.box_size = box_size
        self.border = border
    
    def generate_qr_code(self, data, fill_color='black', back_color='white'):
        """
        Generate a QR code from any text or URL.
        
        Args:
            data (str): The text or URL to encode
            fill_color (str): Color of the QR code boxes
            back_color (str): Background color
            
        Returns:
            BytesIO: Image buffer containing the QR code PNG
            
        Raises:
            ValueError: If data is empty
            Exception: If QR code generation fails
        """
        if not data or not data.strip():
            raise ValueError("Data cannot be empty")
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=self.box_size,
                border=self.border,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            
            buf = BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            
            return buf
            
        except Exception as e:
            raise Exception(f"Failed to generate QR code: {str(e)}")
    
    def upload_file_and_get_link(self, file_bytes, filename):
        """
        Upload file to hosting service and get shareable link.
        Prioritizes services with LONGER expiration times.
        
        Args:
            file_bytes (bytes): The file content
            filename (str): Name of the file
            
        Returns:
            dict: Contains 'success', 'url', 'service', and 'message'
        """
        # Service 1: catbox.moe (PERMANENT - Best option!)
        try:
            url = self._upload_to_catbox(file_bytes, filename)
            if url:
                return {
                    'success': True,
                    'url': url,
                    'service': 'catbox.moe',
                    'message': '✓ PERMANENT link - Never expires!'
                }
        except Exception as e:
            print(f"catbox.moe failed: {e}")
        
        # Service 2: pixeldrain.com (90 days for free, permanent with account)
        try:
            url = self._upload_to_pixeldrain(file_bytes, filename)
            if url:
                return {
                    'success': True,
                    'url': url,
                    'service': 'pixeldrain.com',
                    'message': '✓ Link available for 90+ days'
                }
        except Exception as e:
            print(f"pixeldrain failed: {e}")
        
        # Service 3: 0x0.st (365 days - 1 year!)
        try:
            url = self._upload_to_0x0(file_bytes, filename)
            if url:
                return {
                    'success': True,
                    'url': url,
                    'service': '0x0.st',
                    'message': '✓ Link available for 365 days (1 year)'
                }
        except Exception as e:
            print(f"0x0.st failed: {e}")
        
        # Service 4: gofile.io (Good for larger files, 10+ days)
        try:
            url = self._upload_to_gofile(file_bytes, filename)
            if url:
                return {
                    'success': True,
                    'url': url,
                    'service': 'gofile.io',
                    'message': '✓ Link expires after 10 days of inactivity'
                }
        except Exception as e:
            print(f"gofile.io failed: {e}")
        
        # Service 5: file.io (Backup only - expires after download)
        try:
            url = self._upload_to_fileio(file_bytes, filename)
            if url:
                return {
                    'success': True,
                    'url': url,
                    'service': 'file.io',
                    'message': '⚠️ Link expires after FIRST download or 14 days'
                }
        except Exception as e:
            print(f"file.io failed: {e}")
        
        # All services failed
        return {
            'success': False,
            'url': None,
            'service': None,
            'message': '❌ All upload services failed. Please try again or use Google Drive/Dropbox.'
        }
    
    def _upload_to_catbox(self, file_bytes, filename):
        """Upload to catbox.moe - PERMANENT storage!"""
        files = {'fileToUpload': (filename, file_bytes)}
        data = {'reqtype': 'fileupload'}
        response = requests.post('https://catbox.moe/user/api.php', files=files, data=data, timeout=60)
        
        if response.status_code == 200 and response.text.startswith('https://'):
            return response.text.strip()
        return None
    
    def _upload_to_pixeldrain(self, file_bytes, filename):
        """Upload to pixeldrain.com - 90+ days storage."""
        files = {'file': (filename, file_bytes)}
        response = requests.post('https://pixeldrain.com/api/file', files=files, timeout=60)
        
        if response.status_code == 201:
            data = response.json()
            file_id = data.get('id')
            if file_id:
                return f'https://pixeldrain.com/u/{file_id}'
        return None
    
    def _upload_to_0x0(self, file_bytes, filename):
        """Upload to 0x0.st - 365 days storage."""
        files = {'file': (filename, file_bytes)}
        response = requests.post('https://0x0.st', files=files, timeout=30)
        
        if response.status_code == 200:
            return response.text.strip()
        return None
    
    def _upload_to_gofile(self, file_bytes, filename):
        """Upload to gofile.io service."""
        server_response = requests.get('https://api.gofile.io/getServer', timeout=10)
        if server_response.status_code != 200:
            return None
        
        server_data = server_response.json()
        if server_data.get('status') != 'ok':
            return None
        
        server = server_data['data']['server']
        
        files = {'file': (filename, file_bytes)}
        upload_response = requests.post(
            f'https://{server}.gofile.io/uploadFile',
            files=files,
            timeout=60
        )
        
        if upload_response.status_code == 200:
            data = upload_response.json()
            if data.get('status') == 'ok':
                return data['data']['downloadPage']
        return None
    
    def _upload_to_fileio(self, file_bytes, filename):
        """Upload to file.io service - BACKUP ONLY."""
        files = {'file': (filename, file_bytes)}
        response = requests.post('https://file.io', files=files, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                return data.get('link')
        return None
    
    def generate_qr_from_file(self, file_bytes, filename, fill_color='black', back_color='white'):
        """
        Upload any file and generate QR code from the link.
        
        Args:
            file_bytes (bytes): File content
            filename (str): File name (with extension)
            fill_color (str): QR code color
            back_color (str): Background color
            
        Returns:
            tuple: (qr_image_buffer, upload_info)
        """
        upload_result = self.upload_file_and_get_link(file_bytes, filename)
        
        if not upload_result['success']:
            raise Exception(upload_result['message'])
        
        qr_image = self.generate_qr_code(
            upload_result['url'],
            fill_color=fill_color,
            back_color=back_color
        )
        
        return qr_image, upload_result
    
    def update_settings(self, box_size=None, border=None):
        """Update the generator settings."""
        if box_size is not None:
            self.box_size = box_size
        if border is not None:
            self.border = border
    
    def save_to_file(self, qr_buffer, filename='qr_code.png'):
        """Save QR code buffer to a file."""
        qr_buffer.seek(0)
        with open(filename, 'wb') as f:
            f.write(qr_buffer.read())
        return filename


def create_qr_code(data, box_size=10, border=4, 
                   fill_color='black', back_color='white'):
    """Quick function to generate QR from text."""
    generator = QRCodeGenerator(box_size=box_size, border=border)
    return generator.generate_qr_code(data, fill_color, back_color)


if __name__ == "__main__":
    generator = QRCodeGenerator()
    
    print("Testing text QR code...")
    text_qr = generator.generate_qr_code("https://www.example.com")
    generator.save_to_file(text_qr, 'text_qr.png')
    print("✓ Text QR saved")
    
    print("\nTesting file upload...")
    test_file = b"Test PDF content here"
    result = generator.upload_file_and_get_link(test_file, "test.pdf")
    print(f"Upload result: {result}")