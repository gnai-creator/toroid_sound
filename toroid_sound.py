import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine
import math

# Protege a função len se ela tiver sido sobrescrita
len = __builtins__.len

# ============================
# Configurações físicas e sonoras
# ============================

c = 299792458        # Velocidade da luz (m/s)
r = 1e12               # Raio muito grande → simula infinito
duration_ms = 60000   # Duração total do áudio (60s)
num_pulses = 100       # Número de giros do toroide ("wOOmmm")
max_wr_over_c = 0.99   # Limite relativístico
max_w = (max_wr_over_c * c) / r  # Máxima velocidade angular admissível

# ============================
# Geração dos sons
# ============================

segments = []

for i in range(num_pulses):
    w = 0.01 + (i / num_pulses) * max_w
    wr_over_c = (w * r) / c

    if wr_over_c >= 1:
        continue  # Evita singularidade relativística

    # Equação relativística
    v = (4 * w * r) / (np.pi * np.sqrt(1 - wr_over_c ** 2))

    # Frequência do som (entre 50Hz e 300Hz)
    freq = np.interp(v, [0, (4 * c) / np.pi], [50, 300])

    # Tempo de cada pulso e pausa (fica mais rápido)
    pulse_duration = int(np.interp(i, [0, num_pulses], [300, 30]))
    pause_duration = int(np.interp(i, [0, num_pulses], [200, 10]))

    # Gera som da volta do toroide
    pulse = Sine(freq).to_audio_segment(duration=pulse_duration).fade_out(30)
    pause = AudioSegment.silent(duration=pause_duration)
    segments.append(pulse + pause)

# Combina tudo
toroid_sound = sum(segments, AudioSegment.silent(duration=0))

# ============================
# Vibração contínua final
# ============================

v_final = (4 * max_w * r) / (np.pi * np.sqrt(1 - max_wr_over_c ** 2))
freq_final = np.interp(v_final, [0, (4 * c) / np.pi], [50, 300])

vibration = Sine(freq_final).to_audio_segment(duration=1000).fade_in(100).fade_out(100)

# Preenche o restante do tempo com a vibração
remaining_ms = duration_ms - len(toroid_sound)
repeat_count = math.ceil(remaining_ms / len(vibration))
toroid_sound += vibration * repeat_count

# ============================
# Corte final e exportação
# ============================

final_audio = toroid_sound[:duration_ms]
final_audio.export("toroide_tesoura_loop.mp3", format="mp3")
print("✅ Áudio gerado com sucesso: toroide_tesoura_loop.mp3")
