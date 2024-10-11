# Evaluating Performance of Pathological Speech Detection 

Relevant folders:
- PC-GITA_per_task_16000Hz: folder containing
  - The subfolder text_files containing a subfolder per scenario, each containing all the possible combination of audio along with the values of alpha, beta, SNR, and duration
  - The subfolder processed_audio containing a subfolder per scenario, each containing a text file where each line corresponds to the two audio processed along with the SI-SDR of the the mix audio before and after going through Sepformer and through ReSepformer
  - The subfolder processed_audio_example containing a subfolder per scenario, each containing the processed data text files for three audios pairs per scenarios along with the audio signals before and after separation

Relevant files:
- Generate.txt.files.ipynb: The code for creating the directories and text files, downsampling the dataset, and updating the text files with random values of SNR for each audio combination and the corresponding values of alpha, beta and duration
- Code.py : The code for processing the files and computing the performance
- Analysis.ipynb : The code for analyzing the results
- Idiap_Dana_Report.pdf: Project's report
