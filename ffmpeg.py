import os
import platform

class FFMPEG():
    def __init__(self):
        self.path_windows = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'windows', 'ffmpeg.exe')
        self.path_linux = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'linux', 'ffmpeg')
        self.path_mac = os.path.join(os.path.dirname(__file__), 'ffmpeg', 'macos', 'ffmpeg')
        
    def get_path(self):
        if platform.system() == 'Windows':
            return self.path_windows
        elif platform.system() == 'Linux':
            return self.path_linux
        elif platform.system() == 'Darwin':
            return self.path_mac
        else:
            raise Exception('OS not supported')
        
    def get_command(self, input_file, output_file, flip=False, speed_factor=1):
        commands = []
        
        # Add ffmpeg path
        commands.append('"{}"'.format(self.get_path()))
        
        # Add input file
        commands.append('-i "{}"'.format(input_file))
        
        # Initialize filters list
        filters = []
        
        # Add hflip filter if flip is True
        if flip:
            filters.append('hflip')
        
        # Add video speed adjustment
        filters.append('setpts=(PTS-STARTPTS)/{}'.format(speed_factor))
        
        # Add audio speed adjustment
        filters.append('atempo={}'.format(speed_factor))
        
        # Combine filters into a single filter string
        filter_str = ','.join(filters)
        
        # Add filter_complex option
        commands.append('-filter_complex "{}"'.format(filter_str))
        
        # Set video codec
        commands.append('-c:v libx264')
        
        # Add output file
        commands.append('"{}"'.format(output_file))
        
        return ' '.join(commands)

def main():
    ffmpeg = FFMPEG()
    print(ffmpeg.get_command('input.mp4', 'output.mp4', flip=True, speed_factor=2.5))

if __name__ == "__main__":
    main()
