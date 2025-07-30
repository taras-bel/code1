#!/usr/bin/env python3
"""
SSL Certificate Generator for NoaMetrics
Generates self-signed SSL certificates for local development
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

def check_cryptography():
    """Check if cryptography is available and install if needed"""
    try:
        import cryptography
        return True
    except ImportError:
        print("Cryptography not found. Attempting to install...")
        
        # Try to install cryptography
        try:
            import subprocess
            import sys
            
            # Try pip3 first
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "cryptography"])
                return True
            except subprocess.CalledProcessError:
                print("Failed to install cryptography with pip")
                return False
                
        except Exception as e:
            print(f"Error installing cryptography: {e}")
            return False

def generate_certificates():
    """Generate self-signed SSL certificates"""
    
    # Check if cryptography is available
    if not check_cryptography():
        print("❌ Cryptography library not available. Please install it manually:")
        print("   apt install python3-cryptography")
        print("   or")
        print("   pip3 install cryptography --break-system-packages")
        return False
    
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
    except ImportError as e:
        print(f"❌ Error importing cryptography: {e}")
        return False
    
    # Create ssl directory if it doesn't exist
    ssl_dir = Path("ssl")
    ssl_dir.mkdir(exist_ok=True)
    
    # Generate private key
    print("🔑 Generating private key...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    
    # Generate certificate
    print("📜 Generating certificate...")
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "CA"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "NoaMetrics"),
        x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.now()
    ).not_valid_after(
        datetime.now() + timedelta(days=365)
    ).add_extension(
        x509.SubjectAlternativeName([
            x509.DNSName("localhost"),
        ]),
        critical=False,
    ).sign(private_key, hashes.SHA256())
    
    # Save private key
    print("💾 Saving private key...")
    with open(ssl_dir / "key.pem", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Save certificate
    print("💾 Saving certificate...")
    with open(ssl_dir / "cert.pem", "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))
    
    # Set proper permissions
    os.chmod(ssl_dir / "key.pem", 0o600)
    os.chmod(ssl_dir / "cert.pem", 0o644)
    
    print("✅ SSL certificates generated successfully!")
    print(f"   Certificate: {ssl_dir / 'cert.pem'}")
    print(f"   Private key: {ssl_dir / 'key.pem'}")
    
    return True

if __name__ == "__main__":
    print("🔧 Generating SSL certificates for NoaMetrics...")
    
    if generate_certificates():
        print("\n🎉 SSL certificates are ready!")
        print("⚠️  Note: These are self-signed certificates for development only.")
        print("   Your browser will show a security warning - this is normal.")
        print("   Click 'Advanced' and 'Proceed to localhost' to access the application.")
    else:
        print("\n❌ Failed to generate SSL certificates.")
        sys.exit(1) 