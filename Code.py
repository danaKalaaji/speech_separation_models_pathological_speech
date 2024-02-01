# %%
import os
import numpy as np
from speechbrain.pretrained import SepformerSeparation as separator
import torch
import torchaudio
from torchmetrics.audio import ScaleInvariantSignalDistortionRatio
from mir_eval.separation import bss_eval_sources
import joblib 

# %%
''' Generates x different random numbers between 0 and max'''

def generate_x_random_numbers(x, max):
    numbers = [] 
    while len(numbers) < x:
        number = np.random.randint(0, max)
        if number not in numbers:
            numbers.append(number)
    return numbers

# %%
''' Runs the SepFormer algorithm on the signal y'''

def audio_through_Sepformer(y):
    sepformer = separator.from_hparams(source="speechbrain/sepformer-wsj02mix")
    print("Separating the audio with Sepformer...")

    # if parameter y is a path to the audio file
    #y, sr = torchaudio.load(y_path)
    #if sr != 8000:
    #    raise ValueError("Sampling rate must be 8000 Hz")
    
    y_hat = sepformer.separate_batch(y)
    x1_s = y_hat[:, :, 0].detach().cpu()
    x2_s = y_hat[:, :, 1].detach().cpu()
    
    print("Done")
    return x1_s, x2_s

# %%
''' Runs the RE-SepFormer algorithm on the signal y'''

def audio_through_Resepformer(y):
    resepformer = separator.from_hparams(source="speechbrain/resepformer-wsj02mix")
    print("Separating the audio with ReSepformer...")

    # if parameter y is a path to the audio file
    #y, sr = torchaudio.load(y_path)
    #if sr != 8000:
    #    raise ValueError("Sampling rate sr must be 8000 Hz")

    y_hat = resepformer.separate_batch(y)
    x1_r = y_hat[:, :, 0].detach().cpu()
    x2_r = y_hat[:, :, 1].detach().cpu()

    print("Done")
    return x1_r, x2_r

# %%
''' Computes the SI-SDR, this function is not used in the code but was implemented to 
    verify that the values computed by the torchmetric function yields the same results'''

def SI_SDR(prediction, target):   
    #(yields same results as torchmetric function)
    a = torch.sum(target * prediction) / torch.sum(target**2) 
    num = torch.sum((a * target)**2)
    denum = torch.sum(((a * target) - prediction)**2) 
    SI_SDR = 10 * torch.log10(num/denum)
    
    return SI_SDR


# %%
def SDR(prediction, target):  
    try:
        target_data = target.cpu().numpy()
        prediction_data = prediction.cpu().numpy()
        sdr, _, _, _  = bss_eval_sources(target_data, prediction_data)
        SDR = np.mean(sdr) # In our case we only have 1 source so no need to average
        return SDR

    except Exception as e:
            print(f"An error occurred: {e}")
            raise 


# %%
''' 
Processes a number lines_processed_per_file of audio pairs of the text file of for scenario
These text files are located in text_file_dir
The results of the processed signals are written in a separate text_file located in processed_audio_dir

If lines_processed_per_file = 0, process all the lines in the text files
'''

def process_x_audio_pair(base_dir, text_file_dir, processed_audio_dir, lines_processed_per_file):
    # Iterate through all the text files in the text_file_dir directory
    for filename in os.listdir(text_file_dir):
        if filename.endswith(".txt"):    # or if filename == "specific_file": 
            text_file_path = os.path.join(text_file_dir, filename)

            # Get the right path for saving the processed audio files
            sub_dir_name = os.path.splitext(filename)[0]  #removes the .txt extension
            sub_processed_audio_dir_ = os.path.join(processed_audio_dir, sub_dir_name)
            path_text_file_processed = os.path.join(sub_processed_audio_dir_, filename)

            print(f"Processing {filename}")   
            # Pick at random the index of the lines to be processed
            with open(text_file_path, "r") as text_file:
                lines = text_file.readlines()
              
                with open(path_text_file_processed, "a") as processed_file:
                # If lines_processed_per_file = 0, process all the lines in the text files
                    if lines_processed_per_file == 0:
                        processed_lines_index = [i for i in range(len(lines))]
                        print(f"-Number of processed lines in {filename} : {len(processed_lines_index)} ")
                        processed_file.write(f"{len(processed_lines_index)} \n")
                    else:
                        processed_lines_index = generate_x_random_numbers(lines_processed_per_file, len(lines))
                        print(f"-Processed lines in {filename} : {processed_lines_index} ")
                        processed_file.write(f"{processed_lines_index} \n")
  
                # Process the audios of each line chosen at random
                for i in processed_lines_index:

                    # Create the subdirectory for saving the processed audio files if it does not exist
                    sub_processed_audio_dir = os.path.join(sub_processed_audio_dir_, f"{i}")
                    if not os.path.exists(sub_processed_audio_dir):
                        os.makedirs(sub_processed_audio_dir)

                        # Get the audio files paths and the parameters of the line
                        print(f"-- Line {i}:")
                        line = lines[i].split()
                        audio1_path, alpha, audio2_path, beta, SNR, duration = line
                        alpha = float(alpha)
                        beta = float(beta)
                        duration = int(duration)
                        
                        # Create the paths for saving the processed audio files
                        x1_path = os.path.join(sub_processed_audio_dir, f"{i}_x1.wav")
                        x2_path = os.path.join(sub_processed_audio_dir, f"{i}_x2.wav")
                        y_path = os.path.join(sub_processed_audio_dir, f"{i}_y.wav")
                        x1_s_path = os.path.join(sub_processed_audio_dir, f"{i}_x1_s.wav")
                        x2_s_path = os.path.join(sub_processed_audio_dir, f"{i}_x2_s.wav")
                        x1_r_path = os.path.join(sub_processed_audio_dir, f"{i}_x1_r.wav")
                        x2_r_path = os.path.join(sub_processed_audio_dir, f"{i}_x2_r.wav")

                        # Calculate and save the mix audio signal and the original audio signals
                        audio1_path_windows = audio1_path
                        audio2_path_windows = audio2_path
                        audio1_path = audio1_path.replace('\\', '/')
                        audio2_path = audio2_path.replace('\\', '/')
                        audio1_path = os.path.join(base_dir, audio1_path)
                        audio2_path = os.path.join(base_dir, audio2_path)

                        audio1, sr1 = torchaudio.load(audio1_path)
                        audio2, sr2 = torchaudio.load(audio2_path)

                        # Check if the sampling rates are 8000 Hz
                        if sr1 != 8000:
                            raise ValueError("Sampling rate r1 must be 8000 Hz")
                        if sr2 != 8000:
                            raise ValueError("Sampling rate r2 must be 8000 Hz")
                        
                        # Calculate the mix audio
                        x1 = alpha * audio1[:, :duration]
                        x2 = beta * audio2[:, :duration]
                        y = x1 + x2
                        
                        torchaudio.save(x1_path, x1, 8000, format='wav')
                        torchaudio.save(x2_path, x2, 8000, format='wav')
                        torchaudio.save(y_path, y, 8000, format='wav')

                        # Calculate and save the separated audios obtained after Sepformer
                        x1_s, x2_s = audio_through_Sepformer(y)
                        torchaudio.save(x1_s_path, x1_s, 8000, format='wav') 
                        torchaudio.save(x2_s_path, x2_s, 8000, format='wav')
                    
                        # Calculate and save the the separated audios obtained after Resepformer
                        x1_r, x2_r = audio_through_Resepformer(y)
                        torchaudio.save(x1_r_path, x1_r, 8000, format='wav')
                        torchaudio.save(x2_r_path, x2_r, 8000, format='wav')
                        
                        # Calculate the SI_SDR of the audio through Sepformer and Resepformer
                        #print("Calculating the SI_SDR...")
                        si_sdr = ScaleInvariantSignalDistortionRatio()

                        # SISDR for audio without separation
                        SI_SDR_y = si_sdr(y, x1)
                        print(f"SI_SDR For Audio Without Speech Separation: {SI_SDR_y}")  
                        
                        # SISDR for audio through Sepformer
                        SI_SDR_x1_s = si_sdr(x1_s, x1)
                        SI_SDR_x2_s = si_sdr(x2_s, x1)
                        SI_SDR_sep = max(SI_SDR_x1_s, SI_SDR_x2_s)
                        print(f"SI_SDR For Audio Through Sepformer: {SI_SDR_sep} was {SI_SDR_x1_s} and {SI_SDR_x2_s}")  
                        
                        # SISDR for audio through Resepformer
                        SI_SDR_x1_r = si_sdr(x1_r, x1)
                        SI_SDR_x2_r = si_sdr(x2_r, x1)
                        SI_SDR_resep = max(SI_SDR_x1_r, SI_SDR_x2_r)
                        print(f"SI_SDR For Audio Through Sepformer: {SI_SDR_resep} was {SI_SDR_x1_r} and {SI_SDR_x2_r}")  

                        # Save the index of the processed line and the SI_SDR through Sepformer and Resepformer
                        with open(path_text_file_processed, "a") as processed_file:
                            processed_file.write(f"{i} {audio1_path_windows} {audio2_path_windows} {SI_SDR_y} {SI_SDR_sep} {SI_SDR_resep} \n")
                    
                    else:
                        # If the subdirectory already exists, the line has already been processed
                        print(f"-- Line {i} already processed")
                        #processed_lines_index.remove(i)
                        #processed_lines_index.append(generate_x_random_numbers(1, len(lines))[0])


# %%

base_dir = r"/idiap/temp/dkalaaji/Dana_Kalaaji"
base_dir_PC = r"/idiap/temp/dkalaaji/Dana_Kalaaji/PC-GITA_per_task_16000Hz"
text_file_dir = os.path.join(base_dir_PC, "text_files")
processed_audio_dir = os.path.join(base_dir_PC, "processed_audio")

# Test to see that code began
joblib.dump({}, os.path.join(base_dir_PC, 'test_debut.pkl')) 

lines_processed_per_file = 0  # If set to 0, process all the lines in the files
processed_audio = process_x_audio_pair(base_dir, text_file_dir, processed_audio_dir, lines_processed_per_file)

# Test to see that code ended
joblib.dump({}, os.path.join(base_dir_PC, 'test_fin.pkl')) 
