"""
Storage Utilities
Handle file storage and image processing
"""
import os
import base64
from pathlib import Path
from typing import Optional, Tuple
import uuid

class FileStorage:
    """Manage file storage operations"""
    
    def __init__(self, storage_dir: str = "storage"):
        """Initialize file storage"""
        self.storage_dir = Path(storage_dir)
        self.image_dir = self.storage_dir / "images"
        self.temp_dir = self.storage_dir / "temp"
        
        # Create directories
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
    
    def save_uploaded_image(
        self,
        image_bytes: bytes,
        filename: Optional[str] = None
    ) -> Tuple[bool, str, str]:
        """
        Save uploaded image
        
        Returns:
            (success, file_path, error_message)
        """
        try:
            if not filename:
                filename = f"{uuid.uuid4()}.jpg"
            
            # Ensure safe filename
            filename = self._sanitize_filename(filename)
            filepath = self.image_dir / filename
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(image_bytes)
            
            return True, str(filepath), ""
        
        except Exception as e:
            return False, "", str(e)
    
    def save_base64_image(
        self,
        base64_string: str,
        filename: Optional[str] = None
    ) -> Tuple[bool, str, str]:
        """
        Save base64 encoded image
        
        Returns:
            (success, file_path, error_message)
        """
        try:
            # Remove data URL prefix if present
            if ',' in base64_string:
                base64_string = base64_string.split(',')[1]
            
            # Decode base64
            image_bytes = base64.b64decode(base64_string)
            
            return self.save_uploaded_image(image_bytes, filename)
        
        except Exception as e:
            return False, "", f"Failed to decode base64: {str(e)}"
    
    def get_image_base64(self, filepath: str) -> Optional[str]:
        """Convert image to base64 string"""
        try:
            with open(filepath, 'rb') as f:
                image_bytes = f.read()
            return base64.b64encode(image_bytes).decode('utf-8')
        except Exception as e:
            print(f"Error reading image: {e}")
            return None
    
    def delete_file(self, filepath: str) -> bool:
        """Delete a file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
    
    def cleanup_temp_files(self, max_age_hours: int = 24) -> None:
        """Clean up temporary files older than specified hours"""
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        for filepath in self.temp_dir.glob('*'):
            try:
                file_age = current_time - filepath.stat().st_mtime
                if file_age > max_age_seconds:
                    filepath.unlink()
            except Exception as e:
                print(f"Error cleaning up {filepath}: {e}")
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename to prevent path traversal"""
        # Remove any path components
        filename = os.path.basename(filename)
        # Remove potentially dangerous characters
        filename = "".join(c for c in filename if c.isalnum() or c in '._-')
        # Ensure it has an extension
        if '.' not in filename:
            filename += '.jpg'
        return filename
    
    def get_storage_stats(self) -> dict:
        """Get storage statistics"""
        total_files = 0
        total_size = 0
        
        for filepath in self.storage_dir.rglob('*'):
            if filepath.is_file():
                total_files += 1
                total_size += filepath.stat().st_size
        
        return {
            'total_files': total_files,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'image_count': len(list(self.image_dir.glob('*')))
        }