from setuptools import setup, find_packages

setup(
    name="OOP_Asekron",            # Paket adınız
    version="0.1.0",               # Paket versiyonu
    description="OOP Asekron için kısa açıklama",  # README dosyasından uzun açıklama alabilirsiniz
    long_description_content_type="text/markdown",  # README dosyanız markdown formatındaysa
    author="Adınız Soyadınız",     # Paket yazarınız
    author_email="email@example.com",  # İletişim e-posta adresiniz
    url="https://github.com/EnsarYazici/EnsarPyTools",  # Projenizin GitHub URL'si
    packages=find_packages(),      # Otomatik olarak tüm alt paketleri bulur
    install_requires=[             # Paketinizin bağımlılıklarını burada belirtebilirsiniz
        # Örnek: "requests>=2.25.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Lisans tipiniz
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",       # Gereken minimum Python versiyonu
)
