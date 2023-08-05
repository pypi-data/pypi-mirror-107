# Gesundheit për tutti

This project consists in a chatbot that aims to help people that may have some limits to access information about services related to health in South Tyrol, such as medical services, available doctors and open pharmacies. The program accepts text, audio and image input in different languages. The user will get the results as on-screen text or audio according to his/her input and language choice.

Since the aim of this project is to improve accessibility, this chatbot can be easily used by immmigrants, teenagers, elderly people or phisically challenged people.

Here you can find image and audio files to try out different kind of input: https://drive.google.com/drive/folders/1xHndS1OlaZyqfxz1ytqpy08N0-mK0onh?usp=sharing

Once the package is installed, make sure that the following dependencies are installed:

      - pip install googletrans==3.1.0a0 (to be installed manually)
      - pip install ibm_watson (to be installed manually)
      - pip install word2number (to be installed manually)
  

API and libraries used in the code:

    - Translator (from googletrans)
    - gTTS (from gtts)
    - SpeechToTextV1 (from ibm_watson)
    - IAMAuthenticator (from ibm_cloud_sdk_core.authenticators)
    - easyocr (from easyocr)
    - w2n (from word2number)
    - Health services http://dati.retecivica.bz.it/it/dataset southtyrolean-health-activities-list
    - Available doctors http://dati.retecivica.bz.it/it/dataset/southtyrolean-doctors-on-duty
    - Open pharmacies http://dati.retecivica.bz.it/it/dataset/farmacie-di-turno-dell-alto-adige1
  

In the function section you will find two function that need to be completed:

     - audio_input(audio, Model) >  APIkey and url
     - image_input() > insert the directory of the folder in your drive in which the files were saved 

Once it's done, you can run all the functions in the section.
  
After that you will be able to call the function gesundheit(): in order to start using the chatbot.  
