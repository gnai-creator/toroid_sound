import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import math

# Protege a função len
len = __builtins__.len

# Constantes físicas
c = 299_792_458  # velocidade da luz (m/s)
r = 1e12         # raio do toroide (m)
duration_ms = 60000   # duração total do áudio (ms)
num_pulses = 100      # quantidade de "loops"
max_wr_over_c = 0.99
max_w = (max_wr_over_c * c) / r

# Parâmetros do som
min_freq = 126   # Hz, frequência inicial do "wOOmmm"
max_freq = 700   # Hz, frequência final desejada

segments = []

# Geração exponencial dos valores de w para acelerar o efeito
w_values = np.logspace(np.log10(0.01), np.log10(max_w), num_pulses)
logw_min = np.log(w_values[0])
logw_max = np.log(w_values[-1])

for i, w in enumerate(w_values):
    wr_over_c = (w * r) / c
    if wr_over_c >= 0.99:
        break

    # v(w) relativístico
    v = (4 * w * r) / (np.pi * np.sqrt(1 - wr_over_c ** 2))
    loop_interval = 1000 / v  # intervalo entre "wOOmmm" em ms
    loop_interval = max(8, min(loop_interval, 1000))  # evita valores extremos

    # Frequência do tom cresce logaritmicamente com w
    logw = np.log(w)
    base_tone_freq = min_freq + (max_freq - min_freq) * ((logw - logw_min) / (logw_max - logw_min))

    pulse_duration = int(loop_interval * 0.6)
    pause_duration = int(loop_interval * 0.4)

    pulse = Sine(base_tone_freq).to_audio_segment(duration=pulse_duration).fade_out(20)
    pause = AudioSegment.silent(duration=pause_duration)

    segments.append(pulse + pause)

# Junta todos os loops
toroid_sound = sum(segments, AudioSegment.silent(duration=0))

# Preenche com vibração contínua no final (freq final igual ao tom base máximo)
vibration = Sine(max_freq).to_audio_segment(duration=1000).fade_in(100).fade_out(100)
remaining_ms = duration_ms - len(toroid_sound)
if remaining_ms > 0:
    repeat_count = math.ceil(remaining_ms / len(vibration))
    toroid_sound += vibration * repeat_count

# Exporta o resultado
final_audio = toroid_sound[:duration_ms]
final_audio.export("toroide_tesoura_loop.mp3", format="mp3")
print("✅ Som gerado com aceleração temporal e frequência variável (física do toroide)!")
