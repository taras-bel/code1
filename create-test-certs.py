#!/usr/bin/env python3
"""
Создание тестовых SSL сертификатов для HTTPS
"""
import os
import subprocess
import sys

def create_test_certs():
    """Создает тестовые SSL сертификаты"""
    print("🔐 Создание тестовых SSL сертификатов...")
    
    # Создаем директорию ssl
    if not os.path.exists('ssl'):
        os.makedirs('ssl')
        print("✅ Создана директория ssl")
    
    # Генерируем самоподписанный сертификат
    try:
        # Используем Python для создания сертификата
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import rsa
        from datetime import datetime, timedelta
        
        print("🔐 Генерация RSA ключа...")
        # Генерируем приватный ключ
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        print("🔐 Создание сертификата...")
        # Создаем сертификат
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "RU"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Moscow"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Moscow"),
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
        
        print("💾 Сохранение сертификатов...")
        # Сохраняем приватный ключ
        with open("ssl/key.pem", "wb") as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        # Сохраняем сертификат
        with open("ssl/cert.pem", "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        print("✅ Тестовые SSL сертификаты созданы!")
        print("   - ssl/cert.pem (сертификат)")
        print("   - ssl/key.pem (приватный ключ)")
        return True
        
    except ImportError:
        print("❌ Модуль cryptography не установлен")
        print("📦 Установите: pip install cryptography")
        return False
    except Exception as e:
        print(f"❌ Ошибка создания сертификатов: {e}")
        return False

if __name__ == "__main__":
    success = create_test_certs()
    if success:
        print("\n🎉 Сертификаты готовы! Теперь можно запускать HTTPS")
    else:
        print("\n❌ Не удалось создать сертификаты")
        sys.exit(1) 