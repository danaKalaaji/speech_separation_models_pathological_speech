# Pathological speech detection

Relevant folders:
- PC-GITA_per_task_16000Hz: folder containing
  - The dataset we are working with in the subfolders sentences and sentences2
  - The created subfolder text_files containing all the possible combination of audio along with the values of alpha, beta, SNR, and duration
  - The subfolder processed_audio containing a subfolder per scenario each containing a text file where each line corresponds to the two audio processed along with the SI-SDR of the the mix audio after going through Sepformer and through ReSepformer
  - The excel file PCGITA_allmetadata containing additional information on the dataset
- text_files_values_generated: folder containing the text files with the values of alpha, beta, SNR, duration generated that we use for audio processing. To be used if the corresponding folder in PC-GITA_per_task_16000Hz has been modified.
- Folder PC-GITA_per_task_16000Hz-untouched: the original dataset before downsampling and with some audios we won't use

Relevant files:
- Generate.txt.files.ipynb: The code for creating the directories and text files, downsampling the dataset, and updating the text files with random values of SNR for each audio combination and the corresponding values of alpha, beta and duration
- Code.ipynb : The code for processing the files
- Pathological speech detection.odp: PowerPoint showcasing the results for 3 audio combination per scenario
