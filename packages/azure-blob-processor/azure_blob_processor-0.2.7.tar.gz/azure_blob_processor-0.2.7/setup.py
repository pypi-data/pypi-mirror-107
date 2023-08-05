from setuptools import setup
setup(
  name = 'azure_blob_processor',        
  packages = ['azure_blob_processor'],  
  version = '0.2.7',      
  license='MIT',        
  description = 'Library to process file in Azure blob storage',   
  author = 'Zhenbo Zhang',                  
  author_email = 'zhenbo.zhang@outlook.com',     
  url = 'https://github.com/zhenbzha/azure-blob-processor',  
  download_url = 'https://github.com/zhenbzha/azure-blob-processor',    
  keywords = ['Azure', 'blob'], 
  install_requires=[         
          'azure-storage-blob==12.8.1',
          'aiofile==3.5.0',
          'aiohttp==3.7.4.post0'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',    
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)