from pydub import AudioSegment
from bitarray import bitarray
import os
import pathlib

class EchoHiding:
    def encode(self,audioLocation,stringToEncode):
        samples_per_frame = 1024
        frames_to_skip = 1
        loudness = -20
        delay = 1

        message_bitarray = bitarray()
        message_bitarray.frombytes(stringToEncode.encode('utf-8'))
        frame_to_edit = len(message_bitarray)

        R_sequence = bitarray(frame_to_edit)
        current_number = 12345
        a_key = 7

        for i in range(frame_to_edit):
            current_number = (a_key * current_number + 2*a_key) % frame_to_edit
            R_sequence[i] = current_number%6>2

        
        original_audio = AudioSegment.from_wav(audioLocation)
        channels = original_audio.split_to_mono()
        original_audio = channels[0]

        echoed_audio = AudioSegment.empty()

        original_audio_sample_number = int(len(original_audio.get_array_of_samples()))
        original_audio_frames = original_audio_sample_number/samples_per_frame
        available_frames = original_audio_frames // (frames_to_skip + 1)

        if available_frames < frame_to_edit:
            print('The audio is too short to encode the message')
            return 'The audio is too short to encode the message'
        
        frames_edited = 0
        skip = 0
        start_index = 0
        end_index = start_index + samples_per_frame

        while frames_edited < frame_to_edit:
            if skip:
                slice_to_edit = original_audio.get_sample_slice(start_index,end_index)
                echoed_audio = echoed_audio + slice_to_edit
                skip = (skip + 1) % (frames_to_skip + 1)
                start_index = end_index
                end_index = end_index + samples_per_frame
                continue
            slice_to_edit = original_audio.get_sample_slice(start_index,end_index)

            if R_sequence[frames_edited]:
                if not message_bitarray[frames_edited]:
                    slice_to_edit = slice_to_edit.overlay(slice_to_edit.apply_gain(loudness), position=delay)
            else:
                if message_bitarray[frames_edited]:
                    slice_to_edit = slice_to_edit.overlay(slice_to_edit.apply_gain(loudness), position=delay)
            
            slice_to_edit_array = slice_to_edit.get_array_of_samples()
            slice_to_edit_original_array = slice_to_edit.get_array_of_samples()
            slice_to_edit_length = len(slice_to_edit.get_array_of_samples())

            if slice_to_edit_length < samples_per_frame:
                to_append_samples = slice_to_edit_original_array[-(samples_per_frame - slice_to_edit_length):]
                to_append = AudioSegment(data=to_append_samples.tobytes(), sample_width=original_audio.sample_width, frame_rate=original_audio.frame_rate, channels=1)
                slice_to_edit = slice_to_edit + to_append

            echoed_audio = echoed_audio + slice_to_edit
            frames_edited += 1
            skip = (skip + 1) % (frames_to_skip + 1)
            start_index = end_index
            end_index = end_index + samples_per_frame

        echoed_audio = echoed_audio + original_audio.get_sample_slice(end_index - samples_per_frame, original_audio_sample_number)

        dir = os.path.dirname(audioLocation)
        echoed_audio.export(dir+'/output-echo.wav', format='wav')

        return dir+'/output-echo.wav'
    
    def decode(self,originalLocation,encodedLocation,messageLength):
        samples_per_frame = 1024
        frames_to_skip = 1  
        original_audio = AudioSegment.from_wav(originalLocation)
        encoded_audio = AudioSegment.from_wav(encodedLocation)

        original_audio = original_audio.split_to_mono()[0]
        encoded_audio = encoded_audio.split_to_mono()[0]

        original_samples = original_audio.get_array_of_samples()
        encoded_samples = encoded_audio.get_array_of_samples()

        R_sequence = bitarray(messageLength)

        current_number = 12345
        a_key = 7

        for i in range(messageLength):
            current_number = (a_key * current_number + 2*a_key) % messageLength
            R_sequence[i] = current_number%6>2

        binary_message = ''
        count = 0
        start_index = 0
        end_index = start_index + samples_per_frame
        skip = 0

        while count < messageLength:
            if skip:
                skip = (skip + 1) % (frames_to_skip + 1)
                start_index = end_index
                end_index = end_index + samples_per_frame
                continue

            current_original = original_samples[start_index:end_index]
            current_encoded = encoded_samples[start_index:end_index]

            different = False
            for j in range(len(current_original)):
                if current_original[j] != current_encoded[j]:
                    different = True
                    break
            
            if different:
                if R_sequence[count]:
                    binary_message += '0'
                else:
                    binary_message += '1'
            else:
                if R_sequence[count]:
                    binary_message += '1'
                else:
                    binary_message += '0'

            count += 1
            skip = (skip + 1) % (frames_to_skip + 1)
            start_index = end_index
            end_index = end_index + samples_per_frame

        binary_message_in_bytes = int(binary_message, 2).to_bytes((len(binary_message) + 7) // 8, 'big')
        decoded_message = binary_message_in_bytes.decode('utf-8')

        return decoded_message




        
