import io
import base64
import qrcode
from qrcode.constants import ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q, ERROR_CORRECT_H


class QRService:
    
    ERROR_CORRECTION_MAP = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }
    
    def generate_qr_code(self, 
                         url: str,
                         size: int = 400,
                         error_correction: str = "M",
                         border: int = 4,
                         ) -> bytes:
        """
        Generate QR code as PNG bytes.
        
        Args:
            url: URL to encode in QR code
            size: Size of QR code in pixels (100-1000)
            error_correction: Error correction level (L, M, Q, H)
            border: Border size in boxes (1-10)
            
        Returns:
            PNG image as bytes
            
        Raises:
            ValueError: If parameters are invalid
        """
        
        if not url or not url.strip():
            raise ValueError("URL cannot be empty")
        
        if len(url) > 2048:
            raise ValueError("URL exceeds maximum length of 2048 characters")
        
        if not isinstance(size, int) or not (100 <= size <= 1000):
            raise ValueError("Size must be an integer between 100 and 1000")
        
        error_correction_upper = error_correction.upper()
        if error_correction_upper not in self.ERROR_CORRECTION_MAP:
            raise ValueError("Invalid error correction level")
        
        if not isinstance(border, int) or not (0 <= border <= 10):
            raise ValueError("Border must be an integer between 0 and 10")
        
        error_correction_code = self.ERROR_CORRECTION_MAP[error_correction_upper]
        box_size = max(1, size // 25)
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=box_size,
                border=border,
            )
            
            qr.add_data(url)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            # convert to bytes 
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)

            return img_bytes.getvalue()
        
        except Exception as e:
            raise ValueError(f"Failed to generate QR code: {str(e)}") from e
        
    
    def generate_qr_code_base64(self, url: str, size: int = 400, error_correction: str = "M", border: int = 4) -> str:
        """
        Generate a QR code for a given URL and return it as a base64 encoded string.
        
        Args:
            url: The URL to generate a QR code for
            size: The size of the QR code
            error_correction: The error correction level
            border: The border size
        """
        img_bytes = self.generate_qr_code(url, size, error_correction, border)
        return base64.b64encode(img_bytes).decode("utf-8")