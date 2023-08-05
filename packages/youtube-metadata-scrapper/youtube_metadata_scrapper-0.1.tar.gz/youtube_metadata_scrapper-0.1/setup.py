from distutils.core import setup
setup(
  name = 'youtube_metadata_scrapper',         # How you named your package folder (MyLib)
  packages = ['youtube_metadata_scrapper'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'a simple celery worker that youtube_metadata_scrapper',   # Give a short description about your library
  author = 'Nicolas Herbaut',                   # Type in your name
  author_email = 'nicolas.herbaut@univ-paris1.fr',      # Type in your E-Mail
  url = 'https://github.com/stream-for-good/youtube-metadata-scrapper',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['youtube', 'metadata', 'scrapper'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          "amqp==5.0.6",
          "billiard==3.6.4.0",
          "cachetools==4.2.1",
          "celery==5.0.5",
          "certifi==2020.12.5",
          "chardet==4.0.0",
          "click==7.1.2",
          "click-didyoumean==0.0.3",
          "click-plugins==1.1.1",
          "click-repl==0.1.6",
          "google-api-core==1.26.3",
          "google-api-python-client==2.2.0",
          "google-auth==1.29.0",
          "google-auth-httplib2==0.1.0",
          "google-auth-oauthlib==0.4.4",
          "googleapis-common-protos==1.53.0",
          "httplib2==0.19.1",
          "idna==2.10",
          "importlib-metadata==4.0.1",
          "kombu==5.0.2",
          "munch==2.5.0",
          "oauthlib==3.1.0",
          "packaging==20.9",
          "prompt-toolkit==3.0.18",
          "protobuf==3.15.8",
          "pyasn1==0.4.8",
          "pyasn1-modules==0.2.8",
          "pyparsing==2.4.7",
          "pytz==2021.1",
          "requests==2.25.1",
          "requests-oauthlib==1.3.0",
          "rsa==4.7.2",
          "six==1.15.0",
          "typing-extensions==3.7.4.3",
          "uritemplate==3.0.1",
          "urllib3==1.26.4",
          "vine==5.0.0",
          "wcwidth==0.2.5",
          "zipp==3.4.1",
          "docker==4.4.4"
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
